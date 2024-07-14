### Email spam Detection ##
"""
Description:
              Email spam detection system is used to detect email spam using Machine Learning technique called Natural Language Processing and Python,
              where we have a dataset contain a lot of emails by extract important words and then use naive classifier we can detect if this email is spam or not.
"""
from __future__ import print_function

import pickle

## Importing modules ##
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import nltk

nltk.download('stopwords')

# Import Google Gmail API
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

## 1 | Data Preprocessing ##
"""Prepare data before training"""

# 1.1 Load dataset
dataset = pd.read_csv('../Dataset/emails.csv')
print(f"Dataset head : \n{dataset.head()}\n")

# 1.2 Check for duplicates and remove them 
dataset.drop_duplicates(inplace=True)

# 1.3 Number of missing data for each column 
print(f"Number of missing data : \n{dataset.isnull().sum()}\n")


# 1.4 Cleaning data from punctuation and stopwords and then tokenizing it into words (tokens)
def process(text):
    nopunc = [char for char in text if char not in string.punctuation]
    nopunc = ''.join(nopunc)
    clean = [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]
    return clean


print(
    f"Dataset head after cleaning punctuation and stopwords and then tokenizing it into words : \n{dataset['text'].head().apply(process)}\n")

# 1.5 Convert the text into a matrix of token counts
# message = CountVectorizer(analyzer=process).fit_transform(dataset['text'])
# pickle.dump(message, open("Model/vector.pickel", "wb"))    # Save the vectorizer output message
message = pickle.load(open("../Model/vector.pickel", "rb"))  # Load the vectorizer output message

# 1.6 Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(message, dataset['spam'], test_size=0.20, random_state=0)

feature_extraction = TfidfVectorizer(min_df=1, stop_words='english', lowercase='True')


## 2 | Model Creation ##
"""Create model to fit it to the data"""

# 2.1 Create and train the Naive Bayes Classifier
classifier = MultinomialNB().fit(X_train, y_train)


# classifier là một obj.

# 2.2 Classifiers prediction
y_pred = classifier.predict(X_test)
print(f"Prediction results (y_pred): \n{y_pred}\n")

## 3 | Model Evaluation ##
"""Evaluate model performance"""
print(f"Classification report :\n{classification_report(y_test, y_pred)}\n")
print(f"Confusion Matrix :\n{confusion_matrix(y_test, y_pred)}\n")
print(f"Model accuracy : {round(accuracy_score(y_test, y_pred), 2) * 100} %")


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        results2 = service.users().messages().get(userId='tduong.hust02@gmail.com', id='1801999b96c48426').execute()
        objMessage = results2.get('payload').get('headers', [])
        subject = objMessage[20]

        text = subject.get('value')
        print(objMessage)
        print(text)

        # y_pred = classifier.predict()
        # print(f"Prediction results (y_pred): \n{y_pred}\n")

        input_data_features = feature_extraction.transform(text)
        prediction = classifier.predict(input_data_features)
        print(prediction)


    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()
