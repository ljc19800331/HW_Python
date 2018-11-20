
import numpy as np

# Encode the words to make it in a list
ENCODINGS = {
    'he': np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    'she': np.array([0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    'is': np.array([0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    'and': np.array([0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    'but': np.array([0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]),
    'not': np.array([0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]),
    'very': np.array([0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]),
    'tall': np.array([0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]),
    'fast': np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]),
    'strong': np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]),
    'short': np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]),
    'slow': np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]),
    'weak': np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
}

# Encode the sentences
# Encode the sentence
def encode_sentence(sentence):
    encodings = [ENCODINGS[word.lower()] for word in sentence[:-1].split(' ')]
    return np.array(encodings)

sen_test = "She is strong and fast but not very tall."
sen_encode_test = encode_sentence(sen_test)
print(sen_encode_test)

# generate data
data = \
[
    ("She is strong and fast but not very tall.", 2),
    ("He is slow but tall and very very strong.", 3),
    ("She is not fast but slow.", -1),
    ("He is slow and very weak.", -3)
]

# generate RNN
# nnet = RNN(spec)

# encode data and apply rnn
sentences = [x[0] for x in data]    # This is the items of each sentence
targets = [x[1] for x in data]      # This is the ground truth
scores = []                         # This is the score for the current results

for sentence in sentences:
    x = encode_sentence(sentence)       # The encode data is a matrix
    # result = nnet.apply(x)
    # scores.append(result.ravel()[-1])

if np.all(np.argsort(targets) == np.argsort(scores)):
    print('Success.')
else:
    print('Not quite.')


np.array([[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         ])