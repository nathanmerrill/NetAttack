import random
import Communicator
import math

NODES_PER_BOT = 20
NUM_TURNS = 2000

class Node:
    def __init__(self, owner):
        self.owner = owner
        self.strength = 2
        self.safe = False
        self.attacks = dict()

    def grow(self):
        self.strength += 1

    def add_strength(self, node):
        self.attacks[node.owner] = self.attacks.get(node.owner, 0)+node.strength
        node.strength = 0
        
    def resolve_battles(self):
        self.add_strength(self)
        self.strength = max(self.attacks.values())
        self.owner = random.choice([k for k, v in self.attacks.items()
                                    if v == self.strength])
        if self.strength == 0:
            self.safe = True
        self.attacks.clear()
        


if __name__ == "__main__":
    names = list(Communicator.read_bot_list())
    communicators = Communicator.create_bots(permanent=False, names=names)
    active_communicators = communicators[:]
    nodes = map(Node, names*NODES_PER_BOT)
    active_nodes = list(nodes)
    random.shuffle(nodes)
    for _ in xrange(NUM_TURNS):
        strength = [node.strength for node in active_nodes]
        for communicator in active_communicators:
            friendly = ["F" if node.owner == communicator.name else "E"
                        for node in active_nodes]
            message = " ".join([f+str(int(s))
                                for f, s in zip(friendly, strength)])
            response = communicator.send_message(message=message)
            commands = response.split(" ")
            messages = [map(int, command.split(",")) for command in commands]
            for sender, reciever in messages:
                if sender > len(active_nodes) or reciever > len(active_nodes)\
                        or sender < 0 or reciever < 0:
                    raise RuntimeError(communicator.name + " tried to use a node that doesn't exist")
                if active_nodes[sender].owner != communicator.name:
                    raise RuntimeError(communicator.name + " tried to command unowned node")
                if sender is reciever:
                    active_nodes[sender].grow()
                else:
                    active_nodes[reciever].add_strength(active_nodes[sender])
        for node in active_nodes:
            node.resolve_battles()
        active_nodes = [node for node in active_nodes if not node.safe]
        active_owners = set([node.owner for node in active_nodes])
        active_communicators = [comm for comm in active_communicators
                                if comm.name in active_owners]
        if len(active_nodes) == 1:
            break
    points = dict()
    for node in nodes:
        if node.safe:
            points[node.owner] = points.get(node.owner, 0) + 1
    points = list(points.items())
    points.sort(key=lambda tup: tup[1])
    for name, point in points:
        print name+" got "+str(point)+" points"