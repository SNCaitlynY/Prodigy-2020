import os
import pandas as pd
import json
import re
import timeit

path = "./"
fileList = os.listdir(path)
r = re.compile(".*dat")
DBlist = list(filter(r.match, fileList))
#DBlist = ['1.dat']
frequency_list = []

word_file = "main.txt.dic"
words = open(word_file, encoding="utf-8").readlines()
word_list_frequency = {}
cur_post = ""
temp_word_list = {}
for w in words:
    word = w.replace("\n", "")
    word_post = word[-1]
    if word_post != cur_post:
        if cur_post != "":
            word_list_frequency[cur_post] = temp_word_list
        cur_post = word_post
        temp_word_list = {}
        temp_word_list[word] = [len(word), 0]
    else:
        temp_word_list[word] = [len(word), 0]
word_list_frequency[cur_post] = temp_word_list
start = timeit.default_timer()
for DB in DBlist:
    
    word_to_name = {}
    file = open(DB, encoding="utf-8")
    preProcess = file.readline()
    data = preProcess.replace("\n", "").replace("false", "False").replace("False", "\"False\"").replace("true", "\"True\"").replace("True", "True").replace("None", "\"True\"").replace("null", "\"\"")
    js = json.loads(json.dumps(eval(data)))
    names = []
    hits = js['hits']['hits']
    for h in hits:
        names.append(h['_source']['name'])
    name_index = 0
    for name in names:
        for w in name:
            if w in word_to_name:
                word_to_name[w].add(name_index)
            else:
                word_to_name[w] = set(str(name_index))
        name_index += 1
    midtime = timeit.default_timer()
    for key in word_list_frequency:
        if key in word_to_name:
            for name_id in word_to_name[key]:
                for m in re.finditer(key, names[int(name_id)]):
                    key_index = m.start()
                    for words_num in range(1, 5):
                        word_to_check = names[int(name_id)][key_index-words_num+1:key_index+1]
                        if word_to_check in word_list_frequency[key]:
                            #print(word_to_check, names[int(name_id)])
                            word_list_frequency[key][word_to_check][1] += 1

total_list = []
for key in word_list_frequency:
    for w_key in word_list_frequency[key]:
        total_list.append([w_key, word_list_frequency[key][w_key][1]]) 
sorted_total_list = sorted(total_list, key = lambda s: s[1], reverse = True)
list_to_dict = {}
index = 0
for i in sorted_total_list:
    list_to_dict[index] = {'詞' : i[0], '頻率' : i[1]}
    index += 1

total_df = pd.DataFrame.from_dict(list_to_dict, "index")

csv_file = "frequency.csv"
total_df.to_csv(csv_file, encoding = 'utf_8_sig', index = False)

stop = timeit.default_timer()
print("Done all!")
print("Total Time: ", '%.3f' % (stop - start), "s")
