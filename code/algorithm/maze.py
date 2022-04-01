import cv2
import time
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
import matplotlib.animation as animation
from matplotlib.backends.backend_agg import FigureCanvasAgg
import pandas as pd
import matplotlib
import PIL
import PIL.Image
# matplotlib.use('Agg')

std_ratio1 = 0.0534


# show the picture through matplotlib, the image shown by cv2 is too big
def show(img, time=0):
    plt.imshow(img, cmap='gray')
    plt.axis('off')
    plt.show()
    if time != 0:
        plt.pause(time)
        plt.close()


# sample points between two turnings for better animation, argument 'num' for sampling numbers
def sampling(start, end, num):
    result = []
    i = 1
    while i < num:
        result.append(round(start + i * (end - start) / num))
        i += 1
    return result


# this function is used to convert pixel distance to real distance
def convert(pix_dist, ratio):
    rolls = int(pix_dist * ratio / 20.9 * 10)
    return rolls


# this class is used for solve the route algorithm based on a maze graph and draw the animation
class car_map:
    image: np.array
    car_center: list
    car_length: int
    mark_map: np.array
    bfs_queue: list
    route: list
    route_for_gif: list

    def __init__(self, image, car_center, car_length):
        self.image = deepcopy(image)
        self.copy = deepcopy(self.image)
        self.car_center = car_center
        self.car_length = car_length
        self.mark_map = np.zeros(shape=(self.image.shape[0], self.image.shape[1], 3))
        self.bfs_queue = []
        self.route = []
        self.route_for_gif = []

    def init_car_in_map(self):
        for i in range(self.car_center[0] - self.car_length, self.car_center[0] + self.car_length + 1):
            for j in range(self.car_center[1] - self.car_length, self.car_center[1] + self.car_length + 1):
                self.image[i][j] = 128
        return True

    def destroy_car_in_map(self):
        self.image = deepcopy(self.copy)
        return True

    def show_map(self, alter=0):
        show(self.image, alter)

    # judge whether pixels of certain colors appears in the shape of car on the map
    # pure black: 0; pure white: 255
    def judge(self, color):
        # the four points
        if color != 64:
            if self.car_center[0] - self.car_length < 0 \
                    or self.car_center[0] + self.car_length > self.image.shape[0] \
                    or self.car_center[1] - self.car_length < 0 \
                    or self.car_center[1] + self.car_length > self.image.shape[1]:
                return True

        up = color in self.copy[self.car_center[0] - self.car_length,
                      self.car_center[1] - self.car_length: self.car_center[1] + self.car_length + 1]
        down = color in self.copy[self.car_center[0] + self.car_length,
                        self.car_center[1] - self.car_length: self.car_center[1] + self.car_length + 1]
        left = color in self.copy[self.car_center[0] - self.car_length: self.car_center[0] + self.car_length + 1,
                        self.car_center[1] - self.car_length]
        right = color in self.copy[self.car_center[0] - self.car_length: self.car_center[0] + self.car_length + 1,
                         self.car_center[1] + self.car_length]
        if up | down | left | right is False:
            return False
        return True
        # the algorithm below is ok, but much slower than the algorithm above
        # for i in range(self.car_center[0] - self.car_length, self.car_center[0] + self.car_length + 1):
        #     for j in range(self.car_center[1] - self.car_length, self.car_center[1] + self.car_length + 1):
        #         if self.copy[i][j] == color:
        #             return True
        # return False

    def move_vertical(self, ratio):  # ratio > 0: upward; ratio < 0 downward
        length = self.car_length * ratio
        self.car_center[0] -= length
        if self.judge(0) is True or self.judge(191) is True:  # meet black block or start line
            self.car_center[0] += length
            return False
        else:
            return True

    def move_horizontal(self, ratio):  # ratio > 0: left; ratio < 0 right
        length = self.car_length * ratio
        self.car_center[1] -= length
        if self.judge(0) is True or self.judge(191) is True:  # meet black block or start line
            self.car_center[1] += length
            return False
        else:

            return True

    # set the information(mark, coordinate point of the predecessor)on the image_length * image_width * 3 map
    # trade off: decrease time complexity, increase memory consumption
    def mark_map_assignment(self, mark, predecessor_x, predecessor_y):
        temp = np.array([mark, predecessor_x, predecessor_y])
        self.mark_map[self.car_center[0], self.car_center[1]] = temp

    # using BFS algorithm to get the best way to the end line
    def bfs_route(self, rate):
        self.bfs_queue.append(self.car_center)
        self.mark_map_assignment(1, self.car_center[0], self.car_center[1])
        while len(self.bfs_queue) > 0:
            temp_x, temp_y = self.bfs_queue[0][0], self.bfs_queue[0][1]
            self.car_center = [int(temp_x), int(temp_y)]
            # print(self.bfs_queue)
            # print(self.car_center)
            # self.init_car_in_map()
            # self.show_map(5)
            # self.destroy_car_in_map()
            mark = self.mark_map[temp_x, temp_y][0]
            del self.bfs_queue[0]
            if self.move_vertical(rate):  # go upward, car center modified
                if self.mark_map[self.car_center[0], self.car_center[1]][0] == 0:
                    self.mark_map_assignment(mark + 1, temp_x, temp_y)
                    self.bfs_queue.append(deepcopy(self.car_center))
                    if self.judge(64):
                        break
            self.car_center = [temp_x, temp_y]
            if self.move_vertical(-rate):  # go downward
                if self.mark_map[self.car_center[0], self.car_center[1]][0] == 0:
                    self.mark_map_assignment(mark + 1, temp_x, temp_y)
                    self.bfs_queue.append(deepcopy(self.car_center))
                    if self.judge(64):
                        break
            self.car_center = [temp_x, temp_y]
            if self.move_horizontal(rate):  # turn left
                if self.mark_map[self.car_center[0], self.car_center[1]][0] == 0:
                    self.mark_map_assignment(mark + 1, temp_x, temp_y)
                    self.bfs_queue.append(deepcopy(self.car_center))
                    if self.judge(64):
                        break
            self.car_center = [temp_x, temp_y]
            if self.move_horizontal(-rate):  # turn right
                if self.mark_map[self.car_center[0], self.car_center[1]][0] == 0:
                    self.mark_map_assignment(mark + 1, temp_x, temp_y)
                    self.bfs_queue.append(deepcopy(self.car_center))
                    if self.judge(64):
                        break
            self.car_center = [temp_x, temp_y]

    # after bfs, get the shortest route
    def get_route(self):
        self.route = []
        while True:
            temp = deepcopy(self.car_center)
            temp[0], temp[1] = int(temp[0]), int(temp[1])
            self.route.append(temp)
            if self.mark_map[temp[0]][temp[1]][0] == 1:
                break
            self.car_center[0] = int(self.mark_map[temp[0], temp[1]][1])
            self.car_center[1] = int(self.mark_map[temp[0], temp[1]][2])
        self.route.reverse()  # from the beginning to the end

    # cut out the points in one line, only keep the points on the turning
    def simplify_route(self):
        original_route = deepcopy(self.route)
        self.route = []
        for i in range(len(original_route)):
            if i == 0:
                self.route.append(original_route[i])
            elif i == len(original_route) - 1:
                self.route.append(original_route[i])
            else:
                if original_route[i][0] == original_route[i - 1][0] \
                        and original_route[i][0] == original_route[i + 1][0]:
                    continue
                elif original_route[i][1] == original_route[i - 1][1] \
                        and original_route[i][1] == original_route[i + 1][1]:
                    continue
                else:
                    self.route.append(original_route[i])

    # draw the route acquired by bfs algorithm on the map
    def plot_route(self):
        for i in range(len(self.route)):
            if i == len(self.route) - 1:
                break
            else:
                if self.route[i][0] == self.route[i + 1][0]:
                    _max = max(self.route[i][1], self.route[i + 1][1])
                    _min = min(self.route[i][1], self.route[i + 1][1])
                    for j in range(_min, _max):
                        self.image[self.route[i][0]][j] = 0
                elif self.route[i][1] == self.route[i + 1][1]:
                    _max = max(self.route[i][0], self.route[i + 1][0])
                    _min = min(self.route[i][0], self.route[i + 1][0])
                    for j in range(_min, _max):
                        self.image[j][self.route[i][1]] = 0

    # obtain the instructions through the turning points
    # which is used to control the car
    def set_instruction(self, name):
        route_copy = np.array(deepcopy(self.route))
        file = open('./{}.txt'.format(name), 'w+')
        for i in range(len(route_copy)):
            # initial direction is upward
            if i == 0:
                temp_0 = route_copy[1][0] - route_copy[0][0]
                temp_1 = route_copy[1][1] - route_copy[0][1]
                if temp_0 != 0:
                    temp_0 = abs(convert(temp_0, std_ratio1))
                    file.write('{}'.format(0) + '+m+' + '{:d}\n'.format(temp_0))
                if temp_1 != 0:
                    temp_1 = abs(convert(temp_1, std_ratio1))
                    file.write('{}'.format(0) + '+m+' + '{:d}\n'.format(temp_1))
            elif i == len(route_copy) - 1:
                file.close()
                return
            # positive angle means turning left
            # the annotation below describes: absolute direction -> relative direction
            else:
                temp_forward = route_copy[i + 1] - route_copy[i]
                temp_backward = route_copy[i] - route_copy[i - 1]
                if temp_forward[1] < 0 and temp_backward[0] < 0:  # direction: up to left -> turn left
                    temp = -convert(temp_forward[1], std_ratio1)
                    file.write('{}'.format(270) + '+m+' + '{:d}\n'.format(temp))
                elif temp_forward[1] > 0 and temp_backward[0] < 0:  # direction: up to right -> turn right
                    temp = convert(temp_forward[1], std_ratio1)
                    file.write('{}'.format(90) + '+m+' + '{:d}\n'.format(temp))
                elif temp_forward[1] < 0 and temp_backward[0] > 0:  # direction: down to left -> turn right
                    temp = -convert(temp_forward[1], std_ratio1)
                    file.write('{}'.format(90) + '+m+' + '{:d}\n'.format(temp))
                elif temp_forward[1] > 0 and temp_backward[1] > 0:  # direction: down to right -> turn left
                    temp = convert(temp_forward[1], std_ratio1)
                    file.write('{}'.format(270) + '+m+' + '{:d}\n'.format(temp))
                elif temp_forward[0] < 0 and temp_backward[1] < 0:  # direction: left to up -> turn right
                    temp = -convert(temp_forward[0], std_ratio1)
                    file.write('{}'.format(90) + '+m+' + '{:d}\n'.format(temp))
                elif temp_forward[0] > 0 and temp_backward[1] < 0:  # direction: left to down -> turn left
                    temp = convert(temp_forward[0], std_ratio1)
                    file.write('{}'.format(270) + '+m+' + '{:d}\n'.format(temp))
                elif temp_forward[0] < 0 and temp_backward[1] > 0:  # direction: right to up -> turn left
                    temp = -convert(temp_forward[0], std_ratio1)
                    file.write('{}'.format(270) + '+m+' + '{:d}\n'.format(temp))
                elif temp_forward[0] > 0 and temp_backward[1] > 0:  # direction: right to down -> turn right
                    temp = convert(temp_forward[0], std_ratio1)
                    file.write('{}'.format(90) + '+m+' + '{:d}\n'.format(temp))

    def save_image(self, file_path):
        cv2.imwrite(file_path, self.image)

    # the part below of the class is for the gif demo, which is used for the final show
    def set_demo_gif_route(self, sample_num):
        self.route_for_gif = []
        for i in range(len(self.route)):
            if i == len(self.route) - 1:
                self.route_for_gif.append(self.route[i])
            else:
                if self.route[i][0] == self.route[i + 1][0]:
                    temp = sampling(self.route[i][1], self.route[i + 1][1], sample_num)
                    self.route_for_gif.append(self.route[i])
                    for j in range(len(temp)):
                        self.route_for_gif.append([self.route[i][0], temp[j]])
                elif self.route[i][1] == self.route[i + 1][1]:
                    temp = sampling(self.route[i][0], self.route[i + 1][0], sample_num)
                    self.route_for_gif.append(self.route[i])
                    for j in range(len(temp)):
                        self.route_for_gif.append([temp[j], self.route[i][1]])

    def animate(self, frame_num):
        route = np.array(deepcopy(self.route_for_gif))
        if frame_num == 0:
            plt.scatter(route[0, 1], route[0, 0], c='red', s=50, alpha=1)
        else:
            plt.plot(route[: frame_num, 1], route[: frame_num, 0], lw=5, c='gray', alpha=0.5)
            plt.scatter(route[frame_num - 1, 1], route[frame_num - 1, 0], c='red', s=50, alpha=1)

    def show_demo(self):
        fig = plt.figure()
        plt.imshow(self.image, cmap='gray')
        plt.axis('off')
        ani = animation.FuncAnimation(fig, self.animate, np.arange(0, len(self.route_for_gif)), blit=False)
        ani.save('./change.gif', fps=10)
        plt.show()

    def save_plot_route(self, file_path):
        route = np.array(deepcopy(self.route))
        plt.imshow(self.image, cmap='gray')
        plt.axis('off')
        plt.scatter(route[len(route) - 1, 1], route[len(route) - 1, 0], c='red', alpha=1, s=50)
        plt.plot(route[:, 1], route[:, 0], c='gray', lw=5, alpha=0.5)
        plt.savefig(file_path)
        plt.show()


