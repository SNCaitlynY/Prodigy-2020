from parse_cat import get_cat

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
print(cats)
print()

catid_list = cats.keys()
print(catid_list)
print()

total_count = 0
total_matches = 0
for catid in catid_list:
    file_name = catid + '.txt'
    with open('./data/udn_result/' + file_name, 'r') as f:
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

    # match rate by percentage, ex: 72.4%
    rate = matches/count*100
    print('{}){:10s}={:,}/{:,}   rate={:.1f}%'.format(catid, cats[catid], matches, count, rate))
    total_count += count
    total_matches += matches

total_rate = total_matches/total_count

print('\ntotal_matches = {:,}'.format(total_matches))
print('total_count = {:,}'.format(total_count))
print('\ntotal_rate = {:.1f}%'.format(total_rate))