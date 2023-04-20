import numpy as np
from scipy.spatial import distance


def to_binary(list1: list, list2: list):
    binary_list1 = [1 if name in list2 else 0 for name in list1]
    binary_list2 = [1 if name in list1 else 0 for name in list2]

    """
    Méthode padding 0 just in case
    if len(list1) > len(list2):
        binary_list2 += [0] * (len(list1) - len(list2))
    elif len(list2) > len(list1):
        binary_list1 += [0] * (len(list2) - len(list1))
    """

    return binary_list1, binary_list2


def avg_metric(list_eps: dict):
    rewards = [ep.reward[0].item() for ep in list(list_eps.values())]
    return np.mean(rewards)


def similarity(list1, list2, method="jaccard"):
    bin1, bin2 = to_binary(list1, list2)

    if method == "cosine":
        return 1 - distance.cosine(bin1, bin2)  # higher is is better
    else:
        return 1 - distance.jaccard(bin1, bin2)  # higher is better
