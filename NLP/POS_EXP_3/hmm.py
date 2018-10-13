import math
RARE_WORD_MAX_FREQ = 5
RARE_SYMBOL = '_RARE_'
def preprocess(train):
	tags=[]
	for eachSentence in train:
		sentenceArray=['START','START']
		for eachWordTag in eachSentence.strip().split():
			sentenceArray.append(eachWordTag.rsplit('/', 1)[-1])
		sentenceArray.append('END')
		tags.append(sentenceArray)

	words=[]
	for eachSentence in train:
		sentenceArray=['START','START']
		for eachWordTag in eachSentence.strip().split():
			sentenceArray.append(eachWordTag.rsplit('/', 1)[0].lower())
		sentenceArray.append('END')
		words.append(sentenceArray)

 	return words,tags


def calculate_emission(words,tags):
	emission = {}
	uniqueTags = {}
	for sent_words, sent_tags in zip(words, tags):
		for word, tag in zip(sent_words, sent_tags):
			emission[(word,tag)] = emission.get((word,tag), 0) + 1
			uniqueTags[tag] = uniqueTags.get(tag,0)+1

	# for i in uniqueTags:
	# 	print emission.get(('and',i),0), uniqueTags[i]


	probabilities = {}
	for word, tag in emission:
		probabilities[(word,tag)] = emission[(word, tag)]*1.0/uniqueTags[tag]
	taglist = set(uniqueTags)
	return probabilities, taglist, uniqueTags

def calculate_transition(tags,taghash):
	transition = {}
	for sent_tags in tags:
		for fromTag, toTag in zip(sent_tags[1:],sent_tags[2:]):
			transition[(fromTag,toTag)] = transition.get((fromTag,toTag),0)+1

	probabilities = {}
	for fromTag,toTag in transition:
		probabilities[(fromTag,toTag)] = transition[(fromTag,toTag)]*1.0/taghash[fromTag]
	return probabilities

def viterbi(testSentence):
	
	possibletags = [x for x in taglist if x not in ['START','END']]

	testWords = testSentence.lower().split()
	for i in range(len(testWords)):
		if testWords[i] not in freq_words:
			testWords[i] = RARE_SYMBOL
	# testWords.append('END')

	trellis_matrix = [[{'source':-1, 'value':0} for x in xrange(len(possibletags))] for y in xrange(len(testWords))]
	for i in range(len(possibletags)):
		trellis_matrix[0][i] = {'source':-1}
		trellis_matrix[0][i]['value'] = transitionProbabilities.get(('START',possibletags[i]),0) * emissionProbabilities.get((testWords[0],possibletags[i]),0)
	##For other words
	lastWordTag = -1
	for i in range(1,len(testWords)):  ## iterator for words
		maxForThisWord = 0
		for j in range(len(possibletags)):  ## iterator for current word tag
			for k in range(len(possibletags)):  ## iterator for previous word tag
				tempValue = trellis_matrix[i-1][k]['value'] * transitionProbabilities.get((possibletags[k],possibletags[j]),0) * emissionProbabilities.get((testWords[i],possibletags[j]),0)
				if maxForThisWord < tempValue:
					maxForThisWord = tempValue
					trellis_matrix[i][j] = {'value':maxForThisWord, 'source':k}
					if i==len(testWords)-1:
						lastWordTag = j

	testWords = testSentence.lower().split()
	# print testWords
	taggedSentence = ""
	i=len(testWords)-1
	tag = j
	while i>0:
		prevTag = trellis_matrix[i][tag]['source']
		taggedSentence = testWords[i-1]+"/"+possibletags[prevTag] + " "+ taggedSentence
		tag = prevTag
		i-=1
	return taggedSentence

def calc_known():
    known_words = set()
    word_c = {}

    for sent_words in words:
        for word in sent_words:
            word_c[word]= word_c.get(word,0) + 1

    for word, count in word_c.iteritems():
        if count > RARE_WORD_MAX_FREQ:
            known_words.add(word)
    return known_words

def replace_rare(known_words):
    for i, sent_words in enumerate(words):
        for j, word in enumerate(sent_words):
            if word not in known_words:
                words[i][j] = RARE_SYMBOL
    return None


if __name__ == "__main__":

	f = open('Data_2_train_tagged.txt', 'r')
	train = f.readlines()
	f.close()
	words,tags=preprocess(train)


	freq_words = calc_known()
	replace_rare(freq_words)

	emissionProbabilities, taglist, uniqueTagHash = calculate_emission(words,tags)

	uniqueTagHash['START'] /=2  ## For trigram it is counted twice
	transitionProbabilities = calculate_transition(tags,uniqueTagHash)
	
	# testSentence = 'He had obtained and provisioned a veteran ship called the Discovery and had recruited a crew of twenty-one , the largest he had ever commanded .'
	testSentence = 'The purpose of this fourth voyage was clear . '
	# testSentence = 'A century of exploration had established that a great land mass , North and South America , lay between Europe and the Indies .'
	testSentence = 'I am a boy . '
	result = viterbi(testSentence)
	print result

	# for i in taglist:
	# 	print emissionProbabilities.get(('provisioned',i),0), i
	
