import sys
import random

nodes = list(enumerate(sys.argv[1].split(" ")))

friendlies = [(index, strength[1:]) for index, strength in nodes
              if strength[0] == "F"]

enemies = [(index, strength[1:]) for index, strength in nodes
           if strength[0] == "E"]

def send_message(movements):
    print " ".join([str(start)+","+str(stop) for start, stop in movements])


#This is he actual algorithm
#Creates a list of tuples designating to and from locations to move strength
#Takes each owned node (friendlies), randomly decides whether to send them to
#save, send to friendly, or send to enemy

movements = []
for i in xrange(len(friendlies)):
    choice = random.randrange(3 if enemies else 2)
    options = friendlies if choice is 0 \
        else [friendlies[i]] if choice is 1 \
        else enemies
    movements.append((friendlies[i][0], random.choice(options)[0]))

send_message(movements)
