def bellmanford(graph, start):
    dist = {v: float('inf') for v in graph}
    dist[start] = 0
    parent = {v: 'Null' for v in graph}
    num_vertices = len(graph)
    states = []
    for iteration in range(num_vertices):
        # Print the current state before relaxing edges
        print(f"Iteration {iteration + 1}")
        print("Current distances:", dist)
        print("Current parents:", parent)
        dist_changed = False
        for u in graph:
            if u in dist: 
                for v in graph[u]:
                    weight = graph[u][v]
                    if v in dist:  
                        if dist[u] + weight < dist[v]:
                            dist[v] = dist[u] + weight
                            parent[v] = u
                            dist_changed = True
                        print(u, v)
                        print(dist)
                    
        distAdd = [dist[v] for v in sorted(dist.keys())]
        parentAdd = [parent[v] if v in parent else None for v in sorted(dist.keys())]
        states.append((iteration+1, *distAdd, 'Yes', *parentAdd))
        if not dist_changed:
            break

    for u in graph:
        for v in graph[u]:
            weight = graph[u][v]
            if dist[u] + weight < dist[v]:
                raise ValueError("Graph contains a negative-weight cycle")
    final_entry = states[-1]
    final_entry_list = list(final_entry)


    if 'Yes' in final_entry_list:
        index = final_entry_list.index('Yes')
        final_entry_list[index] = 'No'

    if isinstance(final_entry_list[0], int):
        final_entry_list[0] += 1
    modified_entry = tuple(final_entry_list)

    states.append(modified_entry)
    mst_edges = build_mst(parent)
    test = transform_to_single_list(states)
    return test, mst_edges



def transform_to_single_list(data):
    result = []
    for item in data:
        transformed_item = list(item)
        result.append(transformed_item)
    return result



def build_mst(parent):
    mst_edges = []
    for node, p in parent.items():
        if p is not None and p != 'Null':
            edge = (p, node)
            if edge not in mst_edges and (edge[1], edge[0]) not in mst_edges:
                mst_edges.append(edge)
    return mst_edges


