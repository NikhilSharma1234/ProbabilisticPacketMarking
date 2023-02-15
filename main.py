# Authors: Nikhil Sharma
# Project: Probabilistic Packet Marking
# Full Project Repository: https://github.com/NikhilSharma1234/ProbabilisticPacketMarking
# CPE 445: Internet Security

import sys
from pyvis.network import Network
import random

probability_bank = [0.2, 0.4, 0.5, 0.6, 0.8]
sending_growth_bank = [20, 30, 40, 80, 100]
 
class Packet(object):
    #Constructor
    def __init__(self, node = None): 
        self.node = node

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

def nodeSamplingSingle(branches, normal_packets, attacker_packets, p, growth_factor):
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

    print(iteration)
    print("Growth Factor: " + str(growth_factor))
    print("Normal Packet Amount: " + str(len(normal_packets)))
    print("Attacker Packet Amount: " + str(len(attacker_packets)))
    print([packet.node for packet in normal_packets])
    print([packet.node for packet in attacker_packets])


    #path reconstruction at victim v:
    NodeTable = [] # Intialize Node Table
    for packet in attacker_packets:
        z = next((x for x in NodeTable if x[0] == packet.node), None) # lookup packet.node in NodeTable
        if z != None:
            z[1] += z[1]
        else:
            NodeTable.append([packet.node, 1])
        # Sort table by count
        NodeTable.sort(key = lambda x: x[1])
    print(NodeTable)


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
    p = random.choice(probability_bank)
    growth_factor = random.choice(sending_growth_bank)

    normal_packets = [Packet() for i in range(10)]
    attacker_packets = [Packet() for i in range(10*growth_factor)]

    nodeSamplingSingle(branches, normal_packets, attacker_packets, p, growth_factor)


    
    #Console prints the path from G to A with the edge weights
if __name__ == "__main__":
    main()
