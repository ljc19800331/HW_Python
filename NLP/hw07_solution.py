import numpy as np

def transition_matrix(corpus):
    matrix = np.ones((27,27))
    for word in corpus:
        for index in range(0,len(word)):
            ord_c = ord(word[index])
            if (index == 0):
                matrix[-1,ord_c - 97] += 1
            else:
                matrix[ord(word[index-1])-97,ord_c-97] +=1
        matrix[ord(word[-1])-97,-1] += 1
    for i in range (0,27):
        matrix[i,:] = np.log(matrix[i,:]/np.sum(matrix[i,:]))
    return matrix

def most_likely_word(dictionary, transition_matrix, n):
    index = 0;
    max_prob = -np.Inf
    for i in range(0,len(dictionary)):
        word = dictionary[i]
        if (len(word) == n):
            prob = get_prob(transition_matrix, word)
            if prob > max_prob:
                index = i
                max_prob = prob
    return dictionary[index]

def get_prob(transition_matrix, word):
    ans = 0
    for i in range(0,len(word)):
        if(i == 0):
            ans += transition_matrix[-1,ord(word[i])-97]
        else:
            ans += transition_matrix[ord(word[i-1])-97, ord(word[i])-97]
    ans += transition_matrix[ord(word[-1])-97, -1]
    return ans
