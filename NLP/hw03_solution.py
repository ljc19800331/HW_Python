# Word stemming
import re
import nltk
import numpy as np

def mordernize():

    macbeth = nltk.corpus.gutenberg.raw('shakespeare-macbeth.txt')
    scene5 = macbeth[macbeth.find('Scena Quinta.') + len('Scena Quinta.'):macbeth.find('Scena Sexta.')]
    # np.savetxt('hw3.txt', scene5, delimiter=" ")

    with open('/home/maguangshen/PycharmProjects/NLP/test') as file:
        org = file.read()

    org = scene5

    # step one
    org = re.sub(r'(?:yes)\b', r'ys', org)
    org = re.sub(r'(?:wes)\b', r'ws', org)

    # step two
    org = re.sub(r'(?:esse)$', r'ess', org)
    org = re.sub(r"(?:(?<=[aeiou][aeiou][b-df-hj-np-tv-z]))e\b", r'\1', org)

    # step three
    org = re.sub(r"(?:(?<=[b-df-hj-np-tv-z][aeiou][b-df-hj-np-tv-z])('st))\b", r'\1', org)
    org = re.sub(r"(?:(?<=[b-df-hj-np-tv-z][aeiou][b-df-hj-np-tv-z])('d))\b", "ed", org)

    print("The original text is ", org)

if __name__ == "__main__":
    mordernize()


# (?:(?<=[aeiou][aeiou][b-df-hj-np-tv-z]))e\b|(?:yes)$|(?:wes)\b|(?:(?<=[b-df-hj-np-tv-z][aeiou][b-df-hj-np-tv-z])('st))\b|(?:(?<=[b-df-hj-np-tv-z][aeiou][b-df-hj-np-tv-z])('d))\b