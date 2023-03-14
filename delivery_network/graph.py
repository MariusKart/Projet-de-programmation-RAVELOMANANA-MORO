from time import perf_counter
class Graph:
    """
    A class representing graphs as adjacency lists and implementing various algorithms on the graphs. Graphs in the class are not oriented. 
    Attributes: 
    -----------
    nodes: NodeType
        A list of nodes. Nodes can be of any immutable type, e.g., integer, float, or string.
        We will usually use a list of integers 1, ..., n.
    graph: dict
        A dictionnary that contains the adjacency list of each node in the form
        graph[node] = [(neighbor1, p1, d1), (neighbor1, p1, d1), ...]
        where p1 is the minimal power on the edge (node, neighbor1) and d1 is the distance on the edge
    nb_nodes: int
        The number of nodes.
    nb_edges: int
        The number of edges.
    """

    def __init__(self, nodes=[]):
        """
        Initializes the graph with a set of nodes, and no edges. 
        Parameters: 
        -----------
        nodes: list, optional
            A list of nodes. Default is empty.
        """
        self.nodes = nodes
        self.graph = dict([(n, []) for n in nodes])
        self.nb_nodes = len(nodes)
        self.nb_edges = 0



    def __str__(self):
        """Prints the graph as a list of neighbors for each node (one per line)"""
        if not self.graph:
            output = "The graph is empty"            
        else:
            output = f"The graph has {self.nb_nodes} nodes and {self.nb_edges} edges.\n"
            for source, destination in self.graph.items():
                output += f"{source}-->{destination}\n"
        return output
    
    def add_edge(self, node1, node2, power_min, dist=1):
        """
        Adds an edge to the graph. Graphs are not oriented, hence an edge is added to the adjacency list of both end nodes. 

        Parameters: 
        -----------
        node1: NodeType
            First end (node) of the edge
        node2: NodeType
            Second end (node) of the edge
        power_min: numeric (int or float)
            Minimum power on this edge
        dist: numeric (int or float), optional
            Distance between node1 and node2 on the edge. Default is 1.
        """
        if node1 not in self.graph:
            self.graph[node1] = []
            self.nb_nodes += 1
            self.nodes.append(node1)
        if node2 not in self.graph:
            self.graph[node2] = []
            self.nb_nodes += 1
            self.nodes.append(node2)

        self.graph[node1].append((node2, power_min, dist))
        self.graph[node2].append((node1, power_min, dist))
        self.nb_edges += 1

    def kruskal_mst(self):
        def find(parent, i):
            if parent[i] != i:
                parent[i] = find(parent, parent[i])
            return parent[i]

        def union(parent, rank, i, j):
            root_i, root_j = find(parent, i), find(parent, j)
            if root_i == root_j:
                return False
            
            if rank[root_i] < rank[root_j]:
                parent[root_i] = root_j
            elif rank[root_i] > rank[root_j]:
                parent[root_j] = root_i
            else:
                parent[root_j] = root_i
                rank[root_i] += 1
                
            return True
        # Convert graph to edge list format
        edges = []
        for node in self.graph.keys():
            for neighbor in self.graph[node]:
                edges.append((node, neighbor[0], neighbor[1]))
        
        # Create parent and rank lists
        parent = {node : node for node in self.nodes}
        rank = {node: 0 for node in self.nodes}
        
        # Sort edges by weight
        edges = sorted(edges, key=lambda e: e[2])
        
        # Initialize empty MST
        mst = Graph()
        
        
        for edge in edges:
            # Check if adding the edge will create a cycle
            if union(parent, rank, edge[0], edge[1]):
                # Add edge to MST
                mst.add_edge(edge[0], edge[1],edge[2])
            
            # Stop when MST is complete
            if len(mst.nodes) == len(self.nodes):
                break
        
        return mst


    def get_path_with_power(self, src, dest, power):
        """
        This function should return a path from source node to destination node in a weighted graph 
        if possible, given a power of a truck, if not it will return none.

        Parameters:
        self (graph)
        src (int) : source node
        dest (int) : destination node
        power (int) :power of the truck

        Returns:
        (list): path from src to dest
        (None): if no path is found
        """
        def dfs(node, visited):
            visited.append(node) # as the dfs traverses the graph, we add the node to the visited list
            if node == dest: # if we have found the destination node, we return the path
                return [node]
            for neighbor in self.graph[node]:
                if neighbor[0] not in visited and power >= neighbor[1]:
                    path = dfs(neighbor[0], visited)
                    if path is not None: # if a path to the destination is found, return the path
                        return [node] + path
            return None # if no path to the destination is found, return None
        
        return dfs(src, []) # call the dfs method to find a path from src to dest


    
        
            



        
        
    """def connected_components(self):
        connected = []
        visited = []

        def dfs(components, node):
            if node not in visited:
                visited.append(node)
                components.append(node)
                for neighboor in self.graph[node]:
                    if neighboor[0] not in visited:
                        dfs(components, neighboor[0])
        for node in self.nodes:
            if node not in visited:
                components = []
                dfs(components, node)
                connected.append(components)
        return connected"""
    def connected_components(self):
        L=[]
        n=self.nb_nodes
        #A firt loop to create a list L of lists of direct neighbours for each node
        for i in self.nodes:
            l=[i]+[self.graph[i][c][0] for c in range(len(self.graph[i]))]
            L.append(l)
        #A second loop to concatenate the lists where there are elements in common to have the connected components
        #Each time we concatenate a list i whith a list j, we empty the list j.
        #The loop stops when t=0 which significates that the remaining lists are all empty
        t=1
        while t==1:
            t=0
            for i in range(n):
                if L[i]!=[]:
                    for j in range(n):
                        if L[j]!=[] and i!=j:
                            #If the intersection of the two lists is not empty
                            if list(set(L[i])&set(L[j]))!=[]:
                                #Concatenation eliminating the doubles
                                L[i]=list(set(L[i]+L[j]))
                                #We empty the second list
                                L[j]=[]
                                t=1
        L=[h for h in L if h!=[]]
        return L



                
        
                    
                
        
           



    def connected_components_set(self):
        """
        The result should be a set of frozensets (one per component), 
        For instance, for network01.in: {frozenset({1, 2, 3}), frozenset({4, 5, 6, 7})}
        """
        return set(map(frozenset, self.connected_components()))
    
    def min_power(self, src, dest):
        """
        Should return path, min_power. 
        """
        #we first calculate the max power needed for the entire graph
        pmax=0
        #For that, we look at each edge and if the power needed is higher than our pmax, we replace pmax by this new power
        for i in self.nodes:
            L=[self.graph[i][c][0] for c in range(len(self.graph[i]))]
            for j in L:
                if self.graph[i][L.index(j)][1]>pmax:
                    pmax=self.graph[i][L.index(j)][1]
        #Now, we initiate a loop at a p=pmax level of power and while we can do the traject with this power, we degrowth p by 1 until the traject is not possible for this power p
        p=pmax
        while self.get_path_with_power(src,dest,p)!=None:
            p=p-1
        #Thus, we return p+1, the minimal power needed to get a path from the source to the destination
        return self.get_path_with_power(src,dest,p+1),p+1

    


