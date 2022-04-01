from copy import def save_as_ndarray_for_qt(image, route_list, success_times):
    used_image = deepcopy(image)
    route = np.array(route_list)
    plt.imshow(used_image, cmap='gray')
    plt.axis('off')
    if success_times == 0:
        plt.scatter(route[len(route_list) - 1, 1], route[len(route_list) - 1, 0], c='red', alpha=1, s=50)
    else:
        plt.scatter(route[len(route_list) - 1, 1], route[len(route_list) - 1, 0], c='red', alpha=1, s=50)
        plt.plot(route[:, 1], route[:, 0], c='gray', lw=5, alpha=0.5)
    canvas = FigureCanvasAgg(plt.gcf())
    canvas.draw()
    width, height = canvas.get_width_height()
    temp = np.frombuffer(canvas.tostring_argb(), dtype=np.uint8)
    temp.shape = (width, height, 4)
    temp = np.roll(temp, 3, axis=2)
    result = PIL.Image.frombytes('RGBA', (width, height), temp)
    result = np.asarray(result)
    return result[:, :, : 3]eepcopy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import PIL


d