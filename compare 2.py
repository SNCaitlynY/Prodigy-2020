import os
import pandas as pd
import json

DB_prefix = "db_Z"
DB_file = []
DB_dict = [{}, {}]
DB_file.append(DB_prefix + ".txt")
DB_file.append(DB_prefix + "2.txt")
temp_list = []
csv_df = pd.DataFrame(columns = ['id', 'text', '1版', '2版', '是否相同'])
csv_file = DB_prefix + ".csv"

for f in range(2):
    file = open(DB_file[f], encoding="utf-8")
    preProcess = file.readlines()
    for i in preProcess:
        data = i.replace("\n", "").replace("False", "\"False\"").replace("True", "\"True\"").replace("None", "\"True\"")
        try:
            js = json.loads(json.dumps(eval(data)))
            if 'spans' in js and len(js['spans']) > 0 and 'start' in js['spans'][0] and 'end' in js['spans'][0]:
                DB_dict[f][js['id']] = [js['text'], js['text'][js['spans'][0]['start']:js['spans'][0]['end']]]
            else:
                DB_dict[f][js['id']] = [js['text'], ""]
        except:
            print("This id " + str(js['id']) + " has error in file " + DB_file[f] + ".")
print("Read DB done!")

for key in DB_dict[0]:
    if key in DB_dict[1]:
        if DB_dict[0][key][1] == DB_dict[1][key][1]:
            temp_list.append([key, DB_dict[0][key][0], DB_dict[0][key][1], DB_dict[1][key][1], "O"])
        else:
            temp_list.append([key, DB_dict[0][key][0], DB_dict[0][key][1], DB_dict[1][key][1], "X"])
    else:
        #print("here 1 " + str(key))
        temp_list.append([key, DB_dict[0][key][0], DB_dict[0][key][1], "", "X"])

for key in DB_dict[1]:
    if key not in DB_dict[0]:
        #print("here 2 " + str(key))
        temp_list.append([key, DB_dict[0][key][0], "", DB_dict[1][key][1], "X"])
        
sorted(temp_list, key=lambda x:x[0])
blank1 = 0
blank2 = 0
theSame = 0
for i in temp_list:
    new_row = {'id' : i[0], 'text' : i[1], '1版' : i[2], '2版' : i[3], '是否相同' : i[4]}
    if i[2] == "":
        blank1 += 1
    if i[3] == "":
        blank2 += 1
    if i[4] == "O":
        theSame += 1
    csv_df = csv_df.append(new_row, ignore_index = True)
blank1 = round((blank1 * 100 / len(temp_list)), 2)
blank2 = round((blank2 * 100 / len(temp_list)), 2)
theSame = round((theSame * 100 / len(temp_list)), 2)
blank_row = {'id' : "", 'text' : "未標注", '1版' : str(blank1)+"%", '2版' : str(blank2)+"%", '是否相同' : ""}
csv_df = csv_df.append(blank_row, ignore_index = True)
last_row = {'id' : "", 'text' : "相同率", '1版' : "", '2版' : "", '是否相同' : str(theSame)+"%"}
csv_df = csv_df.append(last_row, ignore_index = True)

csv_df.to_csv(csv_file, encoding = 'utf_8_sig', index = False)
    
