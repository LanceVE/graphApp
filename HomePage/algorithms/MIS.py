
from itertools import combinations
import matplotlib
matplotlib.use('Agg')  
import networkx as nx
import matplotlib.pyplot as plt
import os

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


def build_and_save_graphMIS(graph_data, filename, highlight_nodes=None,  pos=None,):
    directory = 'graphApp/static/graphApp/images'
    G = nx.DiGraph()
    

    for node, edges in graph_data.items():
        for adjacent_node, weight in edges.items():
            G.add_edge(node, adjacent_node, weight=weight)
    
    if pos is None:
        pos = nx.spring_layout(G, seed=42) 
    
    plt.figure(figsize=(12, 12))
    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor((255/255, 253/255, 250/255, 1.0))
    
    ax.set_axis_off()
    
    node_color_rgb = (81/255, 40/255, 132/255) 
    highlight_color_rgb = (255/255, 0/255, 0/255)  
    
    node_colors = [highlight_color_rgb if node in highlight_nodes else node_color_rgb for node in G.nodes()]
    

    nx.draw_networkx_nodes(G, pos, node_size=700, node_color=node_colors)
    

    nx.draw_networkx_edges(G, pos, edge_color='black', arrows=True, arrowstyle='-|>', arrowsize=20)
    
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12, label_pos=0.5, font_color='black')
    
    nx.draw_networkx_labels(G, pos, font_size=12, font_color='white')
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    filepath = os.path.join(directory, filename)
    plt.savefig(filepath, bbox_inches='tight', pad_inches=0, facecolor=fig.get_facecolor())
    
    return pos