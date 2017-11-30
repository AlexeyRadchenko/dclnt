from counters.models import Counters, Accounts, User
from .formats import LoadFormat
from Project import settings
import xlrd


class FileReader:

    def __init__(self, files_list):
        self.result = {}
        self.extensions_readers = {
            'xls': self.xls_reader,
            'xlsx': self.xlsx_reader,
        }
        self.rows_gen = None

        for file in files_list:
            extension = file.rsplit('.', 1)[1]
            try:
                self.rows_gen = self.extensions_readers[extension](file)
                self.result['loading status'] = 'OK'
            except KeyError as e:
                print(str(e))
                self.result['loading status'] = 'Error'
                self.result['error'] = 'Unknown format'

    @staticmethod
    def xls_reader(file):
        sheet = xlrd.open_workbook(file, formatting_info=True).sheet_by_index(0)
        for row_num in range(1, sheet.nrows):
            yield sheet.row_values(row_num)

    @staticmethod
    def xlsx_reader(file):
        return


class DataLoader(FileReader):
    def __init__(self, files_list):
        super().__init__(files_list)
        self.counter_buffer = None

    """
    Данные о двухтарифном счетчике приходят ввиде двух строк
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

    def load(self):
        for row in self.rows_gen:
            counter_row = LoadFormat(row).get_formatted_data()
            if counter_row['day_data'] or counter_row['night_data']:
                if not self.buffer(counter_row):
                    continue
                else:
                    counter_row = self.counter_buffer

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
                    'date_update': counter_row['last_date']
                }
            )
            self.counter_buffer = None

            if counter_created:
                acc_obj, acc_created = Accounts.objects.update_or_create(
                    id=counter_row['account'],
                    street=counter_row['street'],
                    house_number=counter_row['house_number'],
                    apartments_number=counter_row['apartments'],
                    user=User(id=counter_row['account'], username=counter_row['account']),
                    defaults={
                        'date_update': counter_row['last_date'],
                    }
                )

                if acc_created:
                    user = User(id=counter_row['account'], username=counter_row['account'])
                    user.set_password(settings.USERS_PASS)
                    user.save()
            else:
                Accounts.objects.filter(id=counter_row['account']).update(date_update=counter_row['last_date'])
