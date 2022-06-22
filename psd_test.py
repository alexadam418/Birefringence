import numpy as np
from data_processing import find_r

file_data = open(r"/home/alexadam/testdata/data_test.txt", "r")
data = np.array(file_data.read().split(" "), float)
test = find_r(data, 210000, 2)
print(test)


