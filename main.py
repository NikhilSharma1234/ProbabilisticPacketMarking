# Authors: Nikhil Sharma
# Project: Probabilistic Packet Marking
# Full Project Repository: https://github.com/NikhilSharma1234/ProbabilisticPacketMarking
# CPE 445: Internet Security

import sys
from pyvis.network import Network
import random
 
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
    nodes = ["A", "B", "C", "D", "E", "F", "G", "H"]
    types = ["wireless", "wired"]
    graphDictionary = {}
    for node in nodes:
        graphDictionary[node] = {}
    
    # Create graph data
    graphDictionary["A"]["B"] = [random.randint(1,5), random.choice(list(types))]
    graphDictionary["A"]["C"] = [random.randint(1,5), random.choice(list(types))]
    graphDictionary["B"]["D"] = [random.randint(1,5), random.choice(list(types))]
    graphDictionary["C"]["D"] = [random.randint(1,5), random.choice(list(types))]
    graphDictionary["C"]["G"] = [random.randint(1,5), random.choice(list(types))]
    graphDictionary["D"]["G"] = [random.randint(1,5), random.choice(list(types))]
    graphDictionary["D"]["E"] = [random.randint(1,5), random.choice(list(types))]
    graphDictionary["D"]["F"] = [random.randint(1,5), random.choice(list(types))]
    graphDictionary["F"]["H"] = [random.randint(1,5), random.choice(list(types))]

    # Make graph object
    graph = Graph(graphDictionary, nodes)

    # Generate graph using pyvis
    generateVisual(graphDictionary, nodes)

    # Perform Dijkstras
    previousNodes1, shortestPathValues1 = dijkstra(graph=graph, firstNode="A")
    previousNodes2, shortestPathValues2 = dijkstraMod(graph=graph, firstNode="A")

    targetNode = random.choice(list(nodes))
    
    # Display the dijksta path from A to target node
    try:
        display(previousNodes1, graphDictionary, firstNode="A", lastNode=targetNode)
    except:
        print("Node Failure has occured for the dijkstra algorithm")
    try:
        display(previousNodes2, graphDictionary, firstNode="A", lastNode=targetNode)
    except:
        print("Node Failure has occured for the modified dijkstra algorithm")
    
    #Console prints the path from G to A with the edge weights
if __name__ == "__main__":
    main()
