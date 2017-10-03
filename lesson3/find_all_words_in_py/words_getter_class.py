from find_py_files.py_files_getter_class import PyFileFinder
from find_all_words_in_py.flat_mixin import FlatMixin
from find_all_words_in_py.classes_vars_funcs_mixin import FindVarsClassFunctionsMixin


class WordsGetter(PyFileFinder, FlatMixin, FindVarsClassFunctionsMixin):
    def __init__(self, path):
        self.path = path
        self.trees = super().get_trees_from_files_names(path)

    def names_get(self, function):
            return [f for f in self.flat([function(t[1]) for t in self.trees]) if not (f.startswith('__') and f.endswith('__'))]

    @staticmethod
    def split_snake_case_name_to_words(name):
        return [n for n in name.split('_') if n]

    def get_functions_name_words(self):
        function_names = self.names_get(self.get_all_names_functions_in_tree)
        return self.flat([self.split_snake_case_name_to_words(function_name) for function_name in function_names])

    def get_classes_name_words(self):
        classes_names = self.names_get(self.get_all_names_classes_in_tree)
        return self.flat([self.split_snake_case_name_to_words(classes_name) for classes_name in classes_names])

    def get_vars_name_words(self):
        vars_names = self.names_get(self.get_all_names_vars_in_tree)
        return self.flat([self.split_snake_case_name_to_words(var_name) for var_name in vars_names])

    def get_all_words_in_path(self):
        all_words = self.names_get(self.get_all_names_in_tree)
        return self.flat([self.split_snake_case_name_to_words(word) for word in all_words])
    
    def get_functions_names(self):
        return self.names_get(self.get_all_names_functions_in_tree)

    def get_classes_names(self):
        return self.names_get(self.get_all_names_classes_in_tree)

    def get_vars_names(self):
        return self.names_get(self.get_all_names_vars_in_tree)



