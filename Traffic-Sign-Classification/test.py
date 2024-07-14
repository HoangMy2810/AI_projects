import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from PIL import Image
from keras.models import load_model

y_test = pd.read_csv('GTSRB/Test.csv')

labels = y_test["ClassId"].values
imgs = y_test["Path"].values
model = load_model('traffic_sign_20207644.h5')
data=[]

for img in imgs:
    image = Image.open('GTSRB/' + img)
    image = image.resize((30,30))
    data.append(np.array(image))

X_test=np.array(data)
pred = np.argmax(model.predict(X_test), axis=-1)

#Tinh accuracy
from sklearn.metrics import accuracy_score
print(accuracy_score(labels, pred))

