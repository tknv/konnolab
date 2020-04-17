import sys
import time
import os
import csv
import numpy as np
import decimal


# 4/16/2020  17:53:46
p='%Y/%m/%d %H:%M:%S'
os.environ['TZ']='UTC'
# np.set_printoptions(threshold=sys.maxsize)
exping_file = sys.argv[1]
with open(file=exping_file, newline='', encoding="utf8") as csvfile:
    ping_result = csv.reader(csvfile)
    result_list = list(ping_result)
    # craft data
    data_len = len(result_list)
    dataset_mod = data_len % 10
    data_list = result_list[dataset_mod:]
    data_set_len = len(data_list)
    m = 0
    data_set=np.empty((data_set_len, 2), dtype=int)
    # print(data_set)
    for datum in data_list:
        if datum[0] in 'ＯＫ':
            data_set[m][0] = 0
            # data_set[m,1] = 0
        else:
            data_set[m][0] = 1
            # data_set[m,1] = 0
        data_set[m][1] = int(time.mktime(time.strptime(datum[1], p)))
        # data_set[m,2] = int(time.mktime(time.strptime(datum[1], p)))
        m += 1
    a = np.array((data_set), dtype=np.dtype(decimal.Decimal))
    print(a)
    # a = data_set
    # modified_data = np.vstack((a[::2, 0] + a[1::2, 0], (a[::2, 1] + a[1::2, 1]) / 2)).T
    # modified_data = np.vstack((np.sum(a[::2, 0], a[1::2, 0]), np.mean(a[::2, 1], a[1::2, 1])))
    print(a.size)
    b = np.zeros((int(a.shape[0]/10), *a.shape[1:]),  dtype=np.dtype(int))
    b[:, 0] = np.sum(a.reshape(-1, 10, 2), axis=1).reshape(-1, 2)[:, 0]
    b[:, 1] = np.mean(a.reshape(-1, 10, 2), axis=1).reshape(-1, 2)[:, 1]
    # print(modified_data)
    print(b)