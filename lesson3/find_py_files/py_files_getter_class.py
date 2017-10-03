import ast
from find_py_files.file_names_getter_mixin import FileNamesGetterMixin


class PyFileFinder(FileNamesGetterMixin):
    def __init__(self, path):
        self.path = path

    def get_trees_from_files_names(self, with_file_names=False, with_file_content=False):
        trees = []
        for file_name in self.get_file_names(self.path):
            with open(file_name, 'r', encoding='utf-8') as attempt_handler:
                    main_file_content = attempt_handler.read()
            try:
                tree = ast.parse(main_file_content)
            except SyntaxError as e:
                print(e)
                tree = None
            if with_file_names:
                if with_file_content:
                    trees.append((file_name, main_file_content, tree))
                else:
                    trees.append((file_name, tree))
            else:
                trees.append(tree)
        print('trees generated')
        return trees
