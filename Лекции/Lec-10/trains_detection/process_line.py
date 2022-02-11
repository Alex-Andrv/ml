from .euclidian_distance import euclidian_distance
from .config import TRAIN_LEN


# Прямая => путь это прямая
def process_line(contour):
    contour_len = euclidian_distance(contour[0], contour[1])

    train_count = int(round(contour_len / TRAIN_LEN))
    start_point = contour[0][0]
    finish_point = contour[1][0]

    return start_point, finish_point, train_count
