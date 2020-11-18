import os
import pandas as pd
import json
import re

path = "./"
fileList = os.listdir(path)
r = re.compile(".*txt")
DBlist = list(filter(r.match, fileList))

frequency_list = []

for DB in DBlist:
    frequency_dict = {}
    total_dict = {}
    total_list = []
    DB_prefix = DB.split(".")[0]
    categories = DB.split(".")[0].replace("db_", "")
    file = open(DB, encoding="utf-8")
    preProcess = file.readlines()
    for i in preProcess:
        data = i.replace("\n", "").replace("False", "\"False\"").replace("True", "\"True\"").replace("None", "\"True\"")
        try:
            js = json.loads(json.dumps(eval(data)))
            if 'spans' in js and len(js['spans']) > 0 and 'start' in js['spans'][0] and 'end' in js['spans'][0]:
                word = js['text'][js['spans'][0]['start']:js['spans'][0]['end']]
                if word in frequency_dict:
                    frequency_dict[word] += 1
                else:
                    frequency_dict[word] = 1
                if word in total_dict:
                    total_dict[word] += 1
                else:
                    total_dict[word] = 1
        except:
            print("This id " + str(js['id']) + " has error in file " + DB + ".")
    for key in frequency_dict:
        frequency_list.append([frequency_dict[key], key, categories])
    for key in total_dict:
        total_list.append([total_dict[key], key])
    sorted_total_list = sorted(total_list, key = lambda s: s[0], reverse = True)
    csv_file = DB_prefix + ".csv"
    csv_df = pd.DataFrame(columns = ['核心詞', '頻率'])
    number_of_words = 0
    for i in sorted_total_list:
        new_row = {'核心詞' : i[1], '頻率' : i[0]}
        number_of_words += i[0]
        csv_df = csv_df.append(new_row, ignore_index = True)
    new_row = {'核心詞' : "種類", '頻率' : len(sorted_total_list)}
    csv_df = csv_df.append(new_row, ignore_index = True)
    new_row = {'核心詞' : "詞數", '頻率' : number_of_words}
    csv_df = csv_df.append(new_row, ignore_index = True)
    csv_df.to_csv(csv_file, encoding = 'utf_8_sig', index = False)
    
    
sorted_frenquency_list = sorted(frequency_list, key = lambda s: s[0], reverse = True)
total_csv_file = "total" + ".csv"
total_csv_df = pd.DataFrame(columns = ['核心詞', '頻率', '類別'])

number_of_words += i[0]
categories_dict = {}
for i in sorted_frenquency_list:
    new_row = {'核心詞' : i[1], '頻率' : i[0], '類別' : i[2]}
    number_of_words += i[0]
    if i[2] in categories_dict:
        categories_dict[i[2]] += 1
    else:
        categories_dict[i[2]] = 1
    total_csv_df = total_csv_df.append(new_row, ignore_index = True)

categories_list = []
for key in categories_dict:
    categories_list.append([categories_dict[key], key])

sorted_categories_list = sorted(categories_list, key = lambda s: s[0], reverse = True)

sorted_categories_string = sorted_categories_list[0][1] + "->"
for i in range(1, len(sorted_categories_list)):
    sorted_categories_string += sorted_categories_list[i][1]
    if i < len(sorted_categories_list) - 1:
        sorted_categories_string += "->"

new_row = {'核心詞' : "種類", '頻率' : len(sorted_frenquency_list), '類別' : ""}
total_csv_df = total_csv_df.append(new_row, ignore_index = True)
new_row = {'核心詞' : "詞數", '頻率' : number_of_words, '類別' : ""}
total_csv_df = total_csv_df.append(new_row, ignore_index = True)
new_row = {'核心詞' : "類別頻率高->低", '頻率' : sorted_categories_string, '類別' : ""}
total_csv_df = total_csv_df.append(new_row, ignore_index = True)
print(sorted_categories_list)

total_csv_df.to_csv(total_csv_file, encoding = 'utf_8_sig', index = False)

print("Done collecting statistics !")
