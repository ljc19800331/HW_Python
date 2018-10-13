# hw5 -- dynamic programming for edit distance

import numpy as np

def levenshtein_dp(a, b):

    # Test cases
    # a = 'sunday' -- answer is 3
    # b = 'saturday' -- answer is 3

    m = len(a)
    n = len(b)
    d = np.zeros([m+1, n+1])

    # Initialization
    # The delete cost is defined as 1 for this case
    # The insert cost is defined as 1 for this case
    # delete_cost = 1
    # insert_cost = 1
    for i in range(1, m+1):
        d[i,0] = i
    for j in range(1, n+1):
        d[0,j] = j

    # Dynamic programming
    for j in range(1, n+1):
        for i in range(1, m+1):
            if a[i-1] == b[j-1]:
                subcost = 0
            else:
                subcost = 1
            d[i,j] = min( d[i-1, j] + 1, d[i, j-1] + 1, d[i-1, j-1] + subcost)

    return np.int(d[m,n])

