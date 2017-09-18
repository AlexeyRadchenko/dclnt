import ast
import os
import collections

from nltk import pos_tag, download

download('averaged_perceptron_tagger')


def flat(_list):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return sum([list(item) for item in _list], [])


def is_verb(word):
    if not word:
        return False
    pos_info = pos_tag([word])
    return 'VB' in pos_info[0][1]


def get_trees(path, with_file_names=False, with_file_content=False, max_files_in_dir=100):
    file_names = []
    trees = []
    for dir_name, dirs, files in os.walk(path, topdown=True):
        for file in files:
            if file.endswith('.py'):
                file_names.append(os.path.join(dir_name, file))
                if len(file_names) == max_files_in_dir:
                    break
    file_names_length = len(file_names)
    if file_names_length:
        print('='*10)
        print('total %s .py files in \'%s\' directory' % (len(file_names), path))
        for file_name in file_names:
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


def get_verbs_from_function_name(function_name):
    return [word for word in function_name.split('_') if is_verb(word)]


def get_functions_names_in_path(path):
    trees = get_trees(path)
    flat_list = flat([[node.name.lower() for node in ast.walk(t) if isinstance(node, ast.FunctionDef)] for t in trees])
    function_names = [f for f in flat_list if not (f.startswith('__') and f.endswith('__'))]
    return function_names


def get_top_verbs_in_path(path):
    function_names = get_functions_names_in_path(path)
    verbs = flat([get_verbs_from_function_name(function_name) for function_name in function_names])
    return verbs

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
    print(word, '-', occurrence)
