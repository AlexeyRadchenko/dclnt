import sys

from command_handlers import *
from top_getters.top_getter_class import TopGetter


def main(params):
    if params.path_to and params.clone:
        clone_git_repos.clone(args.clone, args.path_to)

    elif params.path_to and not params.clone:
        datagetter = TopGetter(params.path_to)
        data = None

        if params.verbs:
            data = datagetter.get_top_verbs_in_path()
            print('Top verbs in path: ')

        if params.nouns:
            data = datagetter.get_top_nouns_in_path()
            print('Top nouns in path: ')

        if params.functions:
            data = datagetter.get_top_words_in_functions_names()
            print('Top words in functions names: ')

        if params.vars:
            data = datagetter.get_top_words_in_vars_names()
            print('Top words in vars names')

        if params.json:
            out.to_jason_file(params.json, data)

        if params.csv:
            out.to_csv_file(params.csv, data)

        if not params.json and not params.csv and data:
            for word in data:
                print(word)
    else:
        print('Please, use "-p" or "--path" for set repository directory or set checking directory')

if __name__ == '__main__':
    parser = command_parser.create_parser()
    args = parser.parse_args(sys.argv[1:])
    main(args)
