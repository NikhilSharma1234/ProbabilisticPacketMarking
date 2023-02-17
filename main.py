# Authors: Nikhil Sharma
# Project: Probabilistic Packet Marking
# Full Project Repository: https://github.com/NikhilSharma1234/ProbabilisticPacketMarking
# CPE 445: Internet Security

import sys
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

def nodeSamplingSingle(branches, p, growth_factor):
    normal_packets = [NodePacket() for i in range(10)]
    attacker_packets = [NodePacket() for i in range(10*growth_factor)]
    iteration = 0
    for branch in branches:
        if (iteration == 1):
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
    path = []
    iteration = 0
    for node in NodeTable[::-1]:
        if (iteration == 6):
            break
        if node[0] != None:
            path.append(node[0])
            iteration += 1
    attacker_one = [5, 9, 12, 8, 7, 6]
    return path == attacker_one
    
def nodeSamplingDouble(branches, p, growth_factor):
    normal_packets = [NodePacket() for i in range(10)]
    attacker_packets = [NodePacket() for i in range(10*growth_factor)]
    iteration = 0
    for branch in branches:
        if (iteration == 0 or iteration == 1):
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
    path_one = []
    path_two = []
    iteration = 0
    for node in NodeTable[::-1]:
        if node[0] != None and iteration <= 5:
            path_one.append(node[0])
            iteration += 1
        elif node[0] != None and iteration <= 11:
            path_two.append(node[0])
            iteration += 1
    attacker_one = [5, 9, 12, 8, 7, 6]
    attacker_two = [5, 4, 3, 2, 1, 19]
    return path_one == attacker_one and path_two == attacker_two
    

def edgeSamplingSingle(branches, p, growth_factor):
    normal_packets = [EdgePacket() for i in range(10)]
    attacker_packets = [EdgePacket() for i in range(10*growth_factor)]
    iteration = 0
    for branch in branches:
        if (iteration == 1):
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
        else:
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

    all_packets = normal_packets + attacker_packets
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

    attacker_one = ['v', 5, 9, 12, 8, 7, 6]
    success_set = newTree.paths_to_leaves()
    success = False
    if attacker_one in success_set:
        success = True
    
     # newTree.show()
    return success

def edgeSamplingDouble(branches, p, growth_factor):
    normal_packets = [EdgePacket() for i in range(10)]
    attacker_packets = [EdgePacket() for i in range(10*growth_factor)]
    iteration = 0
    for branch in branches:
        if (iteration == 0 or iteration == 1):
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
        else:
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

    all_packets = normal_packets + attacker_packets
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
    success_one, success_two = False, False

    if attacker_one in success_set:
        success_one = True

    if attacker_two in success_set:
        success_two = True
    # newTree.show()
    
    return success_one, success_two


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

    p = 0.4
    growth_factor = 100

    # Uncomment for single attacker results
    total_success = 0
    print("Growth Factor x: " + str(growth_factor))
    print("Marking Probability p: " + str(p))
    for index in range(1, 101):
        success = nodeSamplingSingle(branches, p, growth_factor)
        if (success):
            total_success += 1
    print("Node Sampling w/ Single Attacker Identification Rate: " + str(total_success) + "%\n")

    total_success = 0
    print("Growth Factor x: " + str(growth_factor))
    print("Marking Probability p: " + str(p))
    for index in range(1, 101):
        success = edgeSamplingSingle(branches, p, growth_factor)
        if (success):
            total_success += 1
    print("Node Sampling w/ Single Attacker Identification Rate: " + str(total_success) + "%")
    

    # Uncomment for two attacker results
    # total_success = 0
    # print("Growth Factor x: " + str(growth_factor))
    # print("Marking Probability p: " + str(p))
    # for index in range(1, 101):
    #     success = nodeSamplingDouble(branches, p, growth_factor)
    #     if (success):
    #         total_success += 1
    # print("Node Sampling w/ Double Attacker Identification Rate: " + str(total_success) + "%")

    # total_success = 0
    # print("Growth Factor x: " + str(growth_factor))
    # print("Marking Probability p: " + str(p))
    # for index in range(1, 101):
    #     success_one, success_two = edgeSamplingDouble(branches, p, growth_factor)
    #     if (success_one and success_two):
    #         total_success += 1
    # print("Edge Sampling w/ Double Attacker Identification Rate: " + str(total_success) + "%")



    
    #Console prints the path from G to A with the edge weights
if __name__ == "__main__":
    main()
