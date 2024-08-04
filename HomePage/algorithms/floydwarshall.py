def floydwarshall(graph):
    nodes = list(graph.keys())
    n = len(nodes)
    dist = [[(graph[nodes[i]].get(nodes[j], float('inf')) if i != j else 0) for j in range(n)] for i in range(n)]
    parent = [[(i if i != j and graph[nodes[i]].get(nodes[j], float('inf')) != float('inf') else None) for j in range(n)] for i in range(n)]
    
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    parent[i][j] = parent[k][j]  # Update parent

    return dist, parent