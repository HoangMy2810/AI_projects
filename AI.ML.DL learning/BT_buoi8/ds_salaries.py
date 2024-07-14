import pandas as pd

data = pd.read_csv("ds_salaries.csv")
data['salary'] = data['salary'].astype(int)
data['salary_in_usd'] = data['salary_in_usd'].astype(int)
data['remote_ratio'] = data['remote_ratio'].astype(int)

#Task 1
print('----------Task1----------')

mean_salary_by_job = data.groupby('job_title')['salary_in_usd'].mean()
print(mean_salary_by_job.nlargest(1))

#Task 2
print('\n\n----------Task2----------')
mean_DS_salary = data[data['job_title'] == 'Data Scientist'].groupby('employee_residence')['salary_in_usd'].mean()
print(mean_DS_salary.nlargest(1))

#Task 3
print('\n\n----------Task3----------')
US_data = data[data['company_location'] == 'US']
condition = US_data['employee_residence'] == 'US'
mean_US_salary = US_data.loc[condition, 'salary_in_usd'].mean()
condition = US_data['employee_residence'] != 'US'
mean_forginer_salary = US_data.loc[condition, 'salary_in_usd'].mean()
print(mean_forginer_salary > mean_US_salary)

#Task 4
print('\n\n----------Task4----------')

condition = data['job_title'] == 'Data Engineer' & data['experience_level'] == 'SE' \
            & data['company_location'] == 'US' & (data['company_size'] == 'M' | data['company_size'] == 'S')
print(condition)

