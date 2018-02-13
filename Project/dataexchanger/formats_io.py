import re
from datetime import datetime
import xlwt


class ExcelLoadFormat:
    def __init__(self, row):
        self.data = {
            'N': int(row[0]),
            'account': row[1].strip(' '),
            'street': row[3].split(',')[0].strip(' '),
            'house_number': row[3].split(',')[1].strip(' '),
            'apartments': row[4].strip(' '),
            'type_counter': re.search(r'\D+', row[5].strip(' ')).group(0).capitalize(),
            'serial_number': (
                re.search(r'\d+', row[5].strip(' ')).group(0) if re.search(r'\d+', row[5].strip(' ')) else None
            ),
            'id_from_out_db': (row[6].strip(' ')),
            'tarif': row[7].strip(' '),
            'last_counter_data': float(re.sub(r'^0+', '', row[8]).strip(' ').replace(',', '.')),
            'simple_data': None,
            'day_data': None,
            'night_data': None,
            'last_date': datetime.now(),
            'creation_date': None,
            'setup_date': None,
            'name': row[2].strip(' ')
        }

    def data_type_checker(self):
        if 'день' in self.data['tarif']:
            self.data['day_data'] = self.data['last_counter_data']
        elif 'ночь' in self.data['tarif']:
            self.data['night_data'] = self.data['last_counter_data']
        else:
            self.data['simple_data'] = self.data['last_counter_data']

    def get_formatted_data(self):
        self.data_type_checker()
        return self.data


class ExcelUnloadFormat:
    header = [
        ('N', 2000),
        ('Номер', 5000),
        ('Лицевой счет', 7000),
        ('Дом', 5000),
        ('Помещение', 3000),
        ('Счетчик', 5000),
        ('Код', 5000),
        ('Вид показаний', 5000),
        ('Начальные показания', 7000),
        ('Конечные показания', 7000),
        ('Количество', 5000),
        ('Дата начала показаний', 8000),
        ('Дата окончания показаний', 8000),
        ('Дата последних показаний', 8000)
    ]
    header_style = "font:name Arial; font: bold on; align: horiz center; pattern: pattern solid, fore_colour gray25;"
    formula = None

    def __init__(self, num_row, db_data):
        self.num_row = num_row
        self.db_data = db_data

    def db_data_to_row_data(self):
        if self.db_data['counter_type'] == 'Электроэнергия':
            counter_type = self.db_data['counter_type']
            if self.db_data['counter_data_day']:
                type_data = 'Свет (день)'
                current_value = self.db_data['counter_data_day']
                old_value = self.db_data['old_counter_data_day']
            elif self.db_data['counter_data_night']:
                type_data = 'Свет (ночь)'
                current_value = self.db_data['counter_data_night']
                old_value = self.db_data['old_counter_data_night']
            else:
                type_data = 'Обычные'
                current_value = self.db_data['counter_data_simple']
                old_value = self.db_data['old_counter_data_simple']
        else:
            type_data = 'Обычные'
            counter_type = '{0}{1}'.format(self.db_data['counter_type'], self.db_data['serial_number'])
            current_value = self.db_data['counter_data_simple']
            old_value = self.db_data['old_counter_data_simple']
        row = [
            self.num_row,
            self.db_data['account_id'],
            self.db_data['account_id__name'],
            '{0},{1}'.format(
                self.db_data['account_id__street'], self.db_data['account_id__house_number']
            ),
            self.db_data['account_id__apartments_number'],
            counter_type,
            self.db_data['id_out_system'],
            type_data,
            old_value,
            current_value,
            xlwt.Formula('J{0}-I{0}'.format(self.num_row+1)),
            '01.09.2017',
            '30.09.2017',
            self.db_data['date_update'].strftime("%d.%m.%Y"),

        ]
        return row
