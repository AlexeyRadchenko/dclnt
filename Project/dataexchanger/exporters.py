import xlwt
from formats import ExcelUnloadFormat
#from counters.models import Counters


class FileWriter:
    def __init__(self, file_extension, counters_type, separated_of_counters_type):
        self.counters_type = counters_type
        self.separated_of_counters_type = separated_of_counters_type
        self.file_type = file_extension
        self.result = {}
        self.extensions_writers = {
            'xls': self.xls_writer,
            'xlsx': self.xlsx_writer,
        }
        self.row_format_selector = {
            'xls': ExcelUnloadFormat,
            'xlsx': ExcelUnloadFormat,
        }

    @staticmethod
    def xls_writer():
        book = xlwt.Workbook()
        sheet = book.add_sheet('TDSheet', cell_overwrite_ok=True)
        style = xlwt.easyxf(ExcelUnloadFormat.header_style)
        for i, column in enumerate(ExcelUnloadFormat.header):
            sheet.write(0, i, column[0], style)
            sheet.col(i).width = column[1]
        return book, sheet

    def xlsx_writer(self):
        pass


class DataUnloader(FileWriter):
    def __init__(
            self,
            file_extension,
            account=None,
            street=None,
            house_number=None,
            apartments=None,
            counters_type=None,
            separated_of_counters_type=False
    ):
        super().__init__(file_extension, counters_type, separated_of_counters_type)
        self.account = account
        self.street = street
        self.house_number = house_number
        self.apartments = apartments
        self.writer = self.extensions_writers[file_extension]()
        self.unload()

    def get_account_data_form_db(self):
        if self.account:
            pass

    def get_counter_data_from_db(self):
        pass

    def get_data_from_db(self):
        pass

    def unload(self):
        pass
