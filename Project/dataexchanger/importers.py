from counters.models import Counters, Accounts, User
from django.core.cache import cache
from .formats_io import ExcelLoadFormat
from Project import settings
import xlrd


class FileReader:
    def __init__(self):
        self.result = {}
        self.reader_selector = {
            'xls': self.xls_reader,
            'xlsx': self.xlsx_reader,
        }
        self.row_format_selector = {
            'xls': ExcelLoadFormat,
            'xlsx': ExcelLoadFormat,
        }
        self.rows_gen = None
        self.rows_num = None

    def create_rows_generator(self, sheet):
        for row_num in range(1, self.rows_num):
            yield sheet.row_values(row_num)

    def xls_reader(self, file):
        xls_sheet = xlrd.open_workbook(file, formatting_info=True).sheet_by_index(0)
        self.rows_num = xls_sheet.nrows
        return self.create_rows_generator(xls_sheet)

    def xlsx_reader(self, file):
        return


class DataLoader(FileReader):
    def __init__(self, files_list, process_id):
        super().__init__()
        self.row_format = None
        self.counter_buffer = None
        self.process_id = process_id
        self.progress_step = 0
        self.progress = 0
        self.files_list = files_list

    def start_loading(self):
        read_num = 0
        for file in self.files_list:
            extension = file.rsplit('.', 1)[1]
            try:
                self.rows_gen = self.reader_selector[extension](file)
                self.row_format = self.row_format_selector[extension]
                self.progress_step = (100 - self.progress) / (len(self.files_list) - read_num) / (self.rows_num - 1)
                self.load()
                self.result['loading status'] = 'OK'
            except KeyError as e:
                print(str(e))
                self.result['loading status'] = 'Error'
                self.result['error'] = 'Unknown format'
            read_num += 1

        if read_num == len(self.files_list) and cache.get(self.process_id) < 100:
            cache.set(self.process_id, 100)

    """ Данные о двухтарифном счетчике приходят ввиде двух строк
        100004655|Электроэнергия|10001482|Свет (день)|005547
        100004655|Электроэнергия|10001482|Свет (ночь)|005691
        буфер для приведения записи к виду 
        100004655|Электроэнергия|10001482|005547|005691
    """

    def buffer(self, data):
        if not self.counter_buffer:
            self.counter_buffer = data
            return False
        else:
            if self.counter_buffer['day_data']:
                self.counter_buffer['night_data'] = data['night_data']
            else:
                self.counter_buffer['day_data'] = data['day_data']
            return True

    def update_n_write_progress(self):
        self.progress += self.progress_step
        cache.set(self.process_id, round(self.progress))

    @staticmethod
    def write_row_data_to_db(counter_row):
        counter_obj, counter_created = Counters.objects.update_or_create(
            id_out_system=counter_row['id_from_out_db'],
            in_work=True,
            counter_type=counter_row['type_counter'],
            serial_number=counter_row['serial_number'],
            account_id=Accounts(id=counter_row['account']),
            defaults={
                'setup_date': counter_row['setup_date'],
                'creation_date': counter_row['creation_date'],
                'counter_data_simple': counter_row['simple_data'],
                'counter_data_day': counter_row['day_data'],
                'counter_data_night': counter_row['night_data'],
                'old_counter_data_simple': counter_row['simple_data'],
                'old_counter_data_day': counter_row['day_data'],
                'old_counter_data_night': counter_row['day_data'],
                'date_update': counter_row['last_date'],
            }
        )

        if counter_created:
            acc_obj, acc_created = Accounts.objects.update_or_create(
                id=counter_row['account'],
                street=counter_row['street'],
                house_number=counter_row['house_number'],
                apartments_number=counter_row['apartments'],
                user=User(id=counter_row['account'], username=counter_row['account']),
                defaults={
                    'name': counter_row['name'],
                    'date_update': counter_row['last_date'],
                }
            )
            if acc_created:
                user = User(id=counter_row['account'], username=counter_row['account'])
                user.set_password(settings.USERS_PASS)
                user.save()
        else:
            Accounts.objects.filter(id=counter_row['account']).update(
                date_update=counter_row['last_date'],
                name=counter_row['name']
            )

    def load(self):
        for row in self.rows_gen:
            counter_row = self.row_format(row).get_formatted_data()

            if counter_row['day_data'] or counter_row['night_data']:
                if not self.buffer(counter_row):
                    continue
                else:
                    counter_row = self.counter_buffer

            self.write_row_data_to_db(counter_row)
            self.update_n_write_progress()
            self.counter_buffer = None




