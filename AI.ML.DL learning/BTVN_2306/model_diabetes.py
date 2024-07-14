import pandas as pd
from sklearn.linear_model import LogisticRegressionCV, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from tabulate import tabulate
from imblearn.over_sampling import RandomOverSampler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

df = pd.read_csv(filepath_or_buffer="diabetes.csv", header=0)
#print(tabulate(df, headers="keys",tablefmt="psql"))

#remove 0 values
df = df[['Pregnancies', 'Glucose', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome']]
df = df[(df['BMI'] > 0)]
# df.loc[df['BloodPressure'] == 0, 'BloodPressure'] = df['BloodPressure'].mean()
# df.loc[df['SkinThickness'] == 0, 'SkinThickness'] = df['SkinThickness'].mean()
# df.loc[df['BMI'] == 0, 'BMI'] = df['BMI'].mean()
# print("Length of Dataframe after removing Nan value: {}".format(len(df)))


#visualization
# fig, axs = plt.subplots(4, 2, figsize=(15,12))
# axs = axs.flatten()
# sns.distplot(df['Pregnancies'],rug=True, ax=axs[0])
# sns.distplot(df['Glucose'],rug=True,ax=axs[1])
# sns.distplot(df['BloodPressure'],rug=True,ax=axs[2])
# sns.distplot(df['SkinThickness'],rug=True,ax=axs[3])
# sns.distplot(df['Insulin'],rug=True,ax=axs[4])
# sns.distplot(df['BMI'],rug=True,ax=axs[5])
# sns.distplot(df['DiabetesPedigreeFunction'],rug=True,ax=axs[6])
# sns.distplot(df['Age'],rug=True,ax=axs[7])
# plt.show()

#Check imbalanced data
# outcome_0 = df['Outcome'].value_counts()[0]
# print(outcome_0) #358
# print(len(df) - outcome_0) #179

#Training process
feature_variable = df[['Pregnancies','Glucose','Insulin','BMI','DiabetesPedigreeFunction','Age']]
target_variable = df['Outcome']

#Balanced data
ros = RandomOverSampler(random_state=42)
balanced_feature_variable, balanced_target_variable = ros.fit_resample(feature_variable, target_variable)


#Training set
X_train = feature_variable[:int(0.7*len(df))]
Y_train = target_variable[:int(0.7*len(df))]

#Test set
X_test = feature_variable[int(0.7*len(df)):]
Y_test = target_variable[int(0.7*len(df)):]

#standarded data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

#KNN Model
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X=X_train, y=Y_train)
Y_prediction = knn.predict(X=X_test)
accuracy = accuracy_score(y_true=Y_test, y_pred=Y_prediction)
print(f"KNN: {accuracy * 100}")

#Naive Bayes
gnb = GaussianNB()
gnb.fit(X=X_train, y=Y_train)
Y_prediction = gnb.predict(X_test)
accuracy = accuracy_score(y_true=Y_test, y_pred=Y_prediction)
print(f"Naive Bayes: {accuracy * 100}")

#Logistic Regression
lr = LogisticRegression()
lr.fit(X=X_train, y=Y_train)
Y_prediction = lr.predict(X_test)
accuracy = accuracy_score(Y_test, Y_prediction)
print(f"Logistic Regression: {accuracy * 100}")

#Random Forest Classifier
clf = RandomForestClassifier()
clf.fit(X_train, Y_train)
Y_prediction = clf.predict(X_test)
accuracy = accuracy_score(Y_test, Y_prediction)
print(f"Random Forest Classifier: {accuracy * 100}")

#Gradient Boosting Algorithm
gbc=GradientBoostingClassifier()
gbc.fit(X_train, Y_train)
Y_prediction = gbc.predict(X_test)
accuracy = accuracy_score(Y_test, Y_prediction)
print(f"Gradient Boosting Algorithm: {accuracy * 100}")