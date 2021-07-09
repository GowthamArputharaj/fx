import pandas as pd
import numpy as np


from scipy.signal import argrelmin, argrelmax

from scipy.signal import argrelextrema
import matplotlib.pyplot as plt

data = np.random.randint(3, 40, 20)

def fun():
	return 'Hleo world'

# max_idx = list(argrelmax(data, order=1)[0])
# min_idx = list(argrelmin(data, order=1)[0])


max_idx = list(argrelextrema(data, np.greater, order=1)[0])
min_idx = list(argrelextrema(data, np.less, order=1)[0])


idx = max_idx + min_idx

idx.sort()

peaks = data[idx]

max_idx.sort()
min_idx.sort()

plt.plot(data, color="blue")
plt.scatter(min_idx, data[min_idx], color="green")
plt.scatter(max_idx, data[max_idx], color="red")

# plt.scatter(idx, peaks, c='r')
plt.show()


















