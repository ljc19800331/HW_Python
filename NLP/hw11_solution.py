# Solution for homework 11

import numpy as np
from sklearn.decomposition import LatentDirichletAllocation as LDA
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import CountVectorizer

def lda_solve(doc):

    # get term to document matrix
    X, words = tdm(doc)

    # Apply the LDA to the doc new documents
    N_topic = 3
    lda = LDA(n_components = N_topic, random_state = 0)

    # LDA learns the model
    lda.fit(X)

    # predict the topics
    topic = lda.transform(X)

    # transpose the topic model result to get the phi matrix
    phi = topic.transpose()

    return phi, words

def tdm(doc):

    # get the text-document matrix
    N_doc = len(doc)
    dict = {}
    doc_list = []
    words = []

    # convert to list
    for item in doc:
        doc_list.append(item.tolist())

    # get the term document dictionary
    for idx, item in enumerate(doc):
        # print(idx)
        for word in item:
            if word not in dict:
                vec = [0] * len(doc)
                dict[word] = vec
            else:
                vec = dict[word]
                vec[idx] = vec[idx] + 1
                dict[word] = vec

    # get the words list
    for key, value in dict.items():
        words.append(key)

    # get the term document frequency
    N_words = len(words)
    X = np.zeros([N_words, N_doc])
    for idx, item in enumerate(dict.items()):
        X[idx, :] = np.asarray(item[1])

    return X, words

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
    LST = [None] * len(theta)
    # no.random.choice
    for i in range(len(theta)):
        lst = [None] * N
        prob = np.matmul(theta, phi)
        lst_array = np.random.choice(vocabulary, N, p=(prob[i]))
        LST[i] = lst_array
    return LST

def Doc_show():

    vocabulary = ['bass', 'pike', 'deep', 'tuba', 'horn', 'catapult']
    V = len(vocabulary)
    phi = np.array([
        [0.4, 0.4, 0.2, 0.0, 0.0, 0.0],
        [0.0, 0.3, 0.1, 0.0, 0.3, 0.3],
        [0.3, 0.0, 0.2, 0.3, 0.2, 0.0]
    ])
    alpha = [1, 2, 3]
    num_docs = 1000
    theta = []
    for _ in range(num_docs):
        theta.append(np.random.dirichlet(alpha))
    theta = np.array(theta)
    test_theta = np.asarray(theta)
    N = 100
    documents = lda(vocabulary, phi, theta, N)

    return documents

if __name__ == "__main__":
    doc = Doc_show()
    lda_solve(doc)