"""
prodigy helper for dealing with chinese characters
2020.7.27
"""
import regex

"""
get Udn catelog dictionary, such asdef main
{'0': '品牌專館', '1': '快速到貨', ....}

don't use L, W, X
"""
def get_cat():
    cat = {}
    with open('./data/Cate.txt', 'r') as f:
        for i in range(23):
            line = f.readline()
            index = line[2]

            # cut before
            line = line[7:]
            cut_after = regex.search('[|][#][#]', line)
            # cut after
            match = line[: cut_after.start()]

            cat[index] = match
    return cat

