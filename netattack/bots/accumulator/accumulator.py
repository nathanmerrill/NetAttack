import sys
import random

inputs = [(i, x[0], int(x[1:])) for (i, x) in enumerate(sys.argv[1].split())]

own_nodes = sorted([(s,i) for (i,o,s) in inputs if o == 'F'])
targets = sorted([(s,i) for (i,o,s) in inputs if o == 'E'])

if targets:
    out = ""
    j = 0
    total_str = 0
    attackers = []
    for (s,i) in own_nodes:
        attackers += [i]
        if j < len(targets):
            total_str += s
            if targets[j][0] < total_str - 1:
                out += " ".join([str(k) + "," + str(targets[j][1]) for k in attackers]) + " "
                attackers = []
                total_str = 0
                j += 1
    out += " ".join([str(k) + "," + str(k) for k in attackers])
else:
    out = " ".join([str(i) + "," + str(own_nodes[0][1]) for (s,i) in own_nodes])

print(out.rstrip())
sys.stdout.flush()
