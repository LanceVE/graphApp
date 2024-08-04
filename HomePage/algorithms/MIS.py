import itertools
from itertools import combinations

def isind(graph, vertices):
    for u in vertices:
        for v in vertices:
            if u != v and v in graph[u]:
                return False
    return True

def maximumindependentset(graph):
    nodes = list(graph.keys())
    max_independent_set = []
    states = []  

    for i in range(len(nodes) + 1):
        for subset in combinations(nodes, i):
            states.append((subset, list(max_independent_set))) 
            if isind(graph, subset):
                if len(subset) > len(max_independent_set):
                    max_independent_set = list(subset)
    
                    states.append((subset, list(max_independent_set)))

    return set(max_independent_set), states