Analyze words in your python project.
====================================

  - Python - 3.6
  - GitPython - 2.1.7
  - nltk - 3.2.4

Description
-----------
This script generate next statistics:
<p>- top words in functions or variables names</p>
<p>- top verbs or nouns in names functions, classes and variables</p>

Results can be written in JSON or CSV files.
  
Install requirements
--------------------  
```sh
$ cd lesson3
$ pip3 install -r requirements.txt
```  
How using
-------
If local repository is not exists, you can download it from GitHub:
<p>(-c, --clone)</p>
<p>(-p, --path_to, default=download_repository)</p>
  
```sh
$ python analyze_it.py --clone <url> --path_to <local path>
```

Get top 10 verbs or nouns :
<p>(-v, --verbs)</p>

```sh
$ python analyze_it.py --path_to <local path> --verbs
```
<p>(-n, --nouns)</p>

```sh
python analyze_it.py --path_to <local path> --nouns
```
Get top 10 words in functions names or variables names:
<p>(-f, --functions)</p>

```sh
$ python analyze_it.py --path_to <local path> --functions
```
<p>(-vr, --vars)</p>

```sh
python analyze_it.py --path_to <local path> --vars

```
You can get result in JSON or CSV file:
<p>(-j, --json)</p>

```sh
python analyze_it.py --path_to <local path> --json <file_name.json>
```
<p>(-csv)</p>

```sh
python analyze_it.py --path_to <local path> --json <file_name.csv>
```