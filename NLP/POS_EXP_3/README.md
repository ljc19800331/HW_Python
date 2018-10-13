# POS_Tagging

- This is a python implementation of Parts of Speech tagging a corpus using concepts of Hidden Markov Models. Brown corpus is used for 
training the model. You can also find the data in this reopsitory.
- In this program, Bigram HMM and Viterbi algorithm were used to tag the sentences.
- Emission probabilities were computed as the probability of a word being a particular tag.
- Transition probailities were calculated as the probability of a tag occuring after another. Here the probability is considered to be dependent
only on the previous tag, thus it is called Bigram HMM.
- As we can encounter words which are present in the test set but not in the training data, this problem was resolved by marking those words with
RARE tag when their frequency is less that a threshold value. It is considered as a non-frequent word. This is done for the test data as well.
- Also the morphology of words was considered for better accuracy.


### Tags in the corpus
|Tag | Description    |
|:--:|:--------------:|
|IN  | Preposition    |
|JJ	 |Adjective	      |
|NN	 |Singular Noun   |
|NNS |	Plural Noun   |
|PRP |Personal Pronoun|
|VB	 |Verb Base Form  |
|VBD |Verb Past Tense	|
|.	 |Sentence-Final  |

