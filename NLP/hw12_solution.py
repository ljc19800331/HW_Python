# Homework 12
# https://pythonprogramming.net/wordnet-nltk-tutorial/

from collections import Counter
import numpy as np
from nltk.corpus import wordnet

def score_document(doc, positive_seeds, negative_seeds):

    # Find pos and neg scores for the two seeds
    pos = []
    neg = []

    for pos_seed in positive_seeds:
        for syn in wordnet.synsets(pos_seed):
            for l in syn.lemmas():
                if len(l.antonyms()) == 0:
                    pos.append(l.name())
                if len(l.antonyms()) != 0:  # only sym words not ata words
                    continue

    for neg_seed in negative_seeds:
        for syn in wordnet.synsets(neg_seed):
            for l in syn.lemmas():
                if len(l.antonyms()) == 0:
                    neg.append(l.name())
                if len(l.antonyms()) != 0:  # only sym words not ata words
                    continue

    # Count the pos and neg words in the documents
    WordCounter = Counter(doc)
    score = 0
    for word in pos:
        count = WordCounter[word]
        # print(count)
        score = score + count
    for word in neg:
        count = WordCounter[word]
        score = score - count
    print(score)
    return score