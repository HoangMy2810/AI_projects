import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
data = pd.read_csv("diabetes.csv")
#data.hist()
#data.plot(kind="density", subplots=True, layout=(3,3), sharex=False)
sn.heatmap(data.corr(), annot=True, color="YlGn")
plt.show()