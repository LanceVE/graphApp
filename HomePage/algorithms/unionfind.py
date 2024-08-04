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
    

    def copy(self):
        new_uf = UnionFind(len(self.parent))
        new_uf.parent = self.parent[:] 
        new_uf.rank = self.rank[:]    
        return new_uf


    def unionfind(Q):
        uf_sets = []
        uf = None  
        while Q:
            operation, params = Q.popleft()
            
            if operation == 'MS':  # Makeset
                n = params
                uf = UnionFind(n)
                uf_sets.append((f"MakeSet from {0} to {n-1}", uf.get_sets())) 
            
            elif operation == 'U':  # Union
                x, y = params
                
                uf.union(x, y)
                print(uf_sets)
                uf_sets.append((f"Union between {x} and {y}", uf.get_sets()))
                print(uf_sets)
                print(" ")

            elif operation == 'F':  # Find
                x = params
                uf_sets.append((f"Find {x}", uf.find(x)))
        return uf_sets