import numpy as np


class EdgeDescription:
    """
    Более расширенное описания ребра
    Хранит в себе информацию о соединении ребра с другими ребрами

    info: индекс инцедентного ребра
    state: состояние вершины (0 - свободна, 1 - соединена с ребром, 2 - соединена с городом)
    """

    def __init__(self, edge_info):
        self.fst_point = edge_info[0]
        self.fst_state = 0
        self.fst_info = None

        self.snd_point = edge_info[1]
        self.snd_state = 0
        self.snd_info = None

        self.length = edge_info[2]

    @classmethod
    def try_connect_edges(cls, fst, snd, distance_threshold):
        result = [None] * 4

        if snd.fst_state == 0:
            result[0] = fst.try_connect_to_fst(snd.fst_point, distance_threshold)
            result[2] = fst.try_connect_to_snd(snd.fst_point, distance_threshold)
        if snd.snd_state == 0:
            result[1] = fst.try_connect_to_fst(snd.snd_point, distance_threshold)
            result[3] = fst.try_connect_to_snd(snd.snd_point, distance_threshold)

        return result

    def close(self, idx):
        if idx == 0:
            self.fst_state = 2
        elif idx == 1:
            self.snd_state = 2
        else:
            raise ValueError('Incorrect state idx')

    def connect(self, idx):
        if idx == 0:
            self.fst_state = 1
        elif idx == 1:
            self.snd_state = 1
        else:
            raise ValueError('Incorrect state idx')

    def set_info(self, idx, info):
        if idx == 0:
            self.fst_info = info
        elif idx == 1:
            self.snd_info = info
        else:
            raise ValueError('Incorrect state idx')

    def get_state(self, idx):
        if idx == 0:
            return self.fst_state
        elif idx == 1:
            return self.snd_state
        else:
            raise ValueError('Incorrect state idx')

    def get_point(self, idx):
        if idx == 0:
            return self.fst_point
        elif idx == 1:
            return self.snd_point
        else:
            raise ValueError('Incorrect state idx')

    def try_connect(self, point, distance_threshold):
        return (self.try_connect_to_fst(point, distance_threshold), self.try_connect_to_snd(point, distance_threshold))

    def try_connect_to_fst(self, point, distance_threshold):
        if self.fst_state == 0:
            length = np.linalg.norm([self.fst_point[0] - point[0], self.fst_point[1] - point[1]])
            return length if length <= distance_threshold else None
        return None

    def try_connect_to_snd(self, point, distance_threshold):
        if self.snd_state == 0:
            length = np.linalg.norm([self.snd_point[0] - point[0], self.snd_point[1] - point[1]])
            return length if length <= distance_threshold else None
        return None
