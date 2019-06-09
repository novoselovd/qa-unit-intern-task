import sys
import json
import os.path
from dateutil import parser

objects = []


# Returns true if file exists
def check_file(path):
    return os.path.isfile(path)


# Writes the resulted data to file
def write_output(res):
    with open('output.json', 'w') as outfile:
        json.dump(res, outfile, indent=4, ensure_ascii=False)


# Goes through given files, compares data, adds matched data to OBJECTS list
def analyze(data):
    try:
        with open(data[1], 'r') as a, open(data[2], 'r') as b, open(data[3], 'r') as c:
            one = json.load(a)
            two = json.load(b)
            three = json.load(c)

        for i in one['logs']:
            for j in range(len(three['captures'])):
                if i['time'] == str(int(parser.parse(three['captures'][j]['time']).timestamp())):
                    objects.append({'name': i['test'], 'status': i['output'],
                                    'expected': three['captures'][j]['expected'],
                                    'actual': three['captures'][j]['actual']})
                    three['captures'].pop(j)

        for i in two['suites']:
            for k in i['cases']:
                for j in range(len(three['captures'])):
                    if str(int(parser.parse(k['time']).timestamp())) \
                            == str(int(parser.parse(three['captures'][j]['time']).timestamp())):
                        objects.append({'name': i['name'] + ' - ' + k['name'],
                                        'status': 'fail' if int(k['errors']) != 0 else 'correct',
                                        'expected': three['captures'][j]['expected'],
                                        'actual': three['captures'][j]['actual']})
                        three['captures'].pop(j)

        temp = dict()
        temp['results'] = objects

        write_output(temp)

    except IOError as e:
        print('Operation failed: %s' % e.strerror)


def main():
    if len(sys.argv) != 4:
        print('USAGE: python app.py file1_path.json file2_path.json file3_path.json')
    else:
        if check_file(sys.argv[1]) and check_file(sys.argv[2]) and check_file(sys.argv[3]):
            analyze(sys.argv)
        else:
            print('One or more files do not exist')


if __name__ == '__main__':
    main()
