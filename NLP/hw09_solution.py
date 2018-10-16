import nltk
from nltk.corpus import brown
from collections import Counter
from collections import defaultdict
import numpy as np
from scipy import spatial
import heapq
import operator

def get_tf(training_category):

    # get the term-sentence matrix
    training_category = ['reviews']
    brown.sents(categories=training_category)
    Sents_text = brown.sents(categories=training_category)
    tokens = brown.words(categories=training_category)
    wordCounter = Counter(tokens)
    word_index = 0
    word_dict = {}

    for words in wordCounter:
        temp_array = np.zeros(len(Sents_text))
        for sent_index in range(len(Sents_text)):
            temp_array[sent_index] = Sents_text[sent_index].count(words)
        word_dict[words] = temp_array
        word_index += 1

    return word_dict

def get_idf(Dict_mat, word):

    N_doc = len(Dict_mat.items()[0][1])
    vec_word = Dict_mat[word]
    N_idf = len([i for i in vec_word if i > 0])
    return np.log( N_doc / N_idf)

def get_tfidf(Dict_mat, word_interest, word_obj):

    vec_tf = Dict_mat[word_obj]
    value_idf = get_idf(Dict_mat, word_obj)

    return vec_tf * value_idf

def get_cos(Dict_mat, word_interest, word_obj):

    vec_interest = get_tfidf(Dict_mat, word_interest, word_interest)
    vec_obj = get_tfidf(Dict_mat, word_interest, word_obj)
    cos_interest_obj = 1 - spatial.distance.cosine(vec_interest, vec_obj)
    return cos_interest_obj

def related_words(word_interest, n):

    # Load the pre-trained numpy dataset
    Dict_mat = np.load('/home/maguangshen/PycharmProjects/HW_Python/Dict_Train_review.npy').item()

    # cos function for tfidf
    Dict_cos = {}
    for idx, item in enumerate(Dict_mat):
        if ((idx % 1000) == 0):
            print(idx)
        Dict_cos[item] = get_cos(Dict_mat, word_interest, item)
    print('All the cos results in the dict is ', Dict_cos)

    # Return the n sorted list
    Dict_sorted = sorted(Dict_cos.items(), key=operator.itemgetter(1), reverse=True)
    print(Dict_sorted)

    List_words = []
    for item in Dict_sorted:
        List_words.append(str(item[0]))
    print('The list of related words is ', List_words)

    return List_words

if __name__ == "__main__":
    word = 'play'
    n  = 10
    related_words(word, n)






