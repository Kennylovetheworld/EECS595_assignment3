import pickle
import nltk
from nltk import word_tokenize

def CNF(prob, root, rhs_list):
    rules = []
    # find rhs1 amd rhs2
    rhs1 = rhs_list[0]
    if len(rhs_list) == 2:
        rhs2 = rhs_list[1]
        rule = Rule(prob, root, rhs1, rhs2)
        rules.append(rule)
    else:
        rhs2 = '-' 
        for item in rhs_list[1:]:
            rhs2 = rhs2 + item + '-'
        # construct a rule
        rule = Rule(prob, root, rhs1, rhs2)
        rules.append(rule)
        #recurrsion
        if CNF(1, rhs2, rhs_list[1:]) is not None:
            rules.extend(CNF(1, rhs2, rhs_list[1:]))
    return rules

def CNF_grammer_list(grammer):
    grammer_list = []
    for production in grammer.productions():
        print(production)
        if type(production.rhs()[0]) is nltk.grammar.Nonterminal and len(production.rhs()) == 2:
            rule = Rule(production.prob(), str(production.lhs()), str(production.rhs()[0]), str(production.rhs()[1]))
            grammer_list.append(rule)
        if type(production.rhs()[0]) is nltk.grammar.Nonterminal and len(production.rhs()) > 2:
            grammer_list.extend(CNF(production.prob(), str(production.lhs()), [str(item) for item in production.rhs()]))
        if type(production.rhs()[0]) is not nltk.grammar.Nonterminal:
            rule = Rule(production.prob(), str(production.lhs()), str(production.rhs()[0]))
            grammer_list.append(rule)
    return grammer_list

class Rule():
    def __init__(self, prob, root, left, right = None):
        self.root = root # string
        self.left = left # string
        self.right = right # string
        self.prob = prob # float
    def __repr__(self):
        if self.right == None:
            return self.root + " => (" + self.left + ') [' + str(self.prob) + '] \n'
        return self.root + " => (" + self.left + ' ' + self.right + ') [' + str(self.prob) + '] \n'

class traceback_Rule():
    def __init__(self, rule, prob, traceback = None):
        self.rule = rule
        self.prob = prob
        self.traceback = traceback

class Traceback():
    def __init__(self, row1, col1, idx1, row2, col2, idx2):
        self.row1 = row1
        self.col1 = col1
        self.row2 = row2
        self.col2 = col2
        self.idx1 = idx1
        self.idx2 = idx2

def CKY(line, grammer_list):
    words = word_tokenize(line)
    if words == []:
        return None
    print(words)
    table = []
    for i in range(len(words)):
        row = []
        for j in range(len(words)):
            row.append([])
        table.append(row)
    for i in range(len(words)):
        word = words[i]
        for rule in grammer_list:
            if rule.right is None and rule.left == word:
                table[i][i].append(traceback_Rule(rule, rule.prob))
    for col in range(1, len(words)):
        for row in range(col - 1, -1, -1):
            table[row][col].extend(find_traceback_rule(table, row, col, len(words)))
    return table, len(words)

def traceback_table(table, length):
    best_tbrule = None
    best_prob = 0
    #find the best rule
    for item in table[length-1][length-1]:
        if item.rule.root == 'S' and item.rule.prob > best_prob:
            best_tbrule = item 
            best_prob = item.rule.prob
    if best_tbrule == None:
        raise "No available tree for this sentence"
    output = print_tree(best_tbrule, table)
    return output

def print_tree(tbrule, table):
    #handle the terminal
    if tbrule.traceback == None:
        return '[' + tbrule.rule.root + ' ' + tbrule.rule.left + ']'
    #handle the none terminal
    #find the corresponding tbrule
    tbrule1 = table[tbrule.traceback.row1][tbrule.traceback.col1][tbrule.traceback.idx1]
    tbrule2 = table[tbrule.traceback.row2][tbrule.traceback.col2][tbrule.traceback.idx2]
    output = '[' + tbrule.rule.root + ' ' + print_tree(tbrule1) + ' ' + print_tree(tbrule2) + ']'
    return output

def find_traceback_rule(table, row, col, sent_length):
    traceback_rules_list = []
    for i in range(col - row):
        block1 = table[row][row + i]
        block2 = table[row + i + 1][col]
        for idx1, traceback_rules1 in enumerate(block1):
            for idx2, traceback_rules2 in enumerate(block2):
                left = traceback_rules1.rule.root
                right = traceback_rules2.rule.root
                for rule in grammer_list:
                    if rule.right is not None and rule.left == left and rule.right == right:
                        prob = traceback_rules1.prob * traceback_rules2.prob * rule.prob
                        traceback = Traceback(row, row+i, idx1, row+i+1, col, idx2)
                        traceback_rules_list.append(traceback_Rule(rule, prob, traceback))
    return traceback_rules_list

with open('grammer.pickle', 'rb') as handle:
    grammer = pickle.load(handle)
grammer_list = CNF_grammer_list(grammer)

with open('TestingRaw.txt', 'r') as f:
    testlines = f.readlines()
    for line in testlines:
        table, length = CKY(line, grammer_list)
        tree = traceback_table(table, length)


