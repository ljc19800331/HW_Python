import numpy as np
import nltk
# prepare data for counting

class LoadData():

    def __init__(self):

        self.Filename = '/home/maguangshen/PycharmProjects/NLP/NLP_Midterm/Data/Data_2_train_tagged.txt'
        self.WORD = set()
        self.TAG = set()
        self.Dic_wordtag = {}
        self.Sen_Word_Tag = []
        self.Sen_Word_Tag_raw = []

    def Read_WordTagTuple(self):

        count_train_word = 0
        count_train_sen = 0

        with open(self.Filename, "r") as f:
            for line in f:
                count_train_sen += 1
                tuple_words = line.split()
                list_WordTag = []
                for tup in tuple_words:
                    count_train_word += 1
                    word_split = tup.split('/')
                    word_split_word = "/".join(word_split[:-1])
                    word_split_tag = word_split[-1]
                    # Word Set
                    if word_split_word not in self.WORD:
                        self.WORD.add(word_split_word)
                    # Tag set
                    if word_split_tag not in self.TAG:
                        self.TAG.add(word_split_tag)
                    # Word and Tag set
                    WordTag = (word_split_word, word_split_tag)
                    list_WordTag.append(WordTag)
                    # Create dictionary for the words and tags
                    if word_split_word in self.Dic_wordtag:
                        set_tag = self.Dic_wordtag[word_split_word]
                        set_tag.add(word_split_tag)
                    else:
                    # create a new tag for the first word
                        set_tag = set([word_split_tag])
                        self.Dic_wordtag[word_split_word] = set_tag
                    # Insert two times for the Trigram and index purpose
                list_WordTag.insert(0, ('*', '*'))
                list_WordTag.insert(0, ('*', '*'))
                self.Sen_Word_Tag.append(list_WordTag)

    def Read_DataRaw(self):
        with open(self.Filename, "r") as f:
            for line in f:
                list_WordTag = []
                tuple_words = line.split()
                for tup in tuple_words:
                    list_WordTag.append(tup)
                self.Sen_Word_Tag_raw.append(list_WordTag)

if __name__ == "__main__":

    test = LoadData()
    test.Filename = '/home/maguangshen/PycharmProjects/NLP/NLP_Midterm/Data_1_test_raw.txt'
    test.Read_DataRaw()
    print(test.Sen_Word_Tag_raw)
