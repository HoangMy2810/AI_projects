import csv
with open("cities_population.csv", "r") as file_csv:
    data = list(csv.reader(file_csv, delimiter=','))
file_csv.close()

list_population = []
for row in data[1:]:
    idx = str(row[0]).replace('.', '')
    a = float(str(row[2]).replace(',', ''))
    list_population.append({
        "idx": idx,
        "population": a
    })
list_population.sort(key=lambda x: x["population"], reverse=True)

list_area = []
for row in data[1:]:
    idx = str(row[0]).replace('.', '')
    if idx != '63':
        a = float(str(row[3]).replace(',', ''))
        list_area.append({
            "idx": idx,
            "area": a
         })
list_area.sort(key=lambda x: x['area'], reverse=True)
print(list_area)
#Task 1
print('----------Task1----------')
print('10 most populated cities:')
for x in list_population[0: 10]:
    print(data[int(x["idx"])][1], end=', ')
print('\n10 least populated cities:')
for x in list_population[-9:]:
    print(data[int(x["idx"])][1], end=', ')

frequency = {}
for row in data[1:]:
    name = str(row[7]).replace(' *', '')
    frequency[name] = frequency.get(name, 0) + 1

#Task 2
print('\n\n----------Task2----------')
print('Countries have at least 3 cities in list: ')
for name in frequency:
    if frequency[name] >= 3:
        print(name, end=', ')

#Task 3
print('\n\n----------Task3----------')
frequency = sorted(frequency.items(), key=lambda x: x[1], reverse=True) #return a list of tuples, where each tuple contains a key-value
print('Top 5 countries have most cities in list: ')
for name in frequency[:5]:
    print(name[0], end=', ')

#Task 4
print('\n\n----------Task4----------')
print('Cities with population & area are in the Top 20: ')
for x in list_population[:20]:
    idx = x['idx']
    for y in list_area[:20]:
        if y['idx'] == idx:
            print(data[int(idx)][1], end=', ')

#Task 5
print('\n\n----------Task5----------')
print('Population density statistics by country: ')
density = {}
for row in data[1:]:
    name = str(row[7]).replace(' *', '')
    density[name] = density.get(name, 0) + float(str(row[5]).replace(',',''))
#print(density)
for name in density:
    for tuple in frequency:
        if tuple[0] == name:
            density[name] = density[name] // tuple[1]
for name in density:
    print(f'{name} : {density[name]}')

#Task 6
print('\n\n----------Task6----------')
#print(list_population)
#print(frequency)
print(f'City with the largest population of each country:')
idx = 0
while(frequency[idx][1] >= 2 and idx < len(frequency)):
    country = frequency[idx][0]
    for x in list_population:
        if str(data[int(x['idx'])][7]).replace(' *', '') == country:
            city = data[int(x['idx'])][1]
            print(f'{country} : {city}')
            break
    idx += 1
