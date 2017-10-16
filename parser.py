import sys
import re
import json
import requests
from datetime import datetime

infile = 'logs.log'
outfile = 'parsed.txt'

response = requests.get('http://192.168.56.33:9200/mapping_report_index/_search')
json_data = response.json()

def getFromRegex(message, reg):
    reg = re.compile(reg)
    aux = reg.search(message)
    if aux:
        return aux.group(1)
    return None

def getDate(date):
    date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f+00:00')
    return date.strftime('%Y-%m-%d %H:%M:%S')

def hundred(source):
    date = getDate(source['_source']['datetime'])
    message = source['_source']['message']
    total_vacancies = getFromRegex(message, 'Processed (.\w+.\w+)')
    inserted_vacancies = getFromRegex(message, 'inserted (.\w*)')
    skipped_vacancies = getFromRegex(message, 'skipped (.\w*)')
    updated_vacancies = getFromRegex(message, 'updated (.\w*)')

    return (date + "\tTotal:" + total_vacancies + "\tInserted:" + inserted_vacancies + "\tSkipped:"
        + skipped_vacancies + "\tUpdated:" + updated_vacancies + '\n')

def four_hundred(source):
    message = source['_source']['message']
    value = getFromRegex(message, 'value "(.\w*)')
    if source['_source']['datetime']:
        date = getDate(source['_source']['datetime'])
    vendor = source['_source']['extra']['cmd'][2]
    attribute = getFromRegex(message, 'criteria/(.\w+)')
    return date + "\t" + vendor + "\t" + value + "\t"  + attribute + "\n"

options = { 100 : hundred, 400 : four_hundred}

def getSource(source):
    return options[source['_source']['level']](source)

with open(outfile, "w+") as outf:
    for key, value in json_data.iteritems():
        if key == 'hits':
            results = filter(None, (getSource(source) for source in value['hits']))
            outf.writelines(''.join(results))
