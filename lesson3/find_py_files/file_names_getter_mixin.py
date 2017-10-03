import os


class FileNamesGetterMixin:
    @staticmethod
    def get_file_names(path):
        file_names = []
        for dir_name, dirs, files in os.walk(path, topdown=True):
            for file in files:
                if file.endswith('.py'):
                    file_names.append(os.path.join(dir_name, file))
                    if len(file_names) == 100:
                        break
        print('=' * 10)
        print('total %s .py files in \'%s\' directory' % (len(file_names), path))
        return file_names
