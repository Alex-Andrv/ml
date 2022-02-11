import numpy as np
import cv2
import matplotlib.pyplot as plt


DATA_DIR = './pics/trains/'

TRAIN_LEN = 120  # Примерная длина паровозика
TRAIN_AREA = 1500  # Примерная прощадь паровозика

# Константы для создания графа
MAX_DISTANCE_BETWEEN_TRAINSDISTANCE = int(TRAIN_LEN / 2)
MAX_DISTANCE_BETWEEN_POINTS = 1.8 * TRAIN_LEN

# Цветовые константы
GREEN_LOWER = np.array([63, 124, 56])
GREEN_UPPER = np.array([94, 243, 132])

# Создание примитивов (шаблонов) для использование алгоритма "Template matching"
# Source: https://docs.opencv.org/4.x/d4/dc6/tutorial_py_template_matching.html
img_with_city_templates = cv2.imread(DATA_DIR + 'red_green_blue_inaccurate.jpg')
city_template = img_with_city_templates[255:280, 675:700]

# plt.imshow(city_template)
