import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def ext(str_array, pivot):
    result = np.array([])
    for i in range(len(str_array)):
        temp = int(str_array[i][pivot:])
        result = np.append(result, temp)
    return result


table = pd.read_csv('./table_1.txt', header=None, index_col=None)


l_t = ext(table[0], len('LeftTach: '))
l_s = ext(table[1], len('leftsteps: '))
r_t = ext(table[2], len('righttach: '))
r_s = ext(table[3], len('rightsteps: '))

x = np.arange(len(l_t))
plt.plot(x, l_t, label='left speed', c='orange')
plt.plot(x, r_t, label='left speed', c='violet')
plt.legend()
plt.title('speed via times ')
plt.show()

# output = np.polyfit(l_t, r_t, deg=1)
# x = np.linspace(25000, 60000, 59)
# for i in range(len(l_t)):
#     if abs(r_t[i] - l_t[i]) / l_t[i] > 0.1:
#         color = 'red'
#     else:
#         color = 'green'
#     plt.scatter(l_t[i], r_t[i], c=color)
# plt.plot(x, x, label='standard y = x line', c='black')
# y = l_t * output[0] + output[1]
# plt.plot(l_t, y, label='fitted line', c='blue')
# plt.legend()
# plt.title('right speed via left speed')
# plt.savefig('./l_r_velocity.jpg')
# plt.show()

x = np.linspace(min(l_s), max(l_s), 300)
plt.scatter(l_s, -r_s, label='right via left', c='violet', s=10)
output = np.polyfit(l_s, -r_s, deg=1)
y = x * output[0] + output[1]
plt.plot(x, y, label='fitted line', c='green')
plt.plot(x, x, label='standard y=x line', c='black')
plt.legend()
plt.savefig('./l_r_step.jpg')
plt.show()

