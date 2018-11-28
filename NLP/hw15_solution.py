# referenced from github code: https://github.com/RobMcH/CYK-Parser
# REF: https://www.youtube.com/watch?v=MIlQwfMZ8O4  -- important example
# REF: https://www.youtube.com/watch?v=CFEGKVjEH1Q&t=1172s

# An complicated solution for the parser problem
# Algorithm:
# 1. 1 by 1 -- Fill in the diagonal components
# 2. 2 by 2 --
# 3. 3 by 3 --

# PS:
# The final goal is that we have the probability to know which sentence (after parser) can we get the most likely result
# So the grammar should include the probability distribution
# The most important result in this case is the
# The most important

# Algorithm introduction
# 1. For

'''

// Step 1: Focus on the first layer
# The first step (nonterm means the empty block) # The first layer
    for i = 0; i < #(words); i++
        for A in nonterms
            if A -> words[i] in grammar
                score[i][i+1][A] = P(A -> words[i]);

// Handle unaries -- This is for the special case
# step 2 -- this is a special case -- look at the video on youtube
    boolean added = true
    while added
        added = false
         for A,B in nonterms
            if score[i][i+1][B] > 0 && A -> B in grammar
                prob = P(A -> B) * score[i][i+1][B]
                if (prob > score[i][i+1][A])
                    score[i][i+1][A] = prob
                    back[i][i+1][A] = B
                    added = true

// Go over for the second layer
    prob = score[begin][split][B] * score[split][end][C] * P(A -> BC)
    if (prob > score[begin][end][A])
        score[begin][end][A] = prob
        back[begin][end][A] = mew Triple(split, B, C)

// Again: handle unaries:
    boolean added = true
        while added
            added = false
             for A,B in nonterms
                if score[i][i+1][B] > 0 && A -> B in grammar
                    prob = P(A -> B) * score[i][i+1][B]
                    if (prob > score[i][i+1][A])
                        score[i][i+1][A] = prob
                        back[i][i+1][A] = B
                        added = true

// Step 3:
    for split = begin + 1 to end - 1
        for A,B,C in nonterms
            prob = score[begin][split][B] * score[split][end][C] * P(A -> BC)
            if prob > score[begin][end][A]
                score[begin][end][A] = prob
                back[begin][end][A] = mew Triple(split, B, C)

// step 4: PRINT The parser tree
based on the largest probability

'''

class Node:
   def __init__(self, symbol, child1, child2 = None):
       self.symbol = symbol
       self.child1 = child1
       self.child2 = child2

class Parser:

   def __init__(self, grammar, sentence):
       self.parse_table = None
       self.prods = {}
       self.grammar = []
       self.pos = []
       self.import_grammar(grammar)
       print("check")
       self.input = sentence.split()

   def import_grammar(self, grammar):

       print("check")
       for rule in grammar:
           print(rule)
           if type(rule.right) == tuple:
               self.grammar.append(rule)
           elif type(rule.right) == list:
               self.pos.append(rule)

   def parse(self):

       print("check")

       length = len(self.input)
       self.parse_table = [[[] for _ in range(length - y)] for y in range(length)]

       # Set the first row as the words
       for i, word in enumerate(self.input):
           for rule in self.pos:
               if word in rule.right:
                   self.parse_table[0][i].append(Node(rule.left, word))

       for words_to_consider in range(2, length + 1):
           for starting_cell in range(0, length - words_to_consider + 1):
               for left_size in range(1, words_to_consider):

                   right_size = words_to_consider - left_size
                   left_cell = self.parse_table[left_size - 1][starting_cell]
                   right_cell = self.parse_table[right_size - 1][starting_cell + left_size]

                   for rule in self.grammar:
                       left_nodes = [n for n in left_cell if n.symbol == rule.right[0]]
                       if left_nodes:
                           right_nodes = [n for n in right_cell if n.symbol == rule.right[1]]
                           self.parse_table[words_to_consider - 1][starting_cell].extend(
                               [Node(rule.left, left, right) for left in left_nodes for right in right_nodes]
                           )

def generate_tree(node):
   if node.child2 == None:
       return "{%s}: '{%s}'" % (node.symbol, node.child1)
   else:
       return "{%s}:\n   {%s} \n   {%s}" % (node.symbol, generate_tree(node.child1), generate_tree(node.child2))


def print_parse_trees(data, rules):
   parser = Parser(rules,data)
   parser.parse()
   parser.print_tree()

class Node:
   def __init__(self, symbol, child1, child2 = None):
       self.symbol = symbol
       self.child1 = child1
       self.child2 = child2


class Parser:
   def __init__(self, grammar, sentence):
       self.parse_table = None
       self.prods = {}
       self.grammar = []
       self.pos = []
       self.import_grammar(grammar)
       self.input = sentence.split()

   def import_grammar(self,grammar):
       for rule in grammar:
           if type(rule.right) == tuple:
               self.grammar.append(rule)
           elif type(rule.right) == list:
               self.pos.append(rule)

   def parse(self):



       length = len(self.input)
       self.parse_table = [[[] for _ in range(length - y)] for y in range(length)]

       for i, word in enumerate(self.input):
           for rule in self.pos:
               if word in rule.right:
                   self.parse_table[0][i].append(Node(rule.left, word))
       for words_to_consider in range(2, length + 1):
           for starting_cell in range(0, length - words_to_consider + 1):
               for left_size in range(1, words_to_consider):
                   right_size = words_to_consider - left_size

                   left_cell = self.parse_table[left_size - 1][starting_cell]
                   right_cell = self.parse_table[right_size - 1][starting_cell + left_size]

                   for rule in self.grammar:
                       left_nodes = [n for n in left_cell if n.symbol == rule.right[0]]
                       if left_nodes:
                           right_nodes = [n for n in right_cell if n.symbol == rule.right[1]]
                           self.parse_table[words_to_consider - 1][starting_cell].extend(
                               [Node(rule.left, left, right) for left in left_nodes for right in right_nodes]
                           )

   def print_tree(self):

       start_symbol = self.grammar[0].left
       final_nodes = [n for n in self.parse_table[-1][0] if n.symbol == start_symbol]
       if final_nodes:
          print("\nPossible parse(s):")
          trees = [generate_tree(node) for node in final_nodes]
          for tree in trees:
             print(tree)
       else:
          print("The given sentence is not contained in the language produced by the given grammar!")


def generate_tree(node):
   if node.child2 == None:
       return "{%s}: '{%s}'" % (node.symbol, node.child1)
   else:
       return "{%s}:\n   {%s} \n   {%s}" % (node.symbol, generate_tree(node.child1), generate_tree(node.child2))


def print_parse_trees(data, rules):
   parser = Parser(rules,data)
   parser.parse()
   parser.print_tree()
