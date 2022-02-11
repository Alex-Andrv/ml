from typing import List, Tuple
import numpy as np
import cv2
from .config import TRAIN_AREA
from .process_countours import process_contours
from .create_graph import create_graph


def process_trains(
        img: np.ndarray,
        img_hsv: np.ndarray,
        hsv_lower: np.ndarray,
        hsv_upper: np.ndarray,
        center_points: List[Tuple[int, int]]
):
    """
    Алгоритм поиска паровозиков

    img: Изображение в формате BGR
    img_hsv: Изображение в формате HSV
    hsv_lower: Нижняя чветовая граница
    hsv_upper: Верхняя цветовая граница
    center_points: Координаты городов
    """

    # Фильтруем цвет по маске
    # Source: https://docs.opencv.org/3.4/da/d97/tutorial_threshold_inRange.html
    color_mask = cv2.inRange(img_hsv, hsv_lower, hsv_upper)

    # Применяем морфологические преобразования для уточнения маски (в данном случае эрозию)
    # Source: https://docs.opencv.org/3.4/d9/d61/tutorial_py_morphological_ops.html
    color_mask = cv2.morphologyEx(color_mask, op=cv2.MORPH_ERODE, kernel=(5, 5))

    # Находим по маске контуры изображения
    # Source: https://docs.opencv.org/4.x/d4/d73/tutorial_py_contours_begin.html
    contours, hierarhy = cv2.findContours(color_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Удалаяем маленькие контуры и пытаемcя аппроксимировать оставшиеся как можно более простыми фигурами
    # (прямая, треугольник и прямоугольник). Для этого был подобран коэффицент для `epsilon` равным 0.1
    # Source: https://docs.opencv.org/3.4/dd/d49/tutorial_py_contour_features.html
    filtered_contours = []
    for idx, contour in enumerate(contours):
        cv2.drawContours(img, [contour], -1, (255, 255, 255), 10)
        area = cv2.contourArea(contour)

        # Проверяем что контур достаточного размера и у него нет родителей
        # Source: https://docs.opencv.org/3.4/d9/d8b/tutorial_py_contours_hierarchy.html
        if area > TRAIN_AREA and hierarhy[0][idx][3] == -1:
            epsilon = 0.1 * cv2.arcLength(contour, True)
            contour_approx = cv2.approxPolyDP(contour, epsilon, True)
            filtered_contours.append(contour_approx)

    # Получаем количество паровозиков и "ребра" графа
    edges_info = process_contours(filtered_contours)

    # Строим граф
    additional_lines, connection_idxs, new_centers, train_numbers, = create_graph(
        center_points,
        edges_info
    )

    return additional_lines, edges_info, new_centers, train_numbers