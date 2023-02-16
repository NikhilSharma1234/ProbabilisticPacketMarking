# Authors: Nikhil Sharma
# Project: Probabilistic Packet Marking
# Full Project Repository: https://github.com/NikhilSharma1234/ProbabilisticPacketMarking
# CPE 445: Internet Security

import sys
from pyvis.network import Network
from treelib import Node, Tree
import random

class NodePacket(object):
    #Constructor
    def __init__(self, node = None): 
        self.node = node

class EdgePacket(object):
    #Constructor
    def __init__(self, start = None, end = None, distance = 0) -> None:
        self.start = start
        self.end = end
        self.distance = distance

def generateVisual(branches, routers):
    # Simulates pyvis graph visualizer
    net = Network()

    # Add nodes to graph
    for router in routers:
        net.add_node(router, label=str(router))

    # Add edges to graph
    for branch in branches:
        for router in range(0, len(branch) - 1):
            net.add_edge(branch[router], branch[router+1], physics=False)

    # Pop browser and show graph
    # net.show("nodes.html")

def nodeSamplingSingle(branches, p, growth_factor, multiple):
    normal_packets = [NodePacket() for i in range(10)]
    attacker_packets = [NodePacket() for i in range(10*growth_factor)]
    iteration = 0
    for branch in branches:
        if (iteration == 1 or iteration == 0):
            for router in branch:
                for packet in attacker_packets:
                    x = random.randint(0, 10)/10
                    if x <= p:
                        packet.node = router
        else:
            for router in branch:
                for packet in normal_packets:
                    x = (random.randint(0, 10))/10
                    if x <= p:
                        packet.node = router
        iteration += 1

    print(iteration)
    print("Growth Factor: " + str(growth_factor))
    print("Normal Packet Amount: " + str(len(normal_packets)))
    print("Attacker Packet Amount: " + str(len(attacker_packets)))
    print([packet.node for packet in normal_packets])
    print([packet.node for packet in attacker_packets])

    all_packets = normal_packets + attacker_packets
    #path reconstruction at victim v:
    NodeTable = [] # Intialize Node Table
    for packet in all_packets:
        z = next((x for x in NodeTable if x[0] == packet.node), None) # lookup packet.node in NodeTable
        if z != None:
            z[1] += z[1]
        else:
            NodeTable.append([packet.node, 1])
        # Sort table by count
        NodeTable.sort(key = lambda x: x[1])
    print(NodeTable)

def edgeSamplingSingle(branches, p, growth_factor, multiple):
    normal_packets = [EdgePacket() for i in range(10)]
    attacker_packets = [EdgePacket() for i in range(10*growth_factor)]
    iteration = 0
    for branch in branches:
        if (iteration == 1 or iteration == 0):
            for router in branch:
                for packet in attacker_packets:
                    x = random.randint(0, 10)/10
                    if x <= p:
                        packet.start = router
                        packet.distance = 0
                    else:
                        if packet.distance == 0:
                            packet.end = router
                        packet.distance += 1
        elif (iteration == 2 or iteration == 3):
            for router in branch:
                for packet in normal_packets:
                    x = random.randint(0, 10)/10
                    if x <= p:
                        packet.start = router
                        packet.distance = 0
                    else:
                        if packet.distance == 0:
                            packet.end = router
                        packet.distance += 1
        iteration += 1

    print(iteration)
    print("Growth Factor: " + str(growth_factor))
    print("Normal Packet Amount: " + str(len(normal_packets)))
    print("Attacker Packet Amount: " + str(len(attacker_packets)))
    # print([packet.node for packet in normal_packets])
    # print([packet.node for packet in attacker_packets])
    all_packets = normal_packets + attacker_packets
    iterator = 0
    #path reconstruction at victim v:
    tree = Tree()
    tree.create_node("V", "v")
    for packet in all_packets:
        try:
            if packet.distance == 0:
                tree.create_node(packet.start, packet.start, parent="v", data=0)
            else:
                tree.create_node(packet.start, packet.start, parent=packet.end, data=packet.distance)
        except:
            None
    newTree = Tree(tree)
    for node in tree.all_nodes_itr():
        if len(str(node.identifier)) > 9:
            newTree.remove_node(node.identifier)

    attacker_one = ['v', 5, 4, 3, 2, 1, 19]
    attacker_two = ['v', 5, 9, 12, 8, 7, 6]
    success_set = newTree.paths_to_leaves()
    print(success_set)
    if attacker_one in success_set:
        print("Attacker 1: Success")
    else:
        print("Attacker 1: Failed")

    if multiple and attacker_two in success_set:
        print("Attacker 2: Success")
    else:
        print("Attacker 2: Failed")
    newTree.show()


def main():
    # Initialize graph variables
    routers = []
    for i in range(1, 21):
        routers.append(i)
    print(routers)

    # Create branches
    branches = [[19, 1, 2, 3, 4, 5],
                [6, 7, 8, 12, 9, 5],
                [13, 10, 17, 11, 12, 9, 5],
                [14, 15, 16, 18, 20, 5]]

    generateVisual(branches, routers)
    p = 0.4
    growth_factor = 1000

    # nodeSamplingSingle(branches, p, growth_factor, True)

    edgeSamplingSingle(branches, p, growth_factor, True)


    
    #Console prints the path from G to A with the edge weights
if __name__ == "__main__":
    main()
