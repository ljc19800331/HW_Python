# import nltk
# # nltk.download()
# import numpy as np
# nltk.download('brown')
# from nltk.corpus import brown
# brown.categories()
# words = brown.words(categories='news')
# print(words)
# print(len(words))

# import nltk
# from nltk.corpus import brown
# import numpy as np
# import time
#
# stime = time.time()
# sentences = np.array(brown.tagged_sents())
# print(sentences[0])
#
# words = brown.tagged_words()
# tokens, taged = zip(*words)

import nltk
from nltk.corpus import brown

words = brown.tagged_words()
print(words[0])
print(len(words))