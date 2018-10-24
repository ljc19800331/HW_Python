import numpy as np
#vocabulary of length V
#phi of size (k,V), k is number of topic
#theta of size (M,k) M is number of documents
# N number of words need to be generate 

def lda(vocabulary, phi, theta, N):
    '''
    phi = np.array([
    [0.4, 0.4, 0.2, 0.0, 0.0, 0.0],
    [0.0, 0.3, 0.1, 0.0, 0.3, 0.3],
    [0.3, 0.0, 0.2, 0.3, 0.2, 0.0]
    ])
    vocabulary = ['bass', 'pike', 'deep', 'tuba', 'horn', 'catapult']
    N = 100
    
    print(len(phi))
    print(phi[1])
    #exit()
    '''
    LST = [None] * len(phi)
    #no.random.choice
    for i in range(len(phi)):
        lst = [None] * N
        #aa_milne_arr = ['pooh', 'rabbit', 'piglet', 'Christopher']
        #>>> np.random.choice(aa_milne_arr, 5, p=[0.5, 0.1, 0.1, 0.3])
        #array(['pooh', 'pooh', 'pooh', 'Christopher', 'piglet'],
        prob = np.matmul(theta,phi)     # document to word model probability
        print(theta,phi,prob)
        lst_array = np.random.choice(vocabulary, 100, p=(prob[i]))  # given the probability for each word
        LST[i] = lst_array
    return LST
