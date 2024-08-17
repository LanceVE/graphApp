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


def build_mst(parent):
    mst_edges = []
    for node, p in parent.items():
        if p is not None and p != 'Null':
            edge = (p, node)
            if edge not in mst_edges and (edge[1], edge[0]) not in mst_edges:
                mst_edges.append(edge)
    return mst_edges


def getDijkNodeColors(nodes, n):
    colors = []
    for entry in nodes:
        first_list, second_list = entry
        
        color_dict = {i: 0 for i in range(n)}
        
        for num in first_list:
            index = int(num)
            if 0 <= index < n:
                color_dict[index] = 1
 
        for num in second_list:
            index = int(num)
            if 0 <= index < n and color_dict[index] == 0:
                color_dict[index] = 2
        
        sorted_colors = sorted(color_dict.items())
        colors.append(sorted_colors)
    return colors


def getDijkEdgeColors(data):
    highlighted_edges = []

    for i in range(len(data)):
        relaxed_node, distances, open_set, closed_set, parent_array = data[i]

        relaxed_node = int(relaxed_node)
        
        # Previous distances from the previous state
        if i == 0:
            previous_distances = [float('inf')] * len(distances)
        else:
            previous_distances = data[i-1][1]

        # Determine edges to highlight by checking distance improvements
        edges_to_highlight = []
        for neighbor in range(len(distances)):
            if neighbor != relaxed_node and distances[neighbor] < previous_distances[neighbor]:
                edges_to_highlight.append((relaxed_node, neighbor))

        highlighted_edges.append( edges_to_highlight)

    return highlighted_edges