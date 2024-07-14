import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
import re
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from imblearn.over_sampling import SMOTEN
from sklearn.feature_selection import SelectKBest, chi2


def format_string(x):
    result = re.findall("\,\s[A-Z]{2}$", x)
    if len(result) > 0:
        return result[0][2:]
    return x


data = pd.read_excel("final_project.ods", engine="odf", dtype=str)
data["location"] = data["location"].apply(format_string)

data = data.dropna(subset=['description'])

target = "career_level"
x = data.drop(target, axis=1)
y = data[target]

# stratify=y: phân chia đúng 80-20

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=100, stratify=y)
ros = SMOTEN(random_state=42, sampling_strategy={"director_business_unit_leader": 500, "specialist": 500,
                                                 "managing_director_small_medium_company": 500}, k_neighbors=2)
x_train, y_train = ros.fit_resample(x_train, y_train)

preprocessor = ColumnTransformer(transformers=[
    ("title_feature", TfidfVectorizer(), "title"),
    ("location_feature", OneHotEncoder(handle_unknown="ignore"), ["location"]),
    ("description_feature", TfidfVectorizer(ngram_range=(1, 2), stop_words="english", min_df=0.01, max_df=0.95)
     , "description"),
    ("function_feature", OneHotEncoder(handle_unknown="ignore"), ["function"]),
    ("industry_feature", TfidfVectorizer(), "industry"),
])

cls = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('feature_selection', SelectKBest(chi2, k=500)),
    ('model', RandomForestClassifier())
])
params = {
    "model__n_estimators": [50, 100, 200],
    # "model__criterion": ["entropy", "gini", "log_loss"],
    "feature_selection__k": [i*100 for i in range(1, 11)],
}
grid_reg = GridSearchCV(cls, param_grid=params, cv=6, verbose=2, scoring="f1_weighted", n_jobs=-1)
grid_reg.fit(x_train, y_train)
print(grid_reg.best_params_)
print(grid_reg.best_score_)

# result = cls.fit_transform(x_train)
# print(result.shape)

# cls.fit(x_train, y_train)
y_predict = cls.predict(x_test)
print(classification_report(y_test, y_predict))