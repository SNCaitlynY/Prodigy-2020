import json
import re
from parse_cat import get_cat
# -*- coding: UTF-8 -*-
from prodigy.components.db import connect

db = connect()
all_dataset_names = db.datasets
print('all_dataset_names = ', all_dataset_names)

examples1 = db.get_dataset("udn_A")
print('len(examples1） = ', len(examples1))
print('')

with open('./data/udn_db/db_A.txt', "w", encoding='utf8') as target:
    for i in range(len(examples1)):
        #print(examples1[i])
        #print()
        json.dump(examples1[i], target, ensure_ascii=False)
        target.write('\n')
    target.close()

def get_core_terms():
    with open('./data/coreterm.txt', 'r') as fp:
        line = fp.readline()
        core =[]
        while line:
            c = line.split()
            core.append(c[0])
            line = fp.readline()
    return core

core = get_core_terms()
cats = get_cat()
catid_list = cats.keys()

total_count = 0
total_matches = 0


with open(source_file, 'r') as f:

    count = 0
    matches = 0
    line = f.readline()
    # print(line)
    while line:
        for term in core:
            start = line.find(term)
            # if find term in text
            if start != -1:
                matches += 1
                break
        count += 1
        line = f.readline()


rate = matches/count*100
print('{:,}/{:,}   rate={:.1f}%'.format(matches, count, rate))












