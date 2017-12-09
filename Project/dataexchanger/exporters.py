import xlwt
from formats import ExcelUnloadFormat
from counters.models import Counters, Accounts
from datetime import date


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
            month,
            year,
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
        self.month = month
        self.year = year
        self.writer = self.writers_selector[file_extension]()
        self.unload()

    def get_account_data_form_db(self):
        if self.account:
            pass

    def get_counter_data_from_db(self):
        pass

    def get_data_from_db(self):
        """
        Counters.objects.values(
            'account',
            'name',
            'street',
            'house_number',
            'apartments',
            'counter'
        )"""
        counters_objects = Counters.objects.filter(
            date_update__year=date.today().year,
            date_update__month=date.today().month
        ).annotate(
            name=Accounts('name'),
            street=Accounts('street'),
            house_number=Accounts('house_number'),
            apartments=Accounts('apartments'),
        )
        for counter in counters_objects:
            print(counter.account_id, counter.street)

    def unload(self):
        if not self.counters_type and not self.separated_of_counters_type:
            pass
        elif self.counters_type:
            pass
        elif self.separated_of_counters_type:
            pass

counters = Counters.objects.filter(
            date_update__year=date.today().year,
            date_update__month=date.today().month
        )
for counter in counters:
    print(counter)