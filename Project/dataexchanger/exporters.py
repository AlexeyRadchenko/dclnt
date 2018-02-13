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

    def get_data_from_db(self):
        counters_objects = Counters.objects.select_related(
            'account_id'
        ).filter(
            date_update__year=self.year,
            date_update__month=self.month,
            in_work=True
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
                row_data = ExcelUnloadFormat(row, data).db_data_to_row_data()
                for column, cell_value in enumerate(row_data):
                    sheet.write(row, column, cell_value)
            book.save(settings.BASE_DIR+'/media/export/sd.xls')
        elif self.counters_type:
            pass
        elif self.separated_of_counters_type:
            pass
