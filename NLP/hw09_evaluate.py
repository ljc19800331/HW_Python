"""Assignment 09: Word Features.

ECE 590: Natural Language Processing
Patrick Wang
"""

import nltk
from hw09_solution import related_words

def test_related():
    n = 10
    word = 'play'
    print('The first word is', related_words(word, n))
    word = 'jury'
    print('The second word is', related_words(word, n))

if __name__ == "__main__":
    test_related()
