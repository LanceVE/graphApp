def checkGraph(adjacency_list):
    is_directed = False
    has_negative_cycle = False
    
    for node, neighbors in adjacency_list.items():
        for neighbor, weight in neighbors.items():
            if neighbor in adjacency_list and node in adjacency_list[neighbor]:
                if adjacency_list[neighbor][node] != weight:
                    is_directed = True
    
    if is_directed:
        vertices = list(adjacency_list.keys())
        distances = {vertex: float('inf') for vertex in vertices}
        distances[vertices[0]] = 0
        
        for _ in range(len(vertices) - 1):
            for u in vertices:
                for v, weight in adjacency_list[u].items():
                    if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                        distances[v] = distances[u] + weight
        
        for u in vertices:
            for v, weight in adjacency_list[u].items():
                if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                    has_negative_cycle = True
                    break
            if has_negative_cycle:
                #-1 if negative Cycle
                return -1
                break
    #Directed = 1
    #undirected = -1
    #1 if no negative Cycle
    return 1 if is_directed else -1, 1