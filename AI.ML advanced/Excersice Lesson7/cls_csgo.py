import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from lazypredict.Supervised import LazyClassifier
from lightgbm import LGBMClassifier

data = pd.read_excel("csgo.xlsx")
data = data.drop(["team_a_rounds", "team_b_rounds", "date"], axis=1)

target = "result"
x = data.drop(target, axis=1)
y = data[target]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

nominal_feature = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy="most_frequent")),
    ('scaler', OneHotEncoder(sparse_output=False))
])

num_feature = Pipeline(steps=[
    ('scaler', MinMaxScaler())
])

# result = nominal_feature.fit_transform(data[["map"]])
# print(result)

preprocessor = ColumnTransformer(transformers=[
    ("nom_features", nominal_feature, ["map"]),
    ("num_features", num_feature, ["day", "month", "year", "wait_time_s", "match_time_s", "ping", "kills", "assists",
                                   "deaths", "mvps", "hs_percent", "points"]),
])

cls = Pipeline(steps=[
    ('preprocessor', preprocessor),
    #('model', RandomForestClassifier())
])
# result = cls.fit_transform(x_train)

x_train = cls.fit_transform(x_train)
x_test = cls.transform(x_test)
# cls.fit(x_train, y_train)
# y_predict = cls.predict(x_test)
# for i, j in zip(y_predict, y_test):
#     print("Predict: {}. Actual: {}".format(i, j))

# grid_reg = GridSearchCV(cls, param_grid=params, cv=6, verbose=2, scoring="r2", n_jobs=-1)

# clf = LazyClassifier(verbose=0, ignore_warnings=True, custom_metric=None)
# models, predictions = clf.fit(x_train, x_test, y_train, y_test)
# print(models) ==>>> LGBMClassifier

gridParams = {
    'n_estimators': [8,16,24, 100],
    'num_leaves': [6,8,12,16,31], # large num_leaves helps improve accuracy but might lead to over-fitting
    'boosting_type' : ['gbdt', 'dart', 'rf'], # for better accuracy -> try dart
    'max_bin':[255, 510], # large max_bin helps improve accuracy but might slow down training progress
    'random_state' : [500],
    }
grid_reg = GridSearchCV(LGBMClassifier(), param_grid=gridParams, cv=6, verbose=2, scoring="f1", n_jobs=-1)
grid_reg.fit(x_train, y_train)
y_predict = grid_reg.predict(x_test)
# for i, j in zip(y_predict, y_test):
#     print("Predict: {}. Actual: {}".format(i, j))

print(classification_report(y_test, y_predict, average='macro'))

