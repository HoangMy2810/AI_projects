import numpy as np

data2 = [4, 6, 4, 3, 3, 4, 3, 4, 3, 8]
k = 3
values, counts = np.unique(data2, return_counts=True)
for value, count in zip(values, counts):
    if count > k:
        print(f'{value} ')