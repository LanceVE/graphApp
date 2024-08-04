import heapq

def prims(graph):
    V = len(graph)
    selected = [False] * V
    no_edge = 0
    edges = []
    parent = [-1] * V
    open_queue = []
    closed_queue = []
    states = []

    selected[0] = True
    closed_queue.append(0)
    reachable = reachable_nodes(graph, '0')
    initial = ['Null'] * V

    
    for index in reachable:
        initial[int(index)] = 'v0'

    distances = {str(node): float('inf') for node in range(V)}
    distances['0'] = 0

    states.append((0, list(distances.values()), open_queue, closed_queue, initial))


    while no_edge < V - 1:
        minimum = float('inf')
        x = 0
        y = 0
        for i in range(V):
            if selected[i]:
                for j in graph[str(i)]:
                    if (not selected[int(j)]) and graph[str(i)][j]:
                        if minimum > graph[str(i)][j]:
                            minimum = graph[str(i)][j]
                            x = i
                            y = int(j)
        
        edges.append((x, y, graph[str(x)][str(y)]))
        parent[y] = x
        selected[y] = True
        open_queue = [i for i in range(V) if not selected[i]]
        closed_queue = [i for i in range(V) if selected[i]]
        no_edge += 1

        for i in open_queue:
            if graph[str(y)].get(str(i), None) is not None:
                distances[str(i)] = min(distances[str(i)], graph[str(y)][str(i)])

        state_parent = ['v' + str(item) if item != -1 else 'Null' for item in parent]
        states.append((y, list(distances.values()), open_queue, closed_queue, state_parent))
 
    mst_edges = build_mst(parent)
    return states, mst_edges



def reachable_nodes(graph, node):
    if node not in graph:
        return []
    return list(graph[node].keys())




def build_mst(parent):
    mst_edges = []
    for node, p in enumerate(parent):
        if p != -1: 
            edge = (p, node)
            if edge not in mst_edges and (edge[1], edge[0]) not in mst_edges:
                mst_edges.append(edge)

    return mst_edges