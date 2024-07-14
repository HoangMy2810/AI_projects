import os

import pandas as pd
from PIL import Image
import numpy as np
from keras import Sequential
from keras.models import load_model
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from keras.layers import Conv2D, MaxPool2D, Dense, Flatten, Dropout, MaxPooling2D, BatchNormalization
from matplotlib import pyplot as plt

data = []
labels = []
cur_path = os.getcwd()

#Xu ly tap du lieu
for i in range(43):
    path = os.path.join(cur_path, 'GTSRB\\train', str(i))
    images = os.listdir(path)

    for x in images:
        try:
            image = Image.open(path + '\\' + x)
            image = image.resize((30, 30))
            image = np.array(image)
            data.append(image)
            labels.append(i)
        except:
            print("Lỗi không load được ảnh")
data = np.array(data)
labels = np.array(labels)

#Phan chia du lieu 80-20
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

#Ma hoa cac nhan
y_train = to_categorical(y_train, 43)
y_test = to_categorical(y_test, 43)

#Xay dung mo hinh
filter_size = (3,3)
pool_size = (2,2)

model = Sequential()
model.add(Conv2D(16, filter_size, activation='relu', input_shape=X_train.shape[1:], padding='same'))
model.add(BatchNormalization())
model.add(Conv2D(16, filter_size, activation='relu', padding='same'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=pool_size))
model.add(Dropout(rate=0.2))
model.add(Conv2D(32, filter_size, activation='relu', padding='same'))
model.add(BatchNormalization())
model.add(Conv2D(32, filter_size, activation='relu', padding='same'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=pool_size))
model.add(Dropout(rate=0.2))
model.add(Conv2D(64, filter_size, activation='relu', padding='same'))
model.add(BatchNormalization())
model.add(Conv2D(64, filter_size, activation='relu', padding='same'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=pool_size))
model.add(Dropout(rate=0.2))
model.add(Flatten())
model.add(Dense(2048, activation='relu'))
model.add(Dropout(rate=0.3))
model.add(Dense(1024, activation='relu'))
model.add(Dropout(rate=0.3))
model.add(Dense(128, activation='relu'))
model.add(Dropout(rate=0.3))
model.add(Dense(43, activation='softmax'))

#compile mo hinh
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

#huan luyen mo hinh
history = model.fit(X_train, y_train, batch_size=16, epochs=10, validation_data=(X_test, y_test))
model.save("traffic_sign_20207644.h5")

#in bieu do accuracy
plt.figure(0)
plt.plot(history.history['accuracy'], label='training accuracy')
plt.plot(history.history['val_accuracy'], label='val accuracy')
plt.title('Accuracy')
plt.xlabel('epochs')
plt.ylabel('accuracy')
plt.legend()
plt.show()

plt.figure(1)
plt.plot(history.history['loss'], label='training loss')
plt.plot(history.history['val_loss'], label='val loss')
plt.title('Loss')
plt.xlabel('epochs')
plt.ylabel('loss')
plt.legend()
plt.show()

from sklearn.metrics import accuracy_score

y_test = pd.read_csv('Test.csv')

labels = y_test["ClassId"].values
imgs = y_test["Path"].values

data=[]

for img in imgs:
    image = Image.open(img)
    image = image.resize((30,30))
    data.append(np.array(image))

X_test=np.array(data)

pred = model.predict_classes(X_test)

#Accuracy with the test data
from sklearn.metrics import accuracy_score
print(accuracy_score(labels, pred))