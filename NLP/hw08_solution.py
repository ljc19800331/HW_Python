
import numpy as np

def infer_states(obs, pi, A, B):

    # Initial parameters
    N = len(pi)
    T = len(B[0])
    vtb = np.zeros([N, T])
    bpt = np.zeros([N, T])

    # Initialization with pi
    for s in range(len(pi)):
        vtb[s, 0] = pi[s] * B[s, obs[0]]
        bpt[s, 0] = 0

    # Recursion step
    for t in range(1, T):
        for s in range(N):
            # calculate all the possible values with previous states
            # there is N possible states
            vtb_all = np.zeros(N)
            for s_prime in range(N):
                vtb_all[s_prime] = vtb[s_prime, t - 1] * A[s_prime, s] * B[s, obs[t]]
            vtb[s, t] = np.max(vtb_all)
            bpt[s, t] = np.argmax(vtb_all)  # This returns the index of the argmax pointer

    bestpathprob = np.max(vtb[:, -1])
    bestpathpointer = np.argmax(vtb[:, -1])

    # Method 1: Infer state sequences from viterbi matrix
    # bestpath = np.argmax(vtb, axis = 0)

    # Method 2: Infer state sequences from backtrace (backpointer)
    bestpath = [bestpathpointer]
    # Trace back to the origin
    for i in reversed(range(1, T)):
        idx = np.argmax(bpt, axis=0)
        bestpath.append(np.argmax(bpt[:, i]))
    # reverse output
    bestpath = list(reversed(bestpath))

    return list(bestpath), bestpathprob