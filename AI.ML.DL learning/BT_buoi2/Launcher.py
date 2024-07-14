based_salary = int(input())
age = int(input())
married = int(input())
num_children = int(input())

tax_married = 0
if married == 1:
    tax_married = based_salary * 0.05
elif married == 2:
    tax_married = based_salary * 0.03
else:
    tax_married = based_salary * 0.02

tax_children = 0
if num_children == 1:
    tax_children = based_salary * 0.03
elif num_children == 2:
    tax_children = based_salary * 0.05
else:
    tax_children = based_salary * 0.05 + based_salary * 0.01 * (num_children - 2)

#Tiền lương trước thuế 10 triệu trở xuống được miễn thuế
tax_salary = 0

#trên 10 triệu đến dưới 20 triệu chịu thuế 10%
if based_salary > 10 and based_salary < 20:
    tax_salary = based_salary * 0.1

#từ 20 triệu trở lên chịu thuế lũy tiến 0.1% cho mỗi 1 triệu, nhưng tối đa ko vượt quá 5%
elif based_salary >= 20:
    tax_salary = based_salary * 0.1
    if (based_salary - 20) * 0.001 < 0.05:
        tax_salary += (based_salary - 20) * 0.001
    else:
        tax_salary += based_salary * 0.05


if age >= 18 and age <= 30:
    tax_age = based_salary * 0.06
elif age >= 31 and age <= 45:
    tax_age = based_salary * 0.09
elif age >= 46 and age <= 60:
    tax_age = based_salary * 0.09 - based_salary * (age - 45) * 0.001
else:
    tax_age = based_salary * 0.04

print(based_salary + tax_married - tax_children + tax_salary + tax_age)





