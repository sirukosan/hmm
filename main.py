from lib import *

states = ['b', 'y', 'n', 'e']
transitions = {('b', 'y'): 0.2,
               ('b', 'n'): 0.8,
               ('y', 'y'): 0.7,
               ('y', 'n'): 0.2,
               ('y', 'e'): 0.1,
               ('n', 'n'): 0.8,
               ('n', 'y'): 0.1,
               ('n', 'e'): 0.1
               }
emissions = {'y': {'A': 0.1, 'C': 0.4, 'G': 0.4, 'T': 0.1},
             'n': {'A': 0.25, 'C': 0.25, 'G': 0.25, 'T': 0.25}
             }
sequence = 'CGCGCGCGCGCGCGCGCGCGCTTTTTTTTTTTT'
F, FP = viterbi(states, transitions, emissions, sequence)
print(traceback(states, FP))
