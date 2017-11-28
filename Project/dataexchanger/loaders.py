from counters.models import Counters, Accounts, User
from .input_format import BaseFormat
import xlrd


class FileReader:

    def __init__(self, files_list):
        self.result = {}
        self.extensions_readers = {
            'xls': self.xls_reader,
            'xlsx': self.xlsx_reader,
        }
        self.rows = []

        for file in files_list:
            extension = file.rsplit('.', 1)[1]
            try:
                self.rows = self.extensions_readers[extension](file)
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

"""
    def xls_reader(self, file):
        sheet = xlrd.open_workbook(file, formatting_info=True).sheet_by_index(0)
        counters_in_db = Counters.objects.all()
        for row_num in range(1, sheet.nrows):
            row = sheet.row_values(row_num)
            

            else:
                print(True)"""


class DataLoader(FileReader):
    def __init__(self, files_list):
        super().__init__(files_list)
        self.counter_buffer = None

    """"@staticmethod
    def row_to_counters_object(row):
        data_dict = BaseFormat(row).get_formatted_data()
        return Counters(
            id_out_system=data_dict['id_from_out_db'],
            in_work=True,
            counter_type=data_dict['type_counter'],
            serial_number=data_dict['serial_number'],
            counter_data_simple=data_dict['simple_data'],
            counter_data_day=data_dict['day_data'],
            counter_data_night=data_dict['night_data'],
            date_update=data_dict['last_date'],
            account_id=Accounts(id=data_dict['account'],
                                street=data_dict['street'],
                                house_number=data_dict['house_number'],
                                apartments_number=data_dict['apartments'],
                                user=User(username=data_dict['account'],
                                          password='asdwaDAWfaSDG#$@fs',
                                          is_superuser=False)
                                )
        )
        Accounts(id=counter['account'],
                                    street=counter['street'],
                                    house_number=counter['house_number'],
                                    apartments_number=counter['apartments'],
                                    user=User(username=counter['account'],
                                              password='asdwaDAWfaSDG#$@fs',
                                              is_superuser=False)
                                    )"""
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
        for row in self.rows:
            counter_row = BaseFormat(row).get_formatted_data()
            if counter_row['day_data'] or counter_row['night_data']:
                if not self.buffer(counter_row):
                    continue
                else:
                    counter_row = self.counter_buffer
            print(counter_row['id_from_out_db'], counter_row['day_data'], counter_row['night_data'])
            obj, created = Counters.objects.update_or_create(
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
            if created:
                self.counter_buffer = None
                print('create', obj.counter_data_day, obj.counter_data_night)
            else:
                print('update', obj.counter_data_day, obj.counter_data_night)
#print(FileReader(['text.xls']).xls_reader())
"""
Accounts(id=data_dict['account'], street=data_dict['street'], house_number=data_dict['house_number'], apartments_number=data_dict['apartments'])"""