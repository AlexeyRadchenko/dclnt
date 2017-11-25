import re


class BaseFormat:
    def __init__(self, row):
        self.data = {
            'N': int(row[0]),
            'account': row[1].strip(' '),
            'street': row[3].split(',')[0].strip(' '),
            'house_number': row[3].split(',')[1].strip(' '),
            'appartments': row[4].strip(' '),
            'type_counter': re.search(r'\D+', row[5].strip(' ')).group(0).capitalize(),
            'serial_number_end': re.search(r'\d+', row[5].strip(' ')).group(0),
            'id_from_out_db': (row[6].strip(' ')),
            'tarif': row[7].strip(' '),
            'last_counter_data': float(re.sub(r'^0+', '', row[8]).strip(' ').replace(',', '.')),
            'now_counter_data': None,
            'last_date': row[13].strip(' ')
        }

    def get_formated_data(self):
        return self.data
"""
row = [1.0,
       '100000023 ',
       'Есиков Олег Александрович_',
       'Островского,29', '1',
       'Холодная вода8687',
       '10013576 ',
       'Обычные',
       '000000,833',
       '000000,833',
       0.0,
       '01.09.2017',
       '30.09.2017',
       '31.08.2017'
       ]
data = BaseFormat(row).get_formated_data()
print(data)"""