def save_as_qpixmap(image, route_list, success_times):
    used_image = deepcopy(image)
    route = np.array(route_list)
    fig, ax = plt.subplot()
    ax.imshow(used_image, cmap='gray')
    ax.axis('off')
    if success_times == 0:
        ax.scatter(route[0, 1], route[0, 0], c='red', alpha=1, s=50)
    else:
        ax.scatter(route[success_times, 1], route[success_times, 0], c='red', alpha=1, s=50)
        ax.plot(route[: success_times + 1, 1], route[: success_times + 1, 0], c='gray', lw=5, alpha=0.5)
    canvas = FigureCanvasAgg(ax.gcf())
    canvas.draw()
    width, height = canvas.get_width_height()
    temp = np.frombuffer(canvas.tostring_argb(), dtype=np.uint8)
    temp.shape = (width, height, 4)
    temp = np.roll(temp, 3, axis=2)
    result = PIL.Image.frombytes('RGBA', (width, height), temp)
    result = np.asarray(result)
    image_pil = PIL.Image.fromarray(np.uint8(result))
    image_pil = image_pil.toqpixmap()
    return image_pil


def save(image, route_list, success_times):
    used_image = deepcopy(image)
    route = np.array(route_list)
    fig, ax = plt.subplot()
    ax.imshow(used_image, cmap='gray')
    ax.axis('off')
    if success_times == 0:
        ax.scatter(route[0, 1], route[0, 0], c='red', alpha=1, s=50)
    else:
        ax.scatter(route[success_times, 1], route[success_times, 0], c='red', alpha=1, s=50)
        ax.plot(route[: success_times + 1, 1], route[: success_times + 1, 0], c='gray', lw=5, alpha=0.5)
    ax.savefig('map.jpg', bbox_inches='tight', pad_inches=0)
    # canvas = FigureCanvasAgg(plt.gcf())
    # width, height = canvas.get_width_height()
    # temp = np.frombuffer(canvas.tostring_argb(), dtype=np.uint8)
    # temp.shape = (width, height, 4)
    # temp = np.roll(temp, 3, axis=2)
    # result = PIL.Image.frombytes('RGBA', (width, height), temp)
    # result = np.asarray(result)[:, :, : 3]
    # return result


