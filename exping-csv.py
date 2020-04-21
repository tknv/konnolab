import sys
import datetime
import time
from datetime import datetime
import os
import csv
import decimal
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates
from matplotlib.widgets import Slider
import pytz


from pylab import rcParams

# 4/16/2020  17:53:46
p='%Y/%m/%d %H:%M:%S'
# os.environ['TZ']='UTC'
os.environ['TZ']='Asia/Tokyo'
# np.set_printoptions(threshold=sys.maxsize)
exping_file = sys.argv[1]
with open(file=exping_file, newline='', encoding="cp932") as csvfile:
    next(csvfile)
    ping_result = csv.reader(csvfile)
    result_list = list(ping_result)
# craft data
data_len = len(result_list)
print(data_len)
dataset_mod = data_len % 10
print(dataset_mod)
data_list = result_list[dataset_mod:]
data_set_len = len(data_list)
# print(data_list)
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
b = np.zeros((int(a.shape[0]/10), *a.shape[1:]),  dtype=np.dtype(int))
b[:, 0] = np.sum(a.reshape(-1, 10, 2), axis=1).reshape(-1, 2)[:, 0]
b[:, 1] = np.mean(a.reshape(-1, 10, 2), axis=1).reshape(-1, 2)[:, 1]
# print(b)
for c in b:
    timedate = datetime.fromtimestamp(c[1])
    tz = pytz.timezone('Asia/Tokyo')
    _hit_time = tz.localize(timedate)
    hit_time = _hit_time.strftime('%Y/%m/%d %H:%M:%S')
    if c[0]==10:
        print('%s ping lost 10 times continusouly' % hit_time)
    else:
        print('{} ping lost :'.format(hit_time)
        + "*" * c[0]
        )


plt.gca().set_aspect('equal', adjustable='box')
lost = b[:,0]
print(lost)
epoch = b[:,1]
local_time = []
for mean_time in epoch:
    sec = matplotlib.dates.epoch2num(mean_time)
    local_time.append(sec)
fig, ax = plt.subplots()
ax.plot_date(local_time, lost)
date_fmt = '%y-%m-%d %H:%M:%S'
# Use a DateFormatter to set the data to the correct format.
date_formatter = matplotlib.dates.DateFormatter(date_fmt)
ax.xaxis.set_major_formatter(date_formatter)
# Sets the tick labels diagonal so they fit easier.
fig.autofmt_xdate()
plt.xlabel('Time')
plt.ylabel('Ping lost')
plt.title('Ping lost per 10 shots in meantime')
plt.legend()
plt.xticks(np.arange(min(local_time), max(local_time)+1, 0.001))
graph_img = exping_file + '.png'
plt.savefig(graph_img)
plt.show()