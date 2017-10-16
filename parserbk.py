import sys
import re
import json
import requests
from datetime import datetime

infile, outfile = 'logs.log', 'parsed.txt'

def getValues(words):
    attribute = ''
    value = ''
    vendor = ''

    rege = re.compile('cmd: (.*)')
    search = rege.search(words[1])

    if search:
        vendor = re.sub('[\]\}"]', '', search.group(1).split(',')[2])

    reg = re.compile('value "(.*?)"')
    search = reg.search(words[1])

    if search:
        value = search.group(1)

    rege = re.compile('criteria/(.\w+)')
    search = rege.search(words[1])
    if search:
        attribute = search.group(1)

    if attribute is not '':
        return re.sub('[\[\]]', '', words[0]) + '\t' + value + '\t' + attribute + '\t ' + vendor

with open(infile) as inf, open(outfile,"w") as outf:
    line_words = (line.split('logger.') for line in inf)
    results = filter(None, [getValues(words) for words in line_words if len(words) > 1])
    #from collections import OrderedDict
    #results = OrderedDict.fromkeys(results)

    outf.writelines('\n'.join(results))
