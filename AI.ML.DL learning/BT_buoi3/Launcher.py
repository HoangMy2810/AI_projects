with open(file="Iris.csv", mode="r") as file_csv:
    data = file_csv.readlines()
file_csv.close()


#BAI 1a, 2a
print('----------1a, 2a----------')
sum_len, sum_wid = 0, 0
max_len, max_wid = 0, 0
for row in data[1:51]:
    text = str(row).split(sep=",")
    sum_len += float(text[1])
    sum_wid += float(text[2])
    max_len = max(max_len, float(text[1]))
    max_wid = max(max_wid, float(text[2]))
print(f'Average length, average width of Iris_setosa: {round(sum_len/50, 2)}, {round(sum_wid / 50, 2)}')
print(f'Max length, average width of Iris_setosa: {round(max_len, 2)}, {round(max_wid, 2)}')

sum_len, sum_wid = 0, 0
max_len, max_wid = 0, 0
for row in data[51:101]:
    text = str(row).split(sep=",")
    sum_len += float(text[1])
    sum_wid += float(text[2])
    max_len = max(max_len, float(text[1]))
    max_wid = max(max_wid, float(text[2]))
print(f'Average length, average width of Iris_virginiaca: {round(sum_len/50, 2)}, {round(sum_wid / 50, 2)}')
print(f'Max length, average width of Iris_virginiaca: {round(max_len, 2)}, {round(max_wid, 2)}')

sum_len, sum_wid = 0, 0
max_len, max_wid = 0, 0
for row in data[101:]:
    text = str(row).split(sep=",")
    sum_len += float(text[1])
    sum_wid += float(text[2])
    max_len = max(max_len, float(text[1]))
    max_wid = max(max_wid, float(text[2]))
print(f'Average length, average width of Iris_versicolor: {round(sum_len/50, 2)}, {round(sum_wid / 50, 2)}')
print(f'Max length, average width of Iris_versicolor: {round(max_len, 2)}, {round(max_wid, 2)}')

#BAI 3a
print('----------3a----------')
#len_input = float(input("Enter sepal length of your flower: "))
len_input = 3
#wid_input = float(input("Enter sepal width of your flower: "))
wid_input = 2
min_distance = 100000
name = ""
for row in data[1:]:
    text = str(row).split(sep=",")
    curr_distance = ((len_input - float(text[1])) ** 2 + (wid_input - float(text[2])) ** 2) ** 0.5
    if(min_distance > curr_distance):
        min_distance = curr_distance
        name = text[5]
print(f'That flower is {name}')

#Bai 1b
print('----------1b----------')
len_setosa = []
for row in data[1:51]:
    text = str(row).split(sep=",")
    len_setosa.append(float(text[1]))
len_setosa.sort(reverse=True)
ten_max = []
len_prev = 0
count = 0
idx = 0
while (idx < len(len_setosa) and count < 10):
    if len_setosa[idx] != len_prev:
        len_prev = len_setosa[idx]
        ten_max.append(len_prev)
        count += 1
    idx += 1
print(f'10 largest sepal length of Iris_setosa: {ten_max}')

#Bai 2b
print('----------2b----------')
data_arr = []
for row in data[1:]:
    data_arr.append(str(row).split(sep=","))
data_arr.sort(key=lambda x: (x[1]+x[2]), reverse=True)
count_vir, count_seto, count_versi = 0, 0, 0
for row in data_arr[:50]:
    name = row[5]
    if name == 'Iris-virginica\n':
        count_vir += 1
    elif name == 'Iris-versicolor\n':
        count_versi += 1
    else:
        count_seto += 1
print(f'Top 50 largest flower include: {count_seto} iris_setosa,'
      f' {count_vir} iris_virginica, {count_versi} iris_versicolor')

#Bai 3b
print('----------3b----------')
len_input = float(input("Enter sepal length of your flower: "))
wid_input = float(input("Enter sepal width of your flower: "))
distance = []
for row in data[1:]:
    text = str(row).split(sep=",")
    curr_distance = ((len_input - float(text[1])) ** 2 + (wid_input - float(text[2])) ** 2) ** 0.5
    distance.append({
        "name": text[5],
        "value": curr_distance
    })
distance.sort(key=lambda x: x["value"])

#3b.a
print('----------3b.a----------')
idx = 2
if distance[0]["name"] != distance[1]["name"] and distance[0]["value"] == distance[1]["value"]:
    if distance[2]["name"] == distance[0]["name"]:
        print(f'That flower is: {distance[0]["name"]}')
    elif distance[2]["name"] == distance[1]["name"]:
        print(f'That flower is: {distance[1]["name"]}')
    else:
        print(f'That flower is: {distance[3]["name"]}')
else:
    print(f'That flower is: {distance[0]["name"]}')

#3b.b
print('----------3b.b----------')
count_iris = {}
count_iris['Iris-setosa'] = 0
count_iris['Iris-virginica'] = 0
count_iris['Iris-versicolor'] = 0
for x in distance[:7]:
    name = x['name'].replace('\n', '')
    count_iris[name] += 1
count_iris = sorted(count_iris.items(), key=lambda x: x[1], reverse=True)
#print(count_iris)
idx = 7
while(count_iris[0][1] == count_iris[1][1]):
    name = distance[idx]['name'].replace('\n', '')
    count_iris[name] += 1
    count_iris = sorted(count_iris.items(), key=lambda x: x[1], reverse=True)
    idx += 1
print(f'That flower is: {count_iris[0][0]}')
'''Sửa theo hướng: chỉ xét 7 bông gần nhất, 2 if?
    chạm 4 -> in ?
    2 biến chạm 3 -> in ko thuộc?
    1 biến chạm 3 -> in ?  '''
#3b.c
print('\n----------3b.c----------')
count_seto, count_vir, count_versi = 0, 0, 0
idx = 0
while distance[idx]["value"] <= 0.2:
    if distance[idx]["name"] == 'Iris-virginica\n':
        count_vir += 1
    elif distance[idx]["name"] == 'Iris-versicolor\n':
        count_versi += 1
    else:
        count_seto += 1
    idx += 1
if count_seto > max(count_versi, count_vir):
    print(f'That flower is: Iris setosa')
elif count_vir > max(count_versi, count_seto):
    print(f'That flower is: Iris virginica')
elif count_versi > max(count_seto, count_vir):
    print(f'That flower is: Iris versicolor')
else:
    print('That flower doesnt belong to any class')