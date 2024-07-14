import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.ensemble import RandomForestRegressor


def create_ts_data(data, target, window_size = 5):
    i = 1
    while i < window_size:
        data["co2_{}".format(i)] = data["co2"].shift(-i)
        i += 1
    data[target] = data["co2"].shift(-i)
    data = data.dropna(axis=0)
    return data


target = "target"
window_size = 5
data = pd.read_csv("co2.csv")
data["time"] = pd.to_datetime(data["time"])
data["co2"] = data["co2"].interpolate()

data = create_ts_data(data, target, window_size)
x = data.drop([target, "time"], axis=1)
y = data[target]
training_ratio = 0.8
x_train = x[:int(len(x) * training_ratio)]
y_train = y[:int(len(x) * training_ratio)]
x_test = x[int(len(x) * training_ratio):]
y_test = y[int(len(x) * training_ratio):]

reg = LinearRegression()
reg.fit(x_train, y_train)
y_predict = reg.predict(x_test)

print("MSE {}".format(mean_squared_error(y_test, y_predict)))
print("MAE {}".format(mean_absolute_error(y_test, y_predict)))
print("R2 {}".format(r2_score(y_test, y_predict)))

fig, ax = plt.subplots()
ax.plot(data["time"][:int(len(x) * training_ratio)], data["co2"][:int(len(x) * training_ratio)])
ax.plot(data["time"][int(len(x) * training_ratio):], data["co2"][int(len(x) * training_ratio):])
ax.plot(data["time"][int(len(x) * training_ratio):], y_predict, label="prediction")
ax.set_xlabel("Year")
ax.set_ylabel("CO2")
ax.legend()
plt.show()