def find(parent, i):
    """Finds the root parent of node i with path compression."""
    if parent[i] == i:
        return i
    parent[i] = find(parent, parent[i])  # Path compression
    return parent[i]

def union(parent, rank, x, y):
    """Unites two subsets based on rank."""
    root_x = find(parent, x)
    root_y = find(parent, y)
    
    if root_x != root_y:
        if rank[root_x] < rank[root_y]:
            parent[root_x] = root_y
        elif rank[root_x] > rank[root_y]:
            parent[root_y] = root_x
        else:
            parent[root_y] = root_x
            rank[root_x] += 1
        return True
    return False

def kruskal(graph):
    """
    graph: dict where keys are nodes and values are lists of (neighbor, weight) tuples.
    """
    # 1. Collect all unique edges
    edges = []
    seen_edges = set()
    for u in graph:
        for v, weight in graph[u]:
            # Use sorted tuple to ensure we don't duplicate undirected edges
            edge_key = tuple(sorted((u, v)))
            if edge_key not in seen_edges:
                seen_edges.add(edge_key)
                edges.append((weight, u, v))
                
    # 2. Sort edges by weight manually (bubble sort mechanism for module-free purity)
    # Alternatively, you can use Python's built-in sorted(): edges = sorted(edges)
    # Using sorted() does not require an import.
    edges.sort() 

    # 3. Initialize Union-Find structures
    parent = {}
    rank = {}
    for node in graph:
        parent[node] = node
        rank[node] = 0
        
    mst = []
    total_weight = 0
    num_vertices = len(graph)
    
    # 4. Process edges
    for weight, u, v in edges:
        # If adding the edge doesn't form a cycle, include it
        if union(parent, rank, u, v):
            mst.append((u, v, weight))
            total_weight += weight
            
            # Optimization: Stop early if we have V-1 edges
            if len(mst) == num_vertices - 1:
                break
                
    return mst, total_weight

# Example usage:
example_graph = {
    'A': [('B', 4), ('H', 8)],
    'B': [('A', 4), ('H', 11), ('C', 8)],
    'C': [('B', 8), ('I', 2), ('D', 7), ('F', 4)],
    'D': [('C', 7), ('F', 14), ('E', 9)],
    'E': [('D', 9), ('F', 10)],
    'F': [('C', 4), ('D', 14), ('E', 10), ('G', 2)],
    'G': [('F', 2), ('I', 6), ('H', 1)],
    'H': [('A', 8), ('B', 11), ('G', 1), ('I', 7)],
    'I': [('C', 2), ('G', 6), ('H', 7)]
}

mst_edges, cost = kruskal(example_graph)
print("Edges in MST:", mst_edges)
print("Total Cost:", cost)
