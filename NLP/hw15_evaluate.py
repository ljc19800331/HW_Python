import numpy as np
from collections import namedtuple
from hw15_solution import print_parse_trees


class Rule:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __str__(self):
        return '{%s} -> {%s}' % (self.left, self.right)

def test_parsing():
    rules = [
        Rule('S', ('NP', 'VP')),
        Rule('NP', ('Det', 'Nominal')),
        Rule('Nominal', ('Nominal', 'PP')),
        Rule('VP', ('Verb', 'NP')),
        Rule('VP', ('X2', 'PP')),
        Rule('VP', ('VP', 'PP')),
        Rule('X2', ('Verb', 'NP')),
        Rule('PP', ('Preposition', 'NP')),
        Rule('NP', ['I', 'pajamas']),
        Rule('Det', ['the', 'a', 'an']),
        Rule('Nominal', ['elephant', 'rhinoceros']),
        Rule('Verb', ['shot', 'rode']),
        Rule('Preposition', ['in', 'on'])
    ]

    # generate data
    data = "I shot an elephant in pajamas"

    print_parse_trees(data, rules)

if __name__ == "__main__":
    test_parsing()
