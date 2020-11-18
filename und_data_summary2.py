from os import listdir
from parse_cat import get_cat

cats = get_cat()
print(cats)
print(len(cats))
print()

catid_list = cats.keys()

total = 0
for catid in catid_list:
    file_name = catid + '.txt'
    with open('./data/udn_result/' + file_name, 'r') as f:
        count = 0
        line = f.readline()
        # print(line)
        while line:
            # print(line)
            count += 1
            line = f.readline()

    print('{}){:10s}={:,}'.format(catid, cats[catid], count))
    total += count

print('\ntotal = {:,}'.format(total))