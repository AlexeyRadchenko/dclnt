from git import Repo

"""Repo.clone_from(git_url, repo_dir) ('https://github.com/realpython/python-scripts.git', 'cloned')"""


def clone(git_url, repo_dir):
    repo = Repo.clone_from(git_url, repo_dir)
    print('Repository cloned to path: ' + repo.common_dir.strip('.git'))
