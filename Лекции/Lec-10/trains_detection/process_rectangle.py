import numpy as np
from .euclidian_distance import euclidian_distance
from .config import TRAIN_LEN


# Прямоугольник => путь это середина прямоугольника
def process_rectangle(contour):
    max_fst_idx = None
    max_fst_len = -1

    max_snd_idx = None
    max_snd_len = -1

    for idx in range(len(contour)):
        edge_len = euclidian_distance(contour[idx], contour[(idx + 1) % len(contour)])

        if edge_len > max_fst_len:
            max_snd_idx = max_fst_idx
            max_snd_len = max_fst_len

            max_fst_idx = idx
            max_fst_len = edge_len

        elif edge_len > max_snd_len:
            max_snd_idx = idx
            max_snd_len = edge_len

    start_point = None
    finish_point = None

    for idx in range(len(contour)):
        if idx != max_fst_idx and idx != max_snd_idx:
            if start_point is None:
                start_point_x = int(round((contour[idx][0][0] + contour[(idx + 1) % len(contour)][0][0]) / 2))
                start_point_y = int(round((contour[idx][0][1] + contour[(idx + 1) % len(contour)][0][1]) / 2))
                start_point = (start_point_x, start_point_y)
            else:
                finish_point_x = int(round((contour[idx][0][0] + contour[(idx + 1) % len(contour)][0][0]) / 2))
                finish_point_y = int(round((contour[idx][0][1] + contour[(idx + 1) % len(contour)][0][1]) / 2))
                finish_point = (finish_point_x, finish_point_y)

    train_count = int(round(
        np.sqrt
            (np.power(start_point[0] - finish_point[0], 2) + np.power(start_point[1] - finish_point[1], 2)) / TRAIN_LEN
    ))

    return start_point, finish_point, train_count