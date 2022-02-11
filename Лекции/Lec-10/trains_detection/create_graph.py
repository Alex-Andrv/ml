from typing import List, Tuple
import numpy as np
from .edge_description import EdgeDescription
from .config import TRAIN_LEN


def create_graph(
    centers: np.ndarray, 
    edges: List[Tuple[int, int, int]]
):
    """
    Соединяет ребра и города в полноценный граф
    
    centers: Города
    edges: Приближение паровозиков ребрами
    """
    
    additional_connections = []  # Промежуточные соединения между ребрами
    connection_info = []  # Информация о том, какие ребра мы соединяли друг с другом

    edge_descriptions = []
    for edge in edges:
        edge_descriptions.append(EdgeDescription(edge))

    # Постепенно увеличиваем дистанцию соединения
    # Вообще тут есть гипотеза которую не было времени проверить о том, 
    # что лучше соединять не только объекты с минимально дистанцией,
    # но и объекты, для которых эта дистанция просто меньше порога.
    # К счастью, из-за малого количества соединений это не сыграло роли
    for distance_ratio in [0.5, 0.75, 1.0, 1.5]:
        distance_threshold = distance_ratio * TRAIN_LEN
        
        # Пытаемся соединиться с центрами (они приоритетнее чем другие ребра)
        for idx, edge_description in enumerate(edge_descriptions):
            center_distances_1 = []
            center_distances_2 = []

            for center_idx, center in enumerate(centers):
                dist_1, dist_2 = edge_description.try_connect(center, distance_threshold)
                if dist_1:
                    center_distances_1.append((center_idx, dist_1))
                if dist_2:
                    center_distances_2.append((center_idx, dist_2))

            sorted_centers_1 = sorted(center_distances_1, key=lambda x: x[1])
            sorted_centers_2 = sorted(center_distances_2, key=lambda x: x[1])

            best_center_idx_1, best_center_dist_1 = sorted_centers_1[0] if len(sorted_centers_1) > 0 else (None, None)
            best_center_idx_2, best_center_dist_2 = sorted_centers_2[0] if len(sorted_centers_2) > 0 else (None, None)

            if best_center_idx_1 == best_center_idx_2 and best_center_idx_1 is not None:
                if best_center_dist_1 < best_center_dist_2:
                    edge_description.close(0)
                    additional_connections.append((centers[best_center_idx_1], edge_description.fst_point))
                else:
                    edge_description.close(1)
                    additional_connections.append((centers[best_center_idx_2], edge_description.snd_point))
            else:
                if best_center_idx_1 is not None:
                    edge_description.close(0)
                    additional_connections.append((centers[best_center_idx_1], edge_description.fst_point))
                if best_center_idx_2 is not None:
                    edge_description.close(1)
                    additional_connections.append((centers[best_center_idx_2], edge_description.snd_point))

        # Пытаемся соединиться с другими ребрами
        distance_array = []
        for fst_idx, fst_edge in enumerate(edge_descriptions):
            for snd_idx, snd_edge in list(enumerate(edge_descriptions))[fst_idx + 1:]:
                distances = EdgeDescription.try_connect_edges(fst_edge, snd_edge, distance_threshold)
                
                for dist_idx, dist in enumerate(distances):
                    if dist is not None:
                        distance_array.append((dist, fst_idx, snd_idx, dist_idx // 2, dist_idx % 2))

        for (dist, idx_outer_a, idx_outer_b, idx_inner_a, idx_inner_b) in list(
                sorted(distance_array, key=lambda x: x[0])
        ):
            if dist < distance_threshold and \
                edge_descriptions[idx_outer_a].get_state(idx_inner_a) == 0 and \
                edge_descriptions[idx_outer_b].get_state(idx_inner_b) == 0:
                
                edge_descriptions[idx_outer_a].connect(idx_inner_a)
                edge_descriptions[idx_outer_b].connect(idx_inner_b)
                
                edge_descriptions[idx_outer_a].set_info(idx_inner_a, idx_outer_b)
                edge_descriptions[idx_outer_b].set_info(idx_inner_b, idx_outer_a)

                edge_descriptions[idx_outer_a].length += int(dist / TRAIN_LEN)
                
                additional_connections.append((
                    edge_descriptions[idx_outer_a].get_point(idx_inner_a),
                    edge_descriptions[idx_outer_b].get_point(idx_inner_b)
                ))
                connection_info.append((idx_outer_a, idx_outer_b))
    
    new_centers = []
    train_numbers = 0
    
    for idx, edge_descr in enumerate(edge_descriptions):
        train_numbers += edge_descr.length
        
        # Если вершинка ребра не была ни с чем соединена, то рядом с ней должен быть город
        for i in range(2):
            if edge_descr.get_state(i) == 0:
                new_centers.append(edge_descr.get_point(i))
    
    return additional_connections, connection_info, new_centers, train_numbers
