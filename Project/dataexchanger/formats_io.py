import re
from datetime import datetime


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

    def __init__(self, row):
        pass

"""'000000,833'"""
"""
row = [1.0,
       '100000023 ',
       'Есиков Олег Александрович_',
       'Островского,29', '1',
       'Холодная вода8687',
       '10013576 ',
       'Свет (день)',
       '070153',
       '070153',
       0.0,
       '01.09.2017',
       '30.09.2017',
       '31.08.2017'
       ]
data = BaseFormat(row).get_formatted_data()
print(data)"""