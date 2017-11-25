from counters.models import Counters
from format import BaseFormat


class FileReader:
    def __init__(self, files_list):
        self.result = {}
        for file in files_list:
            extension = file.rsplit('.', 1)[1]
            try:
                self.extensions_readers[extension](file)
                self.result['loading status'] = 'OK'
            except KeyError:
                self.result['loading status'] = 'Error'
                self.result['error'] = 'Unknown format'

    def row_to_db_object(row):
        data_dict = BaseFormat(row).get_formated_data()
        return Counters(
            id = data_dict['id']
        )
    def xls_reader(file):
        sheet = xlrd.open_workbook(file, formatting_info=True).sheet_by_index(0)
        counters_list = list(Counters.objects.all())
        for rownum in range(1, sheet.nrows):
            row = sheet.row_values(rownum)
        return counters_list

    def xlsx_reader(self):
        return

    extensions_readers = {
        'xls': xls_reader,
        'xlsx': xlsx_reader,
    }

print(FileReader(['text.xls']).xls_reader())