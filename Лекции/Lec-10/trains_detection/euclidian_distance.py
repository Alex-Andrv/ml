import numpy as np


def euclidian_distance(fst, snt):
    return np.sqrt(
        np.power(fst[0][0] - snt[0][0], 2) +
        np.power(fst[0][1] - snt[0][1], 2)
    )
