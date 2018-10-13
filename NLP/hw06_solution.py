
from hw05_solution import levenshtein_dp
import numpy as np

def suggest(a, dictionary):

    DIST_MIN = []
    suggestions = []

    for i in range(len(dictionary)):
        b = dictionary[i]
        dist_min = levenshtein_dp(a, b)
        DIST_MIN.append(dist_min)

    mindist = np.array(DIST_MIN)
    listmin = np.where(mindist == mindist.min())
    suggestions = ([ dictionary[index] for index in listmin[0] ])

    return suggestions