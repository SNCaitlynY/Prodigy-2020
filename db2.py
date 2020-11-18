# -*- coding: UTF-8 -*-
import json
from prodigy.components.db import connect

db_settings = {'path': '/Users/shaoning/prodigy', 'name': 'dataset1027.db'}
db = connect(db_settings=db_settings)

all_dataset_names = db.datasets
print('all_dataset_names = ', all_dataset_names)

examples1 = db.get_dataset("udnZ")
print('len(examples1） = ', len(examples1))
print(' \n')

with open('./data/udn_db/dbZ.txt', "w") as target:
    for i in range(len(examples1)):
        #print(examples1[i])
        #print()
        target.write(str(examples1[i])+'\n')
    target.close()