def graph_from_file(filename):
    """
    Reads a text file and returns the graph as an object of the Graph class.

    The file should have the following format: 
        The first line of the file is 'n m'
        The next m lines have 'node1 node2 power_min dist' or 'node1 node2 power_min' (if dist is missing, it will be set to 1 by default)
        The nodes (node1, node2) should be named 1..n
        All values are integers.

    Parameters: 
    -----------
    filename: str
        The name of the file

    Outputs: 
    -----------
    g: Graph
        An object of the class Graph with the graph from file_name.
    """
    with open(filename, "r") as file:
        n, m = map(int, file.readline().split())
        g = Graph(range(1, n+1))
        for _ in range(m):
            edge = list(map(int, file.readline().split()))
            if len(edge) == 3:
                node1, node2, power_min = edge
                g.add_edge(node1, node2, power_min) # will add dist=1 by default
            elif len(edge) == 4:
                node1, node2, power_min, dist = edge
                g.add_edge(node1, node2, power_min, dist)
            else:
                raise Exception("Format incorrect")
    return g

"""data_path = "/input/routes.1.in"
g=graph_from_file("/home/onyxia/work/Projet-de-programmation/input/network.1.in")
time=0
with open ("/home/onyxia/work/Projet-de-programmation/input/routes.1.in","r") as in_routes_file:
    nb_routes = int(in_routes_file.readline())
    for _ in range(nb_routes):
        t_start = perf_counter()
        src, dest, _ = list(map(int, in_routes_file.readline().split()))
        g.min_power(src, dest)
        t_stop = perf_counter()
        time+=(t_stop-t_start)
print("total time=", time)"""





g=graph_from_file("/home/onyxia/work/Projet-de-programmation/input/network.1.in")
print(g.kruskal_mst())
print(g)