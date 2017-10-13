import json
import csv


def to_jason_file(filename, data):
    with open(filename, 'w') as outfile:
        json.dump(dict(data), outfile)
    print('data write in '+filename)


def to_csv_file(filename, data):
    with open(filename, 'w') as outfile:
        datawriter = csv.writer(outfile, delimiter=',', quotechar='|')
        for row in data:
            datawriter.writerow(row)
    print('data write in ' + filename)