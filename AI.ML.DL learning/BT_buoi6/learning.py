import numpy as np
import pandas as pd

data = pd.read_csv("cities_population.csv")
data['Country'] = data['Country'].str.replace(' *', '')
#Task2
print('----------Task2----------')
country_count = data['Country'].value_counts()
print(country_count[country_count >= 3])

#Task 3
print('\n\n----------Task3----------')
print(country_count.head(5))
print(data)

#Task4
print('\n\n----------Task4----------')
#sap xep dataframe theo cot 'area km2' -> lay ra ten 20 thanh pho dau tien

#1. convert sang so, loai bo dinh dang loi
data['Area KM2'] = pd.to_numeric(data['Area KM2'], errors='coerce')
data = data.dropna(subset=['Area KM2'])
#2. sap xep
data.sort_values(by=['Area KM2'], inplace=True, ascending=False)
city2 = data.head(20)['City']

#sap xep dataframe theo cot 'population' -> lay ra ten 20 thanh pho dau tien
data['Population'] = data['Population'].str.replace(",","")
data['Population'] = data['Population'].astype(int)
data.sort_values(by=['Population'], inplace=True, ascending=False)
city1 = data.head(20)['City']
print(city2)
#in ra giao cua 2 tap
print(city1[city1.isin(city2)])

#Task5
print('\n\n----------Task5----------')
#calculate total area of cities, group by country
sum_area_by_country = data.groupby('Country')['Area KM2'].sum()

#calculate total population of cities, group by country
sum_population_by_country = data.groupby('Country')['Population'].sum()

#calculate density
density_by_country = sum_population_by_country // sum_area_by_country
print(density_by_country)

#Task6
print('\n\n----------Task6----------')
#lay ten cac nuoc xuat hien >= 2 lan
country = country_count[country_count >= 2].keys()

print(data)
for value in country:
    print(value, end='                      ')
    # Find the first index where 'country' appears in dataframe
    first_index = data['Country'].tolist().index(value)
    print(first_index)

    #get city name of row index in dataframe
    city = data.iloc[first_index]['City']
    print(f'{city} \n')

