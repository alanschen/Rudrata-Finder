import numpy as np
import networkx as nx
import time

def isHamilton(nodes, path, v):
    """This assumes that the path is valid"""
    if v != path[0] or len(path) != len(nodes):
        return False
    for node in nodes:
        if node not in path:
            return False
    return True

def rotate(path, j):
    """j is the index of the conflicting node"""
    latter = path[j + 1:]
    former = path[:j + 1]
    latter.reverse()
    return former + latter
    
def extend(path, v):
    path.append(v)

def explore(path, v):
    if isHamilton(nodes, path, v):
        extend(path, v)
        return True
    
    elif v not in path:
        extend(path, v)
        return False
    
    else:
        j = path.index(v)
        rotate(path, j)
        return False

def partition_neighbs(g, head, cache):
    visited = cache[head]
    unvisited = set()
    for node in list(g.neighbors(head)):
        if node not in visited:
            unvisited.add(node)
    return list(visited), list(unvisited)
    
def rudrata_randomized(graph, nodes, timeout=3):
    """"This assumes that (1) Rudrata Path exists and (2) The graph is connected
    Algorithm times out after 30 seconds
 
    """
    t0 = time.time()
    # step 1
    n = graph.number_of_nodes()
    head = np.random.choice(nodes)
    path = [head]
    
    cache = {}
    for temp in nodes:
        cache[temp] = set()
    
    # step 2
    visited, unvisited = partition_neighbs(graph, head, cache)
    x = len(visited)
    
    # debug tools
    
    while len(unvisited) != 0:
        t1 = time.time()
        if t1 - t0 > 30:
            break
        # path is defined already
        # neighbors are computed at the end
        prob = np.random.random()
        if prob <= 1/n:
            # case 1 reverse path
            head = path[0]
            path.reverse()
            visited, unvisited = partition_neighbs(graph, head, cache)
            x = len(visited)
            continue
        elif prob <= (x + 1) / n:
            # case 2
            v = np.random.choice(visited)
        else:
            v = np.random.choice(unvisited)
            cache[head].add(v)
        
        # explore
        if isHamilton(nodes, path, v):
            return path

        elif v not in path:
            head = v
            extend(path, v)

        else:
            j = path.index(v)
            head = path[j + 1]
            path = rotate(path, j)
            
        visited, unvisited = partition_neighbs(graph, head, cache)
        x = len(visited)
        
    return False