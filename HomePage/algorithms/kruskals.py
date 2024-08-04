class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            if self.rank[root_x] < self.rank[root_y]:
                self.parent[root_x] = root_y
            elif self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            else:
                self.parent[root_y] = root_x
                self.rank[root_x] += 1
    def get_sets(self):
        sets = {}
        for i in range(len(self.parent)):
            root = self.find(i)
            if root not in sets:
                sets[root] = {i}
            else:
                sets[root].add(i)

        return list(sets.values())
                
def kruskals(graph, numSets):
    states = []
   
    edges = [(weight, int(u), int(v)) for u, neighbors in graph.items() for v, weight in neighbors.items()]
    edges.sort()
    uniqueEdges = remove_duplicate(edges)
    n = len(graph)
    uf = UnionFind(n)
    
    minimum_spanning_tree = []
    for weight, u, v in edges:
        T = []
        if uf.find(u) != uf.find(v):
            numSets -= 1
            minimum_spanning_tree.append((u, v, weight))
            uf.union(u, v)
            edge = 'e'+str(u)+','+str(v)
            for MST_edge in minimum_spanning_tree:
                T.append('e' + str(MST_edge[0]) + ',' + str(MST_edge[1]))
            set = uf.get_sets()
            result = str(set)[1:-1]
            states.append((edge, 'f('+str(u)+ ') =/= '+'f('+str(v) + ')', T, result, numSets))
    add_NoChangeLines(states, uniqueEdges)
    mst = build_mst(states)
    return states, uniqueEdges, mst
    
def remove_duplicate(edges):
    unique_edges = set()
    result = []
    for edge in edges:
        edge_tuple = tuple(sorted(edge))
        if edge_tuple not in unique_edges:
            unique_edges.add(edge_tuple)
            result.append(edge)
    return result

def add_NoChangeLines(states, uniqueEdges):
    changes = [state[0][1:] for state in states]
    full_edges = [f"{tpl[1]},{tpl[2]}" for tpl in uniqueEdges]
    final_item_first_list = changes[-1]
    index = full_edges.index(final_item_first_list)
    truncated_second_list = full_edges[:index+1]
    indexMiss = []
    missElement = []
    for element in truncated_second_list:
        if element not in changes:
            index = truncated_second_list.index(element)
            indexMiss.append(index)
            missElement.append(element)
    for i, index in enumerate(indexMiss):
        u, v = map(int, missElement[i].split(','))
        edge = 'e'+str(u)+','+str(v)
        states.insert(index, (edge, 'f('+str(u)+ ') = '+'f('+str(v) + ')', 'No Change', 'No Change', 'No Change'))
    return states



def build_mst(states):
    mst_edges = []
    if states:
        last_item = states[-1] 
        if isinstance(last_item, tuple) and len(last_item) >= 3 and isinstance(last_item[2], list):
            for pair in last_item[2]:
                if pair.startswith('e'):
                    edge_parts = pair.split(',')
                    if len(edge_parts) == 2:
                        num1, num2 = edge_parts
                        mst_edges.append((num1.strip('e'), num2))
                    else:
                        continue
    return mst_edges
