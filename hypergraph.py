class HyperGraph():
    V = [] # A list of nodes.
    E = [] # A list of hyperedges.
    elist = {} # A dictionary of lists of indices in the list E of hyperedges to which each node belongs.

    # Example
    # V = [1, 2, 3, 4, 5]
    # E = [[1, 2], [2, 3], [1, 2, 3], [1, 2, 3, 4], [1, 2, 3, 4, 5]]
    # elist = {1: [0, 2, 3, 4], 2: [0, 1, 2, 3, 4], 3: [1, 2, 3, 4], 4: [3, 4], 5: [4]}
    # In this example, elist[1] = [0, 2, 3, 4] implies that node 1 belongs to hyperedges E[0], E[2], E[3], and E[4].

    def __init__(self):
        self.V = []
        self.E = []
        self.elist = {}
        self.label = []

    def construct_hypergraph(self, V, E):
        # Construct a hypergraph from a set of nodes V and a set of hyperedges E.

        self.V = list(V)
        self.E = list(E)
        self.elist = {v: [] for v in self.V}

        for i in range(0, len(E)):
            for v in E[i]:
                self.elist[v].append(i)

        return


    def add_node_to_hyperedge(self, v, e_i):
        # Add node v to hyperedge E[e_i]

        if v not in self.elist:
            print("Error: Given node is not found.")
            exit()
        if e_i < 0 or len(self.E) <= e_i:
            print("Error: Given hyperedge is not found.")
            exit()

        self.E[e_i].append(v)
        self.elist[v].append(e_i)

        return

    def remove_node_from_hyperedge(self, v, e_i):
        # Remove node v from hyperedge E[e_i]

        if v not in self.elist:
            print("Error: Given node is not found.")
            exit()
        if e_i < 0 or len(self.E) <= e_i:
            print("Error: Given hyperedge is not found.")
            exit()

        if e_i not in self.elist[v]:
            print("Error: Given node is not included in the given hyperedge.")
            exit()
        self.elist[v].remove(e_i)

        if v not in self.E[e_i]:
            print("Error: Given node does not belong to the given hyperedge.")
            exit()
        self.E[e_i].remove(v)

        return

    def node_degree(self):
        # Calculate the degree of each node (i.e., the number of hyperedges to which each node belongs).

        nd = {}
        for v in self.V:
            nd[v] = int(len(self.elist[v]))

        return nd

    def num_jnt_node_deg(self):
        # Calculate the number of hyperedges that nodes with degree k and nodes with degree k' share.

        node_degrees = set()
        for v in self.V:
            k = int(len(self.elist[v]))
            node_degrees.add(k)

        jnd = {k1: {k2: 0 for k2 in node_degrees} for k1 in node_degrees}

        for e in self.E:
            s = int(len(e))
            for i in range(0, s-1):
                u = e[i]
                k1 = int(len(self.elist[u]))
                for j in range(i+1, s):
                    v = e[j]
                    k2 = int(len(self.elist[v]))
                    jnd[k1][k2] += 1
                    jnd[k2][k1] += 1

        return jnd

    def node_redundancy_coefficient(self):
        # Calculate the redundancy coefficient of each node.
        # See the following paper for the detail of the redundancy coefficient.
        # Basic notions for the analysis of large two-mode networks, M. Latapy, C. Magnien, N. Del Vecchio, Social networks, 2008.
        
        rc = {v: 0 for v in self.V}
        nd = self.node_degree()

        for v in self.V:
            d = nd[v]

            if d < 2:
                rc[v] = 0
                continue

            for i in range(0, d-1):
                e1 = self.elist[v][i]
                for j in range(i+1, d):
                    e2 = self.elist[v][j]

                    s = set(set(self.E[e1]) & set(self.E[e2])) - {v}
                    if len(s) > 0:
                        rc[v] += 2

            rc[v] /= d*(d-1)

        return rc

    def degree_dependent_node_redundancy_coefficient(self):
        # Calculate the degree-dependent redundancy coefficient of the node (i.e., the average of the redundancy coefficient over the nodes with degree k).

        rc = self.node_redundancy_coefficient()
        nd = self.node_degree()

        node_degrees = set()
        for v in self.V:
            k = int(len(self.elist[v]))
            node_degrees.add(k)

        ddrc = {k: 0 for k in node_degrees}
        n_k = {k: 0 for k in node_degrees}

        for v in self.V:
            k = nd[v]
            ddrc[k] += rc[v]
            n_k[k] += 1

        for k in ddrc:
            if n_k[k] > 0:
                ddrc[k] = float(ddrc[k])/n_k[k]

        return ddrc

    def hyperedge_size(self):
        # Calculate the size of each hyperedge (i.e., the number of nodes that belong to each hyperedge).

        hs = {}

        for e_i in range(0, len(self.E)):
            hs[e_i] = len(self.E[e_i])

        return hs