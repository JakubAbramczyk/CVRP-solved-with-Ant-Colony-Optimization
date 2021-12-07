import math
import RegExService
import random
import numpy
from functools import reduce
import sys
import matplotlib.pyplot as plt

#params
alfa = 2
beta = 5
sigm = 3
ro = 0.8
th = 80
fileName = "E-n51-k5.txt"
iterations = 1000
ants = 22

def generateGraph():
    capacityLimit, graph, demand = RegExService.getData(fileName)
    vertices = list(graph.keys())
    vertices.remove(1)
    edges = { (min(a,b),max(a,b)) : numpy.sqrt((graph[a][0]-graph[b][0])**2 + (graph[a][1]-graph[b][1])**2) for a in graph.keys() for b in graph.keys()}
    feromones = { (min(a,b),max(a,b)) : 1 for a in graph.keys() for b in graph.keys() if a!=b }
    return vertices, edges, capacityLimit, demand, feromones, graph

def solutionOfOneAnt(vertices, edges, capacityLimit, demand, feromones):
    solution = list()
    new_ver = vertices[:-1]
    while(len(new_ver)!=0):
        path = list()
        city = 31
        capacity = capacityLimit - demand[city]
        path.append(city)
        while(len(new_ver)!=0):
            probabilities = list(map(lambda x: ((feromones[(min(x,city), max(x,city))])**alfa)*((1/edges[(min(x,city), max(x,city))])**beta), new_ver))
            probabilities = probabilities/numpy.sum(probabilities)
            city = numpy.random.choice(new_ver, p=probabilities)
            capacity = capacity - demand[city]

            if(capacity>0):
                path.append(city)
                new_ver.remove(city)
            else:
                break
        solution.append(path)
    return solution

def rateSolution(solution, edges):
    s = 0
    for i in solution:
        a = 1
        for j in i:
            b = j
            s = s + edges[(min(a,b), max(a,b))]
            a = b
        b = 1
        s = s + edges[(min(a,b), max(a,b))]
    return s

def updateFeromone(feromones, solutions, bestSolution):
    Lavg = reduce(lambda x,y: x+y, (i[1] for i in solutions))/len(solutions)
    feromones = { k : (ro + th/Lavg)*v for (k,v) in feromones.items() }
    solutions.sort(key = lambda x: x[1])
    if(bestSolution!=None):
        if(solutions[0][1] < bestSolution[1]):
            bestSolution = solutions[0]
        for path in bestSolution[0]:
            for i in range(len(path)-1):
                feromones[(min(path[i],path[i+1]), max(path[i],path[i+1]))] = sigm/bestSolution[1] + feromones[(min(path[i],path[i+1]), max(path[i],path[i+1]))]
    else:
        bestSolution = solutions[0]
    for l in range(sigm):
        paths = solutions[l][0]
        L = solutions[l][1]
        for path in paths:
            for i in range(len(path)-1):
                feromones[(min(path[i],path[i+1]), max(path[i],path[i+1]))] = (sigm-(l+1)/L**(l+1)) + feromones[(min(path[i],path[i+1]), max(path[i],path[i+1]))]
    return bestSolution

def main():
    bestSolution = None
    vertices, edges, capacityLimit, demand, feromones, graph = generateGraph()
    for i in range(iterations):
        solutions = list()
        for _ in range(ants):
            solution = solutionOfOneAnt(vertices.copy(), edges, capacityLimit, demand, feromones)
            solutions.append((solution, rateSolution(solution, edges)))
        bestSolution = updateFeromone(feromones, solutions, bestSolution)
        print(str(i)+":\t"+str(int(bestSolution[1])))

    '''DRAWING'''

    x = []
    y = []
    del graph[1]
    for city in graph:
        x.append(graph[city][0])
        y.append(graph[city][1])
    plt.scatter(x, y)

    for idx, car in enumerate(solution):
        x_list = []
        y_list = []
        for city in car:
            x_list.append(graph[city][0])
            y_list.append(graph[city][1])
        plt.plot(x_list, y_list)
    plt.show()
    return bestSolution

if __name__ == "__main__":
    solution = main()

    print("Solution: "+str(solution))
