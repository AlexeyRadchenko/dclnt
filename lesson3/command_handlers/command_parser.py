import argparse


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clone', help='set clone github repository', metavar='<repository url>')
    parser.add_argument('-p', '--path_to', help='set local path where repository download', metavar='<local path>',
                        default='download_repository')
    parser.add_argument('-v', '--verbs', help='find top verbs', action='store_true')
    parser.add_argument('-n', '--nouns', help='find top nouns', action='store_true')
    parser.add_argument('-f', '--functions', help='find top words in functions names', action='store_true')
    parser.add_argument('-vr', '--vars', help='find top words in vars names', action='store_true')
    parser.add_argument('-j', '--json', help='write to json file', metavar='<file_name.json>')
    parser.add_argument('-csv', help='write to json file', metavar='<file_name.csv>')

    return parser
