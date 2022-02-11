from .euclidian_distance import euclidian_distance
from .config import TRAIN_LEN


# Треугольник => путь это все ребра кроме наибольшего
def process_triangle(contour):
    max_idx = None
    max_len = -1
    edges_length_sum = 0

    for idx in range(len(contour)):
        edge_len = euclidian_distance(contour[idx], contour[(idx + 1) % len(contour)])
        edges_length_sum += edge_len

        if edge_len > max_len:
            max_len = edge_len
            max_idx = idx

    train_count = int(round((edges_length_sum - max_len) / TRAIN_LEN))
    start_point = contour[max_idx][0]
    finish_point = contour[(max_idx + 1) % len(contour)][0]

    return start_point, finish_point, train_count
