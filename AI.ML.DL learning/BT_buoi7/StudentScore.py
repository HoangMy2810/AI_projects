import numpy as np
import pandas as pd

data = pd.read_csv("../../AI.ML advanced/Excersice Lesson7/StudentScore.csv")
data['math score'] = data['math score'].astype(int)
data['reading score'] = data['reading score'].astype(int)
data['writing score'] = data['writing score'].astype(int)

#Task 1
print('----------Task1----------')
#___get index of top 100 math score
data.sort_values(by=['math score'], inplace=True, ascending=False)
top100_math = data.head(100).index
#print(data);
#___get index of top 100 reading score
data.sort_values(by=['reading score'], inplace=True, ascending=False)
top100_reading = data.head(100).index

print(top100_math[top100_reading.isin(top100_math)][:10])

#Task 2
print('\n\n----------Task2----------')
#___get 20 students have highest writing score of each group
top20_writing_group = data.groupby('race/ethnicity')['writing score'].apply(lambda x: x.nlargest(20))
print(top20_writing_group)

#Task 3
print('\n\n----------Task3----------')
#get data only group A
groupA = data[data['race/ethnicity'] == 'group A']

#group 'group A' by parental level of education
groupA_parental_level = groupA.groupby('parental level of education')['race/ethnicity'].count()

print(groupA_parental_level)

'''master's degree: thS
   bachelor's degree: bang cu nhan
   asociate's degree: hoc lien ket (~2 nam)
   some college: da hoc nhung chua TN DH
   high school: tot nghiep thpt
   some high school: da hoc nhung chua TN THPT'''

#Task 4
print('\n\n----------Task4----------')
level_education_sorted = pd.Series(['some high school',  'high school', 'some college',
                                    "associate's degree", "bachelor's degree", "master's degree"])

#___add column 'average_score'
average_score = (data['math score'] + data['reading score'] + data['writing score'])/3
data['average score'] = average_score

#___calculate average score by group and sort
average_score_parental_education = data.groupby('parental level of education')['average score'].mean()
average_score_parental_education = average_score_parental_education.sort_values()

#print(f'{average_score_parental_education}')

#___compare level_education_sorted and index of average_score_group
comparison_result = level_education_sorted.values == average_score_parental_education.index

#___Series.all() returns 'True' if all elements of Series are 'True'
print(comparison_result.all())

#Task 5: similar to Task 6
print('\n\n----------Task5----------')
lunch_quality_sorted = pd.Series(['standard', 'free/reduced'])
average_score_lunch = data.groupby('lunch')['average score'].mean()
average_score_lunch.sort_values()
comparison_result = average_score_lunch.index == lunch_quality_sorted
print(comparison_result.all())

#Task 6
print('\n\n----------Task6----------')
grouped = data.groupby('race/ethnicity')
print(grouped)
math_grouped = grouped['math score'].apply(lambda x: x.nlargest(10))

top10_math_grouped = data.groupby('race/ethnicity')['math score'].apply(lambda x: x.nlargest(10))
print(math_grouped)

#Task 7: Xu hướng mình chưa đưa ra kết luận, chỉ xét xem nhận định đúng hay sai.
print('\n\n----------Task7----------')

grouped = data.groupby(['race/ethnicity', 'parental level of education', 'lunch', 'test preparation course'])['average score'].mean()

#print(grouped)

flag = True #___default: 'The statment is correct'

#___check every 2 groups have same ['race/ethnicity', 'parental level of education', 'lunch']

for idx in range(len(grouped) - 1):
    #get names and values of 2 continuos groups
    name_group_1 = list(grouped.keys())[idx]
    name_group_2 = list(grouped.keys())[idx+1]
    value_group_1 = grouped.iloc[idx]
    value_group_2 = grouped.iloc[idx+1]

    #___if 2 groups have same ['race/ethnicity', 'parental level of education', 'lunch']:
    #___it means test_status of (idx)th group is 'Completed', test_status of (idx+1)th group is 'none'
    if name_group_1[:3] == name_group_2[:3]:
        #___check if average score of 'Completed' < average score of 'None':
        #___it means the statement is Incorrect
        if value_group_1 <= value_group_2:
            #print(name_group_1)
            #print(value_group_1)
            #print(value_group_2)
            flag = False
            break
print(flag)
#print(count)