# convert a certain point from one picture to another with different scale
def pixel_point_convert(firsthand_image, target_image, pixel_posi):
    new_x = int(pixel_posi[0] / firsthand_image.shape[1] * target_image.shape[1])
    new_y = int(pixel_posi[1] / firsthand_image.shape[0] * target_image.shape[0])
    return [new_x, new_y]


def store_list(file_name, lis):
    file = open('{}.txt'.format(file_name), 'w+')
    for i in range(len(lis)):
        file.write('{}'.format(lis[i][0]) + ',' + '{}'.format(lis[i][1]) + '\n')
    file.close()


def read_list(file_name):
    file = pd.read_csv('{}.txt'.format(file_name), header=None)
    result = np.array(file).tolist()
    return result


if __name__ == '__main__':
    # # this is used for the original route
    # image = cv2.imread('./maze1.bmp', cv2.IMREAD_GRAYSCALE)
    # copy = deepcopy(image)
    # for i in range(2400, 2450):
    #     for j in range(2300, 2900):  # start line, (255 + 127) / 2 = 191
    #         copy[i][j] = 191
    #
    # for i in range(2400, 2450):
    #     for j in range(650, 1250):  # end line, (255 - 127) / 2 = 64
    #         copy[i][j] = 64
    #
    # # now we get the map with start line, end line
    # center_height, center_width, length = [2300, 2600, 160]
    # car_center = [center_height, center_width]
    # test_car = car_map(copy, car_center, length)
    #
    # # test_car.init_car_in_map()
    # # test_car.show_map(5)
    # # test_car.destroy_car_in_map()
    #
    # test_car.bfs_route(1)
    # test_car.get_route()
    # test_car.simplify_route()
    #
    # test_car.plot_route()
    # test_car.show_map()
    # # used to get the instruction for the car
    # test_car.set_instruction('original map')
    # # used to recover the picture
    # test_car.image = deepcopy(copy)
    #
    # cv2.imwrite('./original_route.jpg', test_car.image)
    #
    # # used for the demo gif showing how the car is moving
    # # test_car.set_demo_gif_route(5)
    # # test_car.show_map()
    # # test_car.show_demo()
    #
    # bg_image = deepcopy(image)
    # image_ndarray = save_as_qpixmap(bg_image, test_car.route)
    #
    # store_list('route.txt', test_car.route)
    #
    # # used for the route with obstacle
    # image_2 = cv2.imread('./maze2.bmp', cv2.IMREAD_GRAYSCALE)
    # copy_2 = deepcopy(image_2)
    # for i in range(2250, 2300):
    #     for j in range(2200, 2750):  # start line, (255 + 127) / 2 = 191
    #         copy_2[i][j] = 191
    #
    # for i in range(2250, 2300):
    #     for j in range(600, 1200):  # end line, (255 - 127) / 2 = 64
    #         copy_2[i][j] = 64
    #
    # # now we get the map with start line, end line
    # length_2 = pixel_point_convert(image, image_2, [test_car.car_length, test_car.car_length])[0]
    # car_center_2 = pixel_point_convert(image, image_2, test_car.route[6])
    # modified_map = car_map(copy_2, car_center_2, length_2)
    #
    # modified_map.init_car_in_map()
    # modified_map.show_map(5)
    # modified_map.destroy_car_in_map()
    #
    # modified_map.bfs_route(1)
    # modified_map.get_route()
    # modified_map.simplify_route()
    #
    # modified_map.plot_route()
    # modified_map.show_map()
    #
    # save(image, test_car.route, -1)

    # this is the main part for creating map and instructions
    image_1 = cv2.imread('./maze1.bmp', cv2.IMREAD_GRAYSCALE)
    image_2 = cv2.imread('./maze2.bmp', cv2.IMREAD_GRAYSCALE)
    image_2 = cv2.resize(image_2, dsize=(image_1.shape[1], image_1.shape[0]))

    # initialize the start point and end point
    for i in range(2400, 2450):
        for j in range(2300, 2900):  # start line, (255 + 127) / 2 = 191
            image_1[i][j] = 191

    for i in range(2400, 2450):
        for j in range(650, 1250):  # end line, (255 - 127) / 2 = 64
            image_1[i][j] = 64

    for i in range(2400, 2450):
        for j in range(2300, 2900):  # start line, (255 + 127) / 2 = 191
            image_2[i][j] = 191

    for i in range(2400, 2450):
        for j in range(650, 1250):  # end line, (255 - 127) / 2 = 64
            image_2[i][j] = 64

    # now we get the map with start line, end line
    center_height, center_width, length = [2300, 2600, 160]
    car_center = [center_height, center_width]
    map_1 = car_map(image_1, car_center, length)

    map_1.bfs_route(1)
    map_1.get_route()
    map_1.simplify_route()

    map_1.plot_route()
    map_1.show_map()
    map_1.save_image('./map_1.jpg')
    map_1.image = deepcopy(image_1)
    map_1.save_plot_route('./map_1_.jpg')
    map_1.set_instruction('map_1')

    block_point = 6
    ch_2, cw_2, l2 = [map_1.route[block_point][0], map_1.route[block_point][1], 160]
    c2_center = [map_1.route[block_point][0], map_1.route[block_point][1]]

    map_2 = car_map(image_2, c2_center, l2)
    map_2.init_car_in_map()
    map_2.show_map()
    map_2.destroy_car_in_map()

    map_2.bfs_route(1)
    map_2.get_route()
    map_2.simplify_route()

    map_2.plot_route()
    map_2.show_map()
    map_2.image = deepcopy(image_2)
    map_2.save_plot_route('./map_2_.jpg')
    map_2.set_instruction('map_2')

