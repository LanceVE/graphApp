import heapq
import random

def dijkstras(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]
    parent = {node: 'Null' for node in graph}
    closed = []
    open = [start]

    states = []
    open.remove(start)
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        if current_distance > distances[current_node]:
            continue
        closed.append(current_node)
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                parent[neighbor] = current_node
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
                if neighbor not in open:
                    open.append(neighbor)
        if current_node in open:
            open.remove(current_node)
        states.append((current_node, list(distances.values()), list(open), list(closed), ['v' + str(item) if item != 'Null' else item for item in parent.values()]))
    mst_edges = build_mst(parent)
    return states, mst_edges


def randomstartnode(graph):
    nodes = list(graph.keys())
    startingNode= random.choice(nodes)
    return startingNode


def build_mst(parent):
    print("parent", parent)
    mst_edges = []
    for node, p in parent.items():
        if p is not None and p != 'Null':
            edge = (p, node)
            if edge not in mst_edges and (edge[1], edge[0]) not in mst_edges:
                mst_edges.append(edge)

    print(mst_edges)
    return mst_edges