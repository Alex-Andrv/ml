import numpy as np
from .process_line import process_line
from .process_triangle import process_triangle
from .process_rectangle import process_rectangle


def process_contours(contours: np.ndarray):
    """
    Переводит контуры в ребра

    contours: Контуры
    """

    edges_info = []  # список информации о ребрах (начало, конец, длина)

    # Разбираем частные случаи контуров
    for contour in contours:
        if len(contour) == 2:
            start_point, finish_point, train_count = process_line(contour)
        elif len(contour) == 3:
            start_point, finish_point, train_count = process_triangle(contour)
        elif len(contour) == 4:
            start_point, finish_point, train_count = process_rectangle(contour)
        else:
            # Поскольку в этом примере мы аппроксимируем контуры очень простыми фигурами, такого не должно произойти
            assert False

        edges_info.append((start_point, finish_point, train_count))

    return edges_info