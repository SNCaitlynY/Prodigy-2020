list1 = []
list2 = []
list3 = []
list4 = []
list5 = []
list6 = []
with open('./data/coreterm.txt', 'r') as f:
    for line in f:
        if len(line) == 7:
            list1.append(line.strip())
        elif len(line) == 6:
            list2.append(line.strip())
        elif len(line) == 5:
            list3.append(line.strip())
        elif len(line) == 4:
            list4.append(line.strip())
        elif len(line) == 3:
            list5.append(line.strip())
        elif len(line) == 2:
            list6.append(line.strip())
        list = list1 + list2 + list3 +list4 + list5 + list6

with open("./data/result.txt", "w") as f:
    for item in list:
        f.writelines(item)
        f.writelines('\n')
    f.close()

print(list)

