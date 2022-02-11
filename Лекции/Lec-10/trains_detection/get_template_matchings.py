import numpy as np
import cv2
from .config import TRAIN_LEN


def get_template_matchings(
        img: np.ndarray,
        template: np.ndarray,
        threshold=0.8
):
    """
    Использование подхода "Template Matching" для нахождения объектов на изображении.

    img: Изображение в формате BGR
    template: Шаблон в формате BGR
    threshold: Гиперпараметр отсечения (может быть до-настроен)
    """

    mask = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED) > threshold  # Находим все похожие точки на изображении

    # Получаем координаты этих точек
    template_points = []
    for y_mask in range(mask.shape[0]):
        for x_mask in range(mask.shape[1]):
            if mask[y_mask, x_mask] > 0:
                # Здесь необходим сдвиг, так как коэффициент определяется для угловой точки шаблона
                template_points.append((x_mask + int(template.shape[1] / 2), y_mask + int(template.shape[0] / 2)))


    # Так как некоторые полученные точки могут ссылаться на один и тот же объект, то фильтруем их по расстоянию
    filtered_points = []
    for (new_point_x, new_point_y) in template_points:
        for idx, (detected_point_x, detected_point_y) in enumerate(filtered_points):
            if max(abs(new_point_x - detected_point_x), abs(new_point_y - detected_point_y)) < (TRAIN_LEN // 2):
                avg_point_x = int(round((new_point_x + detected_point_x) / 2))
                avg_point_y = int(round((new_point_y + detected_point_y) / 2))

                filtered_points[idx] = (avg_point_x, avg_point_y)
                break
        else:
            filtered_points.append((new_point_x, new_point_y))

    return filtered_points
