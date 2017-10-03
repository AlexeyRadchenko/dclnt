import ast
import os
import collections
from find_all_words_in_py.words_getter_class import WordsGetter
from find_py_files.py_files_getter_class import PyFileFinder
from top_getters.top_getter_class import TopGetter


def main():
    #trees = PyFileFinder('./pyramid')
    #print('trees',trees)
    vars = WordsGetter('./pyramid')
    verbs = TopGetter('./pyramid')
    #print(vars.get_all_words_in_path())
    print('functions: ', vars.get_functions_name_words())
    print('classes: ', vars.get_classes_name_words())
    print('vars: ', vars.get_vars_name_words())
    print('all words: ', vars.get_all_words_in_path())
    print('functions names', vars.get_functions_names())
    print('top words in path: ', verbs.get_top_words_in_path(top_size=5))
    print('top words in vars: ', verbs.get_top_words_in_vars_names())
    print('top words in functions: ', verbs.get_top_words_in_functions_names())
    print('top words in classes: ', verbs.get_top_words_in_classes_names())
    print('top verbs in path: ', verbs.get_top_verbs_in_path())
    print('top verbs in vars: ', verbs.get_top_verbs_in_vars_names())
    print('top verbs in functions: ', verbs.get_top_verbs_in_functions_names())
    print('top verbs in classes: ', verbs.get_top_verbs_in_classes_names())
    #for tree in trees:
    #    for node in ast.walk(tree):
    #        if isinstance(node, ast.Name):
    #            print(node.id)
    #        if isinstance(node, ast.FunctionDef):
    #            print(node.name)
    """
    words = []
    projects = [
        'django',
        'flask',
        'pyramid',
        'reddit',
        'requests',
        'sqlalchemy',
    ]

    for project in projects:
        path = os.path.join('.', project)
        words.extend(get_top_verbs_in_path(path))
    if len(words):
        print('functions extracted')
    top_size = 200
    print('total %s words, %s unique' % (len(words), len(set(words))))

    for word, occurrence in collections.Counter(words).most_common(top_size):
        print(word, '-', occurrence)"""


if __name__ == '__main__':
    main()
