# Authors: Nikhil Sharma
# Project: Probabilistic Packet Marking
# Full Project Repository: https://github.com/NikhilSharma1234/ProbabilisticPacketMarking
# CPE 445: Internet Security

import sys
from pyvis.network import Network
import random
 
class Graph(object):
    #Constructor
    def __init__(self, graphDictionary, nodes): 
        self.graph = self.fillGraph(graphDictionary, nodes)
        self.nodes = nodes

    #Fill graph with nodes and edge values
    def fillGraph(self, graphDictionary, nodes):
        graph = {}
        for node in nodes:
            graph[node] = {}
        graph.update(graphDictionary)
        for node1, edges in graph.items():
            for node2, value in edges.items():
                if graph[node2].get(node1, False) == False:
                    graph[node2][node1] = value   
        return graph

    #Returns all nodes
    def returnNodes(self):
        return self.nodes

    #Returns edges of a specific node
    def returnEdges(self, node):
        edges = []
        for neighbor in self.nodes:
            if self.graph[node].get(neighbor, False) != False:
                edges.append(neighbor)
        return edges

    #Returns value of an edge between two nodes
    def returnValue(self, node1, node2):
        return self.graph[node1][node2]

def dijkstra(graph, firstNode):
    unvisitedNodes = list(graph.returnNodes())   
    shortestPathValues = {}

    #Set distance to all nodes as infinity
    for node in unvisitedNodes:
        shortestPathValues[node] = [sys.maxsize, ""]

    #Set distance to starting node as 0
    shortestPathValues[firstNode][0] = 0
    previousNodes = {}

    #Find the closest node and update the shortest path to it
    while unvisitedNodes:
        closestNode = unvisitedNodes[0]
        for node in unvisitedNodes:
            if shortestPathValues[node][0] < shortestPathValues[closestNode][0]:
                closestNode = node

        neighbors = graph.returnEdges(closestNode)

        for neighbor in neighbors:
            newPathLength = shortestPathValues[closestNode][0] + graph.returnValue(closestNode, neighbor)[0]
            if newPathLength < shortestPathValues[neighbor][0]:
                shortestPathValues[neighbor][0] = newPathLength
                shortestPathValues[neighbor][1] = graph.returnValue(closestNode, neighbor)[1]
                previousNodes[neighbor] = closestNode
        unvisitedNodes.remove(closestNode)
    
    return previousNodes, shortestPathValues

def dijkstraMod(graph, firstNode):
    unvisitedNodes = list(graph.returnNodes())   
    shortestPathValues = {}

    #Set distance to all nodes as infinity
    for node in unvisitedNodes:
        shortestPathValues[node] = [sys.maxsize, ""]

    #Set distance to starting node as 0
    shortestPathValues[firstNode][0] = 0
    previousNodes = {}

    #Find the closest node and update the shortest path to it
    while unvisitedNodes:
        closestNode = unvisitedNodes[0]
        for node in unvisitedNodes:
            if shortestPathValues[node][0] < shortestPathValues[closestNode][0]:
                closestNode = node
        neighbors = graph.returnEdges(closestNode)
        wired = False
        for neighbor in neighbors:
            newPathLength = shortestPathValues[closestNode][0] + graph.returnValue(closestNode, neighbor)[0]
            if newPathLength < shortestPathValues[neighbor][0] and graph.returnValue(closestNode, neighbor)[1] == "wired":
                wired = True
                shortestPathValues[neighbor][0] = newPathLength
                shortestPathValues[neighbor][1] = graph.returnValue(closestNode, neighbor)[1]
                previousNodes[neighbor] = closestNode
        if wired == False:
            for neighbor in neighbors:
                newPathLength = shortestPathValues[closestNode][0] + graph.returnValue(closestNode, neighbor)[0]
            if newPathLength < shortestPathValues[neighbor][0]:
                wired = True
                shortestPathValues[neighbor][0] = newPathLength
                shortestPathValues[neighbor][1] = graph.returnValue(closestNode, neighbor)[1]
                previousNodes[neighbor] = closestNode
                
        unvisitedNodes.remove(closestNode)
    
    return previousNodes, shortestPathValues
   
def display(previousNodes, graphDictionary, firstNode, lastNode):
    path = []
    node = lastNode
    
    while node != firstNode:
        path.append(node)
        node = previousNodes[node]
    
    path.append(firstNode)
    
    for i in range(0, len(path)-1):
        if graphDictionary[path[i]][path[i+1]][1] == "wireless":
            randomNum = random.randint(0,3)
            if randomNum == 0:
                raise Exception("Wireless node has failed")
        else:
            randomNum = random.randint(0, 19)
            if randomNum == 0:
                raise Exception("Wired node has failed")
        print(path[i] + "   -" + str(graphDictionary[path[i]][path[i+1]]) + "->   ", end ="")
    print(firstNode)

def generateVisual(graphDictionary, nodes):
    # Simulates pyvis graph visualizer
    net = Network()

    # Add nodes to graph
    for node in nodes:
        net.add_node(node, label=str(node))

    # Add edges to graph
    for edge in graphDictionary:
        for data in graphDictionary[edge]:
            net.add_edge(str(edge), str(data), value=2, label=str(graphDictionary[edge][data][0]) + ' ' + graphDictionary[edge][data][1])

    # Pop browser and show graph
    net.show('nodes.html')


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
