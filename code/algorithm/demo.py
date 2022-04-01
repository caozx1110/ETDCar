import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from time import sleep
from PyQt5.QtGui import QPixmap, QImage

lock = threading.Lock()
img = plt.imread('./1.jpg')
fig = plt.figure(figsize=(4, 3))
ax = fig.add_subplot(111)

def a():
    global result
    global demo_list
    while True:
        print('a start')
        if len(demo_list) == 0:
            print('www')
        elif len(demo_list) == len(result):
            print('a end')
            return
        else:
            print(demo_list)

        sleep(1)


def b():
    global result
    global demo_list
    while True:
        lock.acquire()
        print('b start')
        if len(demo_list) == len(result):
            print('b end')
            return
        elif len(demo_list) == 0:
            demo_list = np.array([result[0]])
        else:
            demo_list = np.concatenate((demo_list, np.array([result[len(demo_list)]])))
        sleep(3)
        lock.release()


if __name__ == '__main__':
    t = [threading.Thread(target=a), threading.Thread(target=b)]
    result = np.random.randint(10, size=(10, 2))
    demo_list = np.array([])

    for i in range(len(t)):
        t[i].setDaemon(True)
        t[i].start()

    while True:
        m = len(demo_list)
        if m == 0:
            continue
        else:
            ax.imshow(img, extent=[0, 10, 0, 10])
            ax.plot(demo_list[:, 0], demo_list[:, 1], c='orange')
            ax.set_title('demo')
            plt.draw()
            plt.pause(1)


def Fig2QPix(data):
    fig = plt.Figure()
    img = plt.imread('net3.jpg')
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    ax.plot(data[:, 0], data[:, 1], c='violet')
    ax.set_title('demo')
    canvas.draw()
    width, height = int(fig.bbox.width), int(fig.bbox.height)
    im = QImage(canvas.buffer_rgba(), width, height, QImage.Format_ARGB32)
    return QPixmap(im)


result = np.random.randint(10, size=(10, 2))
fig = plt.figure(figsize=(4, 3))
ax = fig.add_subplot(111)
img = plt.imread('./1.jpg')
ax.imshow(img, extent=[0, 10, 0, 10])
ax.plot(result[:, 0], result[:, 1], c='violet')
plt.show()

