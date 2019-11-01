from nltk import Tree
from nltk import PCFG
from nltk import induce_pcfg
import pickle
from nltk import Nonterminal

terminal_dict = {}
non_terminal_dict = {}
with open("TrainingTree.txt", 'r') as f:
    lines = f.readlines()
    lines = [line.replace('[', '(').replace(']',')') for line in lines]
    productions = []
    for line in lines:
        t = Tree.fromstring(line)
        productions += t.productions()
S = Nonterminal('S')
grammar = induce_pcfg(S, productions)
print(grammar)

with open('grammer.pickle', 'wb') as handle:
    pickle.dump(grammar, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
