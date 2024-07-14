import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


def create_ts_data(data, target, window_size, target_size):
    i = 1
    while i < window_size:
        data["co2_{}".format(i)] = data["co2"].shift(-i)
        i += 1

    i = 0
    while i < target_size:
        data["{}_{}".format(target, i)] = data["co2"].shift(-i-window_size)
        i += 1
    data = data.dropna(axis=0)
    return data


target = "target"
window_size = 10
target_size = 6
data = pd.read_csv("co2.csv")
data["time"] = pd.to_datetime(data["time"])
data["co2"] = data["co2"].interpolate()

data = create_ts_data(data, target, window_size, target_size)
target_names = ["{}_{}".format(target, i) for i in range(target_size)]
x = data.drop(target_names + ["time"], axis=1)
y = data[target_names]

training_ratio = 0.8
x_train = x[:int(len(x) * training_ratio)]
y_train = y[:int(len(x) * training_ratio)]
x_test = x[int(len(x) * training_ratio):]
y_test = y[int(len(x) * training_ratio):]

regs = [LinearRegression() for _ in range(target_size)]
for i, reg in enumerate(regs):
    reg.fit(x_train, y_train["{}_{}".format(target, i)])
    y_predict = reg.predict(x_test)
    print("MSE {}".format(mean_squared_error(y_test["{}_{}".format(target, i)], y_predict)))
    print("MAE {}".format(mean_absolute_error(y_test["{}_{}".format(target, i)], y_predict)))
    print("R2 {}".format(r2_score(y_test["{}_{}".format(target, i)], y_predict)))

# fig, ax = plt.subplots()
# ax.plot(data["time"][:int(len(x) * training_ratio)], data["co2"][:int(len(x) * training_ratio)])
# ax.plot(data["time"][int(len(x) * training_ratio):], data["co2"][int(len(x) * training_ratio):])
# ax.plot(data["time"][int(len(x) * training_ratio):], y_predict, label="prediction")
# ax.set_xlabel("Year")
# ax.set_ylabel("CO2")
# ax.legend()
# plt.show()
