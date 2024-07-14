import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

df = pd.read_csv(filepath_or_buffer="train.csv", header=0)
df = df[['PassengerId', 'Survived', 'Pclass', 'Sex','Age', 'SibSp', 'Parch', 'Fare']]
#print(tabulate(df, headers="keys", tablefmt="psql"))

#remove Nan values
print("Original length of Dataframe: {}".format(len(df)))
df.dropna(inplace=True)
print("Length of Dataframe after removing Nan value: {}".format(len(df)))

# attribute construction
df['num_family_member'] = df['SibSp'] + df['Parch']
df.drop(['SibSp', 'Parch'], axis=1, inplace=True)

# convert gender to number
df.replace("male", "1", inplace=True)
df.replace("female", "0", inplace=True)
print(tabulate(df, headers="keys", tablefmt="psql"))

# Visualization
#sns.histplot(data=df['Age'])
#plt.title("Age of Passengers")
#plt.xlabel("Age")
#plt.ylabel("Count")
#plt.show()

# Training process

feature_variable = df[['PassengerId', 'Pclass', 'Sex', 'Age', 'Fare', 'num_family_member']]
output_variable = df["Survived"]

#Training set
X_train = feature_variable[:int(0.8*len(df))]
Y_train = output_variable[:int(0.8*len(df))]

#Test set
X_test = feature_variable[int(0.8*len(df)):]
Y_test = output_variable[int(0.8*len(df)):]

#tieu chuan hoa du lieu
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

#khai bao su dung ML model (KNN)
knn = KNeighborsClassifier(n_neighbors=5)

# Huan luyen model
knn.fit(X=X_train, y=Y_train)

# Kiem tra model

Y_prediction = knn.predict(X=X_test)
accuracy = accuracy_score(y_true=Y_test, y_pred=Y_prediction)
print(accuracy*100)