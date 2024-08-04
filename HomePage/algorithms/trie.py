import os
import matplotlib.pyplot as plt
import networkx as nx

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def visualize(self, filename):
        directory = 'graphApp/static/graphApp/images'
        G = self.to_networkx()


        pos = nx.spring_layout(G)

        node_color_rgb= (81/255, 40/255, 132/255)

        plt.figure(figsize=(12, 8))
        nx.draw(G, pos, with_labels=True, node_size=700, node_color = node_color_rgb, font_size=10, font_color = 'white')
    
        for edge in G.edges():
            parent_label = edge[0]
            child_label = edge[1]
            if len(child_label) > len(parent_label) and child_label.startswith(parent_label):
                nx.draw_networkx_edges(G, pos, edgelist=[edge], edge_color='black')

        filepath = os.path.join(directory, filename)
        plt.savefig(filepath)
        plt.close() 
        return filepath

    def to_networkx(self):
        G = nx.DiGraph()
        self._add_to_graph(self.root, '', G)
        return G

    def _add_to_graph(self, node, label, G):
        for char, child_node in node.children.items():
            G.add_edge(label, label + char)
            self._add_to_graph(child_node, label + char, G)
        if node.is_end_of_word:
            G.nodes[label]['is_end_of_word'] = True
    
def trieBuild(words):
    trie = Trie()
    for word in words:
        trie.insert(word)
    return trie