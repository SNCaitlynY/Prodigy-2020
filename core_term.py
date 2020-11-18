def get_core_terms():
    with open('./data/coreterm2.txt', 'r') as fp:
        line = fp.readline()
        core =[]
        while line:
            c = line.split()
            core.append(c[0])
            line = fp.readline()
        print(len(core))
    return core

core = get_core_terms()

text = '日本Sastty 利尻昆布染髮護色乳(黑/咖啡/深褐)'
for term in core:
    start = text.find(term)
    if start != -1:
        break
if start != -1:
    end = start + len(term)
    print('term = {}, start = {}, end = {}', term)
