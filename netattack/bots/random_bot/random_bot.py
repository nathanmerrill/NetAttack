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
#Takes each owned node (friendlies), and moves them to a random node
movements = [(index, random.randrange(len(nodes)))
             for index, strength in friendlies]

send_message(movements)
