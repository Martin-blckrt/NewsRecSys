import numpy as np
from scipy.spatial import distance


def to_binary(list1, list2):
    binary_list1 = [1 if name in list2 else 0 for name in list1]
    binary_list2 = [1 if name in list1 else 0 for name in list2]
    return binary_list1, binary_list2


def avg_metric(list_eps: dict):
    rewards = [ep.reward[0].item() for ep in list(list_eps.values())]
    return np.mean(rewards)


def similarity(list1, list2, method="jaccard"):
    bin1, bin2 = to_binary(list1, list2)

    if method == "cosine":
        return distance.cosine(bin1, bin2)  # lower is better
    elif method == "jaccard":
        return distance.jaccard(bin1, bin2)  # lower is better
    else:
        return distance.kulczynski1(bin1, bin2)  # higher is better
        # maybe return 1/(dist + 1) if we want to make it "lower is better"
