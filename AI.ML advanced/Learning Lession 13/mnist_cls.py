import numpy as np

with np.load("mnist.npz") as f:
    x_train = f["x_train"]
    y_train = f["y_train"]
    x_test = f["x_test"]
    y_test = f["y_test"]

x_train = np.reshape(x_train, (x_train.shape[0], -1))
x_test = np.reshape(x_test, (x_test.shape[0], -1))
y_train = np.reshape(y_train, (y_train.shape[0], -1))
y_test = np.reshape(y_test, (y_test.shape[0], -1))
print(x_train.shape)
print(x_test.shape)



