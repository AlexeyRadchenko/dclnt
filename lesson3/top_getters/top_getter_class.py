import collections
from top_getters.words_type_checker import *
from find_all_words_in_py.words_getter_class import WordsGetter


class TopGetter(WordsGetter):
    def __init__(self, path):
        super().__init__(path)

# =====wraps======
    def top_get_words(self, function_getter, top_size):
        checked_words = [word for word in function_getter()]
        return collections.Counter(checked_words).most_common(top_size)

    def top_get_words_type(self, function_getter, function_checker, top_size):
        checked_words = [word for word in function_getter() if function_checker(word)]
        return collections.Counter(checked_words).most_common(top_size)


# ====top words in path, vars, functions, classes names======
    def get_top_words_in_path(self, top_size=10):
        return self.top_get_words(super().get_all_words_in_path, top_size)

    def get_top_words_in_vars_names(self, top_size=10):
        return self.top_get_words(super().get_vars_name_words, top_size)

    def get_top_words_in_functions_names(self, top_size=10):
        return self.top_get_words(super().get_functions_name_words, top_size)

    def get_top_words_in_classes_names(self, top_size=10):
        return self.top_get_words(super().get_classes_name_words, top_size)

#====top verbs in path, vars, functions, classes names====
    def get_top_verbs_in_path(self, top_size=10):
        return self.top_get_words_type(super().get_all_words_in_path, is_verb, top_size)

    def get_top_verbs_in_vars_names(self, top_size=10):
        return self.top_get_words_type(super().get_vars_name_words, is_verb, top_size)

    def get_top_verbs_in_functions_names(self, top_size=10):
        return self.top_get_words_type(super().get_functions_name_words, is_verb, top_size)

    def get_top_verbs_in_classes_names(self, top_size=10):
        return self.top_get_words_type(super().get_classes_name_words, is_verb, top_size)

#====top nouns in path, vars, functions, classes names====
    def get_top_nouns_in_path(self, top_size=10):
        return self.top_get_words_type(super().get_all_words_in_path, is_noun, top_size)

    def get_top_nouns_in_vars_names(self, top_size=10):
        return self.top_get_words_type(super().get_vars_name_words, is_noun, top_size)

    def get_top_nouns_in_functions_names(self, top_size=10):
        return self.top_get_words_type(super().get_functions_name_words, is_noun, top_size)

    def get_top_nouns_in_classes_names(self, top_size=10):
        return self.top_get_words_type(super().get_classes_name_words, is_noun, top_size)