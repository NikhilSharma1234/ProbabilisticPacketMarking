# Authors: Nikhil Sharma
# Project: Probabilistic Packet Marking
# Full Project Repository: https://github.com/NikhilSharma1234/ProbabilisticPacketMarking
# CPE 445: Internet Security

import sys
from pyvis.network import Network
import random

probability_bank = [0.2, 0.4, 0.5, 0.6, 0.8]
 
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

    # marking procedure at router r
    # for packet in packets:
    #     x = random(0, 10)/10
    #     if x <= p:
    #         packet.node = r

    #path reconstruction at victim v:
    # NodeTable = [] # Intialize Node Table
    # for packet in attacker_packets:
    #     z = any(packet.node in sublist for sublist in NodeTable) # lookup packet.node in NodeTable
    #     if z != None:
    #         z[1] += z[1]
    #     else:
    #         NodeTable.append([packet.node, 1])
    #     # Sort table by count
    #     NodeTable.sort(key = lambda x: x[1])

    
    #Console prints the path from G to A with the edge weights
if __name__ == "__main__":
    main()
