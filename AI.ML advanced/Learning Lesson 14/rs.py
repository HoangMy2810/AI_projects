import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

data = pd.read_csv("movies.csv", encoding="latin-1", sep="\t", usecols=["movie_id", "title", "genres"])
data["genres"] = data["genres"].apply(lambda s: s.replace("|", " ").replace("-", ""))
tf = TfidfVectorizer()
tfidf_matrix = tf.fit_transform(data["genres"])
tfidf_matrix = pd.DataFrame(tfidf_matrix.todense(), columns=tf.get_feature_names_out(), index=data["title"])
cosine_result = pd.DataFrame(cosine_similarity(tfidf_matrix), columns=data["title"], index=data["title"])
top_k = 20
test_movie = "Tom and Huck (1995)"


def get_recommendations(title, df, num_movies=10):
    data1 = df.loc[title, :]
    data1 = data1.sort_values(ascending=False)
    return data1[:num_movies].to_frame(name="score")


result = get_recommendations(test_movie, cosine_result, top_k)

print(result)
