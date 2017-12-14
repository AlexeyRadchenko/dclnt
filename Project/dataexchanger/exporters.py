import xlwt
from .formats_io import ExcelUnloadFormat
from counters.models import Counters, Accounts
from datetime import date
from django.conf import settings


class FileWriter:
    def __init__(self, file_extension):

        self.file_type = file_extension
        self.result = {}
        self.writers_selector = {
            'xls': self.xls_writer,
            'xlsx': self.xlsx_writer,
        }
        self.row_format_selector = {
            'xls': ExcelUnloadFormat,
            'xlsx': ExcelUnloadFormat,
        }

    @staticmethod
    def xls_write_rows(writer, rows, style=None):
        for i, column in enumerate(rows):
            writer.write(0, i, column[0], style)
            writer.col(i).width = column[1]

    def xls_writer(self):
        book = xlwt.Workbook()
        sheet = book.add_sheet('TDSheet', cell_overwrite_ok=True)
        self.xls_write_rows(sheet, ExcelUnloadFormat.header, xlwt.easyxf(ExcelUnloadFormat.header_style))
        return book, sheet

    def xlsx_writer(self):
        pass


class DataUnloader(FileWriter):
    def __init__(
            self,
            file_extension,
            #month,
            #year,
            account=None,
            street=None,
            house_number=None,
            apartments=None,
            counters_type=None,
            separated_of_counters_type=False,
    ):
        super().__init__(file_extension)
        self.account = account
        self.street = street
        self.house_number = house_number
        self.apartments = apartments
        self.counters_type = counters_type
        self.separated_of_counters_type = separated_of_counters_type
        self.month = date.today().month
        self.year = date.today().year
        self.writer = self.writers_selector[file_extension]()
        self.unload()

    def db_data_to_row_data(self, num_row, db_data):
        counter_type, type_data, current_value, old_value = None, None, None, None
        if db_data['counter_type'] == 'Электроэнергия':
            counter_type = db_data['counter_type']
            if db_data['counter_data_day']:
                type_data = 'Свет (день)'
                current_value = db_data['counter_data_day']
                old_value = db_data['old_counter_data_day']
            elif db_data['counter_data_night']:
                type_data = 'Свет (ночь)'
                current_value = db_data['counter_data_night']
                old_value = db_data['old_counter_data_night']
            else:
                type_data = 'Обычные'
                current_value = db_data['counter_data_simple']
                old_value = db_data['old_counter_data_simple']
        else:
            type_data = 'Обычные'
            counter_type = '{0}{1}'.format(db_data['counter_type'], db_data['serial_number'])
            current_value = db_data['counter_data_simple']
            old_value = db_data['old_counter_data_simple']
        row = [
            num_row,
            db_data['account_id'],
            db_data['account_id__name'],
            '{0},{1}'.format(
                db_data['account_id__street'], db_data['account_id__house_number']
            ),
            db_data['account_id__apartments_number'],
            counter_type,
            db_data['id_out_system'],
            type_data,
            old_value,
            current_value,
            xlwt.Formula('J{0}-I{0}'.format(num_row+1)),
            '01.09.2017',
            '30.09.2017',
            db_data['date_update'],

        ]
        return row

    def get_data_from_db(self):
        counters_objects = Counters.objects.select_related(
            'account_id'
        ).filter(
            date_update__year=self.year,
            date_update__month=self.month,
            #in_work=True
        ).values(
            'account_id',
            'account_id__name',
            'account_id__street',
            'account_id__house_number',
            'account_id__apartments_number',
            'counter_type',
            'id_out_system',
            'serial_number',
            'counter_data_simple',
            'counter_data_day',
            'counter_data_night',
            'old_counter_data_simple',
            'old_counter_data_day',
            'old_counter_data_night',
            'date_update'
        )

        return counters_objects

    def unload(self):
        if not self.counters_type and not self.separated_of_counters_type:
            db_data = self.get_data_from_db()
            book, sheet = self.writer
            for row, data in enumerate(db_data, start=1):
                row_data = self.db_data_to_row_data(row, data)
                for column, cell_value in enumerate(row_data):
                    sheet.write(row, column, cell_value)
            book.save(settings.BASE_DIR+'/media/export/sd.xls')
        elif self.counters_type:
            print('dva')
            pass
        elif self.separated_of_counters_type:
            print('tri')
            pass
