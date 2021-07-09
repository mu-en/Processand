#!/usr/bin/env python
# coding: utf-8

# In[1]:


import networkx as nx

class Graph(nx.Graph):
    
    '''
        Graph class is based on networkx graph object
    '''
    def __init__(self, Graph):
        self.G = Graph
        
    def get_shortest_path(self, start_node_id, end_node_id):
    
        # if start_node_id is equal to end_node_id, return start_node_id
        if end_node_id == start_node_id:
            return list(start_node_id)
        
        # adjacency of network G
        G_path = self.G.adj

        # pred(succ) is a dictionary for forward(reverse) node
        pred = {start_node_id: None}
        succ = {end_node_id: None}

        # forward start node and reverse start node
        forward = [start_node_id]
        reverse = [end_node_id]
        
        # Find the path from start_node_id to node_w to end_node_id
        a, b=0, 0 # if a=1, exit while loop;if b=1, exit for loop
        while forward and reverse:
            # Find the path from the start_node_id to the node_w
            if len(forward) <= len(reverse):
                this_level = forward
                forward = []
                for v in this_level:
                    for w in G_path[v]:
                        if w not in pred:
                            forward.append(w)
                            pred[w] = v
                        if w in succ:  # Path found
                            a, b = 1, 1
                            break
                    if b==1: # Exit for loop
                        break
                
            # Find the path from end_node_id to node_w
            else:
                this_level = reverse
                reverse = []
                for v in this_level:
                    for w in G_path[v]:
                        if w not in succ:
                            succ[w] = v
                            reverse.append(w)
                        if w in pred:  # Path found
                            a, b = 1, 1
                            break
                    if b==1: # Exit for loop
                        break
            # Exit while loop               
            if a==1:
                break      
            
        # build path from start_node_id to node_w to end_node_id
        path = []
        # from start_node_id to node_w
        while w is not None:
            path.append(w)
            w = pred[w]
        path.reverse()
        
        # from node_w to end_node_id
        w = succ[path[-1]]
        while w is not None:
            path.append(w)
            w = succ[w]
            
        return path
    
    def get_subtrees(self, selected_node_ids):
        list_of_edge = []
        # Find all edges of selected_node_ids and add to list_of_edge
        for start in selected_node_ids:
            stack = [(start, iter(self.G[start]))]
            while stack:
                parent, children = stack[-1]
                try:
                    child = next(children)
                    list_of_edge.append((parent, child))

                except StopIteration:
                    stack.pop()

        T = nx.Graph()
        for i in selected_node_ids:
            T.add_node(i)
        T.add_edges_from(list_of_edge) # add a list of edges to network T
        
        #Check if there are any cycles in network T
        gnodes = set(T.nodes())
        cycles = []
        while gnodes:  
            # Find the cycle from node 1, and so on
            root = gnodes.pop()
            # list of node we want to check
            stack = [root]
            # pred is a dictionary for find cycle path
            pred = {root: root}
            # used is a dictionary for find cycle
            used = {root: set()}
            while stack:  
                z = stack.pop()  
                zused = used[z]
                for nbr in T[z]:
                    # add new node to pred, stack, used
                    if nbr not in used:  
                        pred[nbr] = z
                        stack.append(nbr)
                        used[nbr] = {z}
                    # found a cycle
                    elif nbr not in zused:  
                        pn = used[nbr]
                        cycle = [nbr, z]
                        p = pred[z]
                        while p not in pn:
                            cycle.append(p)
                            p = pred[p]
                        cycle.append(p)
                        cycles.append(cycle)
                        used[nbr].add(z)
                        
            # exit while loop
            gnodes -= set(pred)
        # if network does not contain any cycles, return edges of network T
        if cycles == []:
            return list(T.edges())
        # remove an edge from the cycle, return edges of network T
        else:
            T.remove_edge(*tuple(cycles[0][0:2]))
            return list(T.edges())
        


# # Simple test

# In[2]:


G = nx.fast_gnp_random_graph(100, 0.1, seed=None, directed=False)
A = Graph(G)
# Get Shortest Path
start_node_id = 12
end_node_id = 30
Short_path = A.get_shortest_path(start_node_id, end_node_id)
print('Shortest Path from {} to {} :'.format(start_node_id, end_node_id), Short_path)
# Get Subtree
selected_node_ids = [12, 30, 40]
list_subtree = A.get_subtrees(selected_node_ids)
print('Subtree of network G according to {}:'.format(selected_node_ids), list_subtree)

