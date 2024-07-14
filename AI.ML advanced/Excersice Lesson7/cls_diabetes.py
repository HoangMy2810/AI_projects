import pandas as pd
import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt
import seaborn as sn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import GridSearchCV
import pickle
from lazypredict.Supervised import LazyClassifier

data = pd.read_csv("diabetes.csv")
#print(tabulate(data, headers="keys",tablefmt="psql"))

#tao anh
# plt.figure(figsize=(3, 3))
# sn.histplot(data["Outcome"])
# plt.title("Label distribution")
# plt.xticks([0, 1])
# plt.show()
#
# sn.heatmap(data.corr(), annot=True)
# plt.show()

target = "Outcome"
x = data.drop(target, axis=1) #default: axis=0 (loai bo hang)
y = data[target]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
scaler = StandardScaler()

x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

# cls = RandomForestClassifier()
# cls.fit(x_train, y_train)
# y_predict = cls.predict(x_test)
#
# target_names = ['ko bi benh', 'bi benh']
# print(classification_report(y_test, y_predict, target_names=target_names))
#
# #in ra confusion matrix
# cm = np.array(confusion_matrix(y_test, y_predict, labels=[0,1]))
# confusion = pd.DataFrame(cm, index=["Ko bi benh", "Bi benh"], columns=["Ko bi benh", "Bi benh"])
# sn.heatmap(confusion, annot=True, fmt="g")
# plt.savefig("confusion_matrix.png")

# #gridSearch
# params = {
#     "n_estimators": [50, 100, 200],
#     "criterion": ['gini', 'entropy', 'log_loss'],
#     "max_features": ["sqrt", "log2", None]
# }
# cls = GridSearchCV(RandomForestClassifier(), param_grid=params, cv=6, verbose=1, scoring="f1", n_jobs=-1)
# cls.fit(x_train, y_train)
# print(cls.best_estimator_)
# print(cls.best_score_)
# y_predict = cls.predict(x_test)
# target_names = ['ko bi benh', 'bi benh']
# print(classification_report(y_test, y_predict, target_names=target_names))

#lazypredict (sau đó kết hợp với gridsearch)
cls = LazyClassifier(verbose=0, ignore_warnings=True, custom_metric=None)
models, predictions = cls.fit(x_train, x_test, y_train, y_test)
print(models)
