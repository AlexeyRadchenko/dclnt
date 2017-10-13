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


