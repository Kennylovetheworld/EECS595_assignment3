import pickle
import nltk

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

def CKY(line, grammer_list):
    


with open('grammer.pickle', 'rb') as handle:
    grammer = pickle.load(handle)
grammer_list = CNF_grammer_list(grammer)

with open('TestingRaw.txt', 'r') as f:
    testlines = f.readlines()
    for line in testlines:
        tree = CKY(line, grammer_list)


