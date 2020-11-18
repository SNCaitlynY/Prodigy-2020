"""
udn data utility
2020.7.27
"""
import json

import numpy as np
import regex
from prodigy.components.loaders import JSONL
from sklearn.utils import shuffle

"""
get Udn data category and make them dictionary, such as
{'0': '品牌專館', '1': '快速到貨', ....}

don't use L, W, X
"""
def get_cats():
    cats = {}
    with open('./data/Cate.txt', 'r') as f:
        for i in range(23):
            line = f.readline()
            index = line[2]

            # cut before
            line = line[7:]
            cut_after = regex.search('[|][#][#]', line)
            # cut after
            match = line[: cut_after.start()]

            cats[index] = match
    return cats

"""
assign id to evey udn data so that we can shuffle it and sample it.
warning! This function should only be executed once.
"""
def assign_id_to_udn_data():
    source_dir = 'udn_result'
    target_dir = 'udn_data_with_id'
    cats = get_cats()
    catid_list = cats.keys()

    id = 0
    for catid in catid_list:
        file_name = catid + '.txt'
        stream = JSONL('./data/udn_result/' + file_name)

        with open('./data/udn_data_with_id/' + file_name, 'w', encoding='utf8') as target:
            for title in strfeam:
                title['id'] = id
                json.dump(title, target, ensure_ascii=False)
                target.write('\n')
                id += 1
            target.close()
    return

def shuffle_ids():
    cats = get_cats()
    for catid in cats:
        source_file = catid + '.txt'
        stream = JSONL('./data/udn_data_with_id/' + source_file)
        ids = []

        for line in stream:
            ids.append(line['id'])

        # convert list to numpy array for shuffle use
        ids = np.array(ids)
        ids = shuffle(ids, random_state=0)

        target_file = './data/udn_data_shuffle/shuffle_' + catid + '.txt'
        with open(target_file, "w") as target:
            for id in ids:
                #print(str(id))
                target.write(str(id) + '\n')
            target.close()
    return


def prepare_annotation_sample_file():
    # set 3 paramters
    catid = 'G'
    begin = 0
    samples_number = 2396
    end = samples_number - begin

    source_file = './data/udn_data_with_id/' + catid + '.txt'
    stream = JSONL(source_file)

    sample_ids = []
    shuffle_file = './data/udn_data_shuffle/shuffle_' + catid + '.txt'
    with open(shuffle_file, 'r') as f:
        line = f.readline()
        while line:
            id = int(line)
            sample_ids.append(id)
            line = f.readline()
        f.close()

    print('total samples: len(sample_ids) =', len(sample_ids))

    #sampling
    sample_ids = sample_ids[begin:end]
    print('after sampling: len(sample_ids) =', len(sample_ids))
    print()

    target_file = './data/udn_data_jsonl_prepare/udn_' + catid + '.jsonl'
    with open(target_file, 'w', encoding='utf8') as target:
        for title in stream:
            id = title['id']
            if id in sample_ids:
                sample = {}
                sample['text'] = title['Name']
                sample['id'] = id
                print(sample)
                json.dump(sample, target, ensure_ascii=False)
                target.write('\n')
        target.close()

    return



#assign_id_to_udn_data()
#shuffle_ids()
prepare_annotation_sample_file()
