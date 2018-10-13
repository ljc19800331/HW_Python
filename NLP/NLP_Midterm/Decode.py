# The Hmm Decode
# Decode process
from Learn import *
from Load import *

class HmmDecode():

    def __init__(self):

        DataLearn = HmmTrain()
        DataLearn.Dict_Counts()
        DataLearn.Prob_Tran()
        DataLearn.Prob_Emiss()

        self.Dic_wordtag = DataLearn.Dic_wordtag
        self.WORD = DataLearn.WORD
        self.TAG = DataLearn.TAG
        self.Tag_Count = DataLearn.Tag_Count

        self.WordTag_Count = DataLearn.WordTag_Count
        self.Word_Count = DataLearn.Word_Count
        self.BiTag_Count = DataLearn.BiTag_Count
        self.TriTag_Count = DataLearn.TriTag_Count

        self.lamda = 1.0
        self.prob_tran = DataLearn.prob_tran
        self.prob_emiss = DataLearn.prob_emiss

        self.datatestraw = '/home/maguangshen/PycharmProjects/NLP/NLP_Midterm/Data/Data_2_test_raw.txt'
        self.datatesttagged = '/home/maguangshen/PycharmProjects/NLP/NLP_Midterm/Data/Data_2_test_tagged.txt'
        self.Trans_Single = {}

    def Vtb(self, sen):

        sen.insert(0, ('*'))
        T = len(sen)
        K = len(self.TAG)
        self.vtb = {}
        self.bpt = {}
        self.vtb_t = {}
        self.bpt_t = {}

        max_vtb = -100000
        for t in range(1, T):
            word = sen[t]
            word_tag_i = self.gettag(word)
            for tag_i in word_tag_i:
                if t == 1:
                    base_transition = self.getTrans('*', '*', tag_i)
                    base_emission = self.getEmiss(word, tag_i)
                    vtb = base_transition + base_emission
                    tag_tuple = ('*', tag_i)
                    backpointer = ('*', tag_i)
                    if vtb > max_vtb:
                        max_vtb = vtb
                    self.vtb[t, tag_tuple] = max_vtb
                    self.bpt[t, tag_tuple] = ('*', '*')
                else:
                    max_vtb = -100000
                    prob_emiss = self.getEmiss(word, tag_i)
                    word_tag_j = self.gettag(sen[t-1])
                    for tag_j in word_tag_j:
                        tag_tuple = (tag_j, tag_i)
                        word_tag_k = self.gettag(sen[t-2])
                        for tag_k in word_tag_k:
                            prob_trans = self.getTrans(tag_k, tag_j, tag_i)
                            vtb = self.vtb[(t-1, (tag_k, tag_j))] + prob_trans + prob_emiss
                            if vtb > max_vtb:
                                max_vtb = vtb
                                backpointer = (tag_k, tag_j)
                        self.vtb[t, tag_tuple] = max_vtb
                        self.bpt[t, tag_tuple] = backpointer

        # Decode for the sentence
        maxtagidx = []
        for t in range(1, len(sen)):
            word = sen[t]
            max_vtb_decode = -100000
            # print(max_vtb)
            wordtag = None
            # print(word)
            for tag1 in self.gettag(word):
                for tag2 in self.gettag(sen[t-1]):
                    tag_tuple = (tag2, tag1)
                    if self.vtb[t, tag_tuple] > max_vtb_decode:
                        max_vtb_decode = self.vtb[t, tag_tuple]
                        wordtag = (word, tag_tuple)
            maxtagidx.insert(0, wordtag)
        maxtagidx.reverse()
        Sen_tagged = [(tup_obj[0], tup_obj[1][1]) for tup_obj in maxtagidx]
        return Sen_tagged

    def SenTag(self):

        Data_test_tagged = LoadData()
        Data_test_tagged.Filename = self.datatesttagged
        Data_test_tagged.Read_DataRaw()
        Datatest_tagged = Data_test_tagged.Sen_Word_Tag_raw

        count_all = 0
        error_all = 0
        correct_all = 0
        err_rate = 0

        Data_test_raw = LoadData()
        Data_test_raw.Filename = self.datatestraw
        Data_test_raw.Read_DataRaw()
        Datatest_raw = Data_test_raw.Sen_Word_Tag_raw

        print('the lambda is ', self.lamda)

        # for sen_item in Datatest_tagged:
        for i, sen_tagged in enumerate(Datatest_tagged):
            print(i)
            sen_raw = Datatest_raw[i]
            sen_res = self.Vtb(sen_raw)
            print('The labelled sentence is', sen_tagged)
            print('The calculated sentence is', sen_res)
            for j, wordtag_item in enumerate(sen_tagged):
                wordtag_split = wordtag_item.split('/')
                word_test = wordtag_split[0]
                tag_test = wordtag_split[1]
                word_res = sen_res[j][0]
                tag_res = sen_res[j][1]
                count_all += 1
                if tag_res != tag_test:
                    error_all += 1
                if tag_res == tag_test:
                    correct_all += 1
        err_rate = correct_all / count_all
        print('The total number of words is ', count_all)
        print('The count of correct match is', correct_all)
        print('The testing accuracy is', err_rate)

    def gettag(self, word):
        if word  == '*':
            return ('*')
        if word in self.Dic_wordtag:
            return self.Dic_wordtag[word]
        else:
            return self.TAG

    def getTrans(self, tag_k, tag_j, tag_i):
        if (tag_k, tag_j, tag_i) in self.prob_tran:
            return self.prob_tran[(tag_k, tag_j, tag_i)]
        else:
            if (tag_k, tag_j) in self.BiTag_Count:
                return np.log( float(self.lamda) / float(self.BiTag_Count[(tag_k,tag_j)] + self.lamda * len(self.TAG)) )
            else:
                return np.log( float(self.lamda) / float( self.lamda * len(self.TAG) ) )

    def getEmiss(self, word, tag):
        if (word, tag) in self.prob_emiss:
            return self.prob_emiss[(word, tag)]
        else:
            if tag in self.TAG:
                return np.log( float(self.lamda) /  float( self.Tag_Count[tag] + self.lamda * len(self.TAG) ) )
            else:
                return np.log(  float(self.lamda) / float( self.lamda * len(self.TAG) ) )

if __name__ == "__main__":

    test = HmmDecode()
    test.SenTag()