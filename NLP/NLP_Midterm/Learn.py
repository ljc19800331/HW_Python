# Calculate the probability counts for word and tags
# Calculate the transmission and emission matrix and probability
from Load import *
import nltk
from nltk.corpus import brown

class HmmTrain():

    def __init__(self):
        # Counting
        self.WordTag_Count = {}
        self.Tag_Count = {}
        self.Word_Count = {}
        self.BiTag_Count = {}
        self.TriTag_Count = {}
        self.lamda = 1
        self.prob_tran = {}
        self.prob_emiss = {}
        # Load the data in advanced
        DataLoad = LoadData()
        DataLoad.Read_WordTagTuple()
        self.WORD = DataLoad.WORD
        self.TAG = DataLoad.TAG
        self.Dic_wordtag = DataLoad.Dic_wordtag
        self.Tuples_all_Sentence = DataLoad.Sen_Word_Tag

    def BrownLearn(self):

        words = brown.tagged_words()
        data_train = words[0:1000000]
        data_test = words[1000001:]

        self.Brown_WORD = set()
        self.Brown_TAG = set()
        self.Brown_Dic_wordtag = {}
        self.Brown_Sen_Word_Tag = []
        self.Brown_Sen_Word_Tag_raw = []

        self.Brown_WordTag_Count = {}
        self.Brown_Tag_Count = {}
        self.Brown_Word_Count = {}
        self.Brown_BiTag_Count = {}
        self.Brown_TriTag_Count = {}

        words = data_train
        print(words)
        print(len(words))

        for i in range(2, len(words)):
            if words[i][0] not in self.Brown_WORD:
                self.Brown_WORD.add(words[i][0])
            if words[i][1] not in self.Brown_TAG:
                self.Brown_TAG.add(words[i][1])
            if words[i][0] in self.Brown_Dic_wordtag:
                set_tag = self.Brown_Dic_wordtag[words[i][0]]
                set_tag.add(words[i][1])
            else:
                set_tag = set([words[i][1]])
                self.Brown_Dic_wordtag[words[i][0]] = set_tag
            if words[i] in self.Brown_WordTag_Count:
                self.Brown_WordTag_Count[words[i]] += 1
            else:
                self.Brown_WordTag_Count[words[i]] = 1
            # 2. Count the Tags only
            if words[i][1] in self.Brown_Tag_Count:
                self.Brown_Tag_Count[words[i][1]] += 1
            else:
                self.Brown_Tag_Count[words[i][1]] = 1
            # 2. Count the Words only
            if words[i][0] in self.Brown_Word_Count:
                self.Brown_Word_Count[words[i][0]] += 1
            else:
                self.Brown_Word_Count[words[i][0]] = 1
            # 3. Count the Bigram match -- include '*' and '*'
            bin = (words[i - 2][1], words[i - 1][1])
            if bin in self.Brown_BiTag_Count:
                self.Brown_BiTag_Count[bin] += 1
            else:
                self.Brown_BiTag_Count[bin] = 1
            # 4. Count the Trigram match -- include the '*', '*' and 'x'
            tri = (words[i - 2][1], words[i - 1][1], words[i][1])
            if tri in self.Brown_TriTag_Count:
                self.Brown_TriTag_Count[tri] += 1
            else:
                self.Brown_TriTag_Count[tri] = 1

    def Dict_Counts(self):

        for item in self.Tuples_all_Sentence:
            for i in range(2, len(item)):
                # 1. Count the WordTag
                if item[i] in self.WordTag_Count:
                    self.WordTag_Count[item[i]] += 1
                else:
                    self.WordTag_Count[item[i]] = 1
                # 2. Count the Tags only
                if item[i][1] in self.Tag_Count:
                    self.Tag_Count[item[i][1]] += 1
                else:
                    self.Tag_Count[item[i][1]] = 1
                # 2. Count the Words only
                if item[i][0] in self.Word_Count:
                    self.Word_Count[item[i][0]] += 1
                else:
                    self.Word_Count[item[i][0]] = 1
                # 3. Count the Bigram match -- include '*' and '*'
                bin = (item[i-2][1], item[i-1][1])
                if bin in self.BiTag_Count:
                    self.BiTag_Count[bin] += 1
                else:
                    self.BiTag_Count[bin] = 1
                # 4. Count the Trigram match -- include the '*', '*' and 'x'
                tri = (item[i-2][1], item[i-1][1], item[i][1])
                if tri in self.TriTag_Count:
                    self.TriTag_Count[tri] += 1
                else:
                    self.TriTag_Count[tri] = 1

    def Prob_Tran(self):
        v = len(self.TAG)
        for tags_tri, tags_count_tri in self.TriTag_Count.items():
            words_bin = (tags_tri[0], tags_tri[1])
            tags_count_bin = self.BiTag_Count[words_bin]
            p = (tags_count_tri + self.lamda) / (tags_count_bin + self.lamda * v)
            self.prob_tran[tags_tri] = np.log(float(p))

    def Prob_Emiss(self):
        v = len(self.TAG)
        for wordtag_obj, wordtag_count in self.WordTag_Count.items():
            word_count = self.Word_Count[wordtag_obj[0]]                    # The word is 0 and tag is 1
            p = (wordtag_count + self.lamda) / (word_count + self.lamda * v)
            self.prob_emiss[wordtag_obj] = np.log(float(p))

    def Brown_Prob_Tran(self):
        self.Brown_prob_tran = {}
        v = len(self.Brown_TAG)
        for tags_tri, tags_count_tri in self.Brown_TriTag_Count.items():
            words_bin = (tags_tri[0], tags_tri[1])
            tags_count_bin = self.Brown_BiTag_Count[words_bin]
            p = (tags_count_tri + self.lamda) / (tags_count_bin + self.lamda * v)
            self.Brown_prob_tran[tags_tri] = np.log(float(p))

    def Brown_Prob_Emiss(self):
        self.Brown_prob_emiss = {}
        v = len(self.Brown_TAG)
        for wordtag_obj, wordtag_count in self.Brown_WordTag_Count.items():
            word_count = self.Brown_Word_Count[wordtag_obj[0]]                    # The word is 0 and tag is 1
            p = (wordtag_count + self.lamda) / (word_count + self.lamda * v)
            self.Brown_prob_emiss[wordtag_obj] = np.log(float(p))

if __name__ == "__main__":

    test = HmmTrain()
    test.BrownLearn()
    print(test.Brown_WORD)
    print(test.Brown_TAG)
    print(test.Brown_Dic_wordtag)
    print(test.Brown_Sen_Word_Tag)
    print(test.Brown_Sen_Word_Tag_raw)
    print(test.Brown_WordTag_Count)
    print(test.Brown_Tag_Count)
    print(test.Brown_Word_Count)
    print(test.Brown_BiTag_Count)
    print(test.Brown_TriTag_Count)

    # test.Dict_Counts()
    # test.Prob_Tran()
    # test.Prob_Emiss()
    # print(test.prob_tran)
    # print(test.prob_emiss)
