'''
Created on Dec 15, 2012

@author: Praveen Shilavantar
'''

"""
Problem:

It is said that everyone is connected to everyone else through at most 6
friendship connections.

Given a list of friendship relationships, and a target person, number everyone
for how many degrees of separation they are from the target.

>>> friendships = [
...     ('bob', 'alice'),
...     ('fred', 'candice'),
...     ('michael', 'candice'),
...     ('bob', 'nancy'),
...     ('michael', 'alice'),
...     ('nancy', 'alice'),
...     ('sally', 'nancy'),
... ]
>>> sorted(list_degrees(friendships, target='bob'))
[(0, 'bob'), (1, 'alice'), (1, 'nancy'), (2, 'michael'), (2, 'sally'), (3, 'candice'), (4, 'fred')]
"""


def list_degrees(friendships, target):
    nodes_dict, nodes = create_degrees_dict(friendships)
    return [(find_degree(nodes_dict, target, i), i) for i in nodes]

def find_degree(nodes_dict, target, dest):
    """
    Find the degree of each node
    """
    # Target is the destination
    if target == dest:
        return 0
    
    # Edges of target
    edges = nodes_dict[target]
    
    paths = []
    for i in edges:
        
        # Mark target as visited
        visited = [target]
        count = 1
        # if one of edges of target is the destination
        if i == dest:
            return 1
        # Find the path between target and its edges
        count = find_path(nodes_dict, target, i, dest, count, visited)
        if count:
            paths.append(count)
    
    # Shortest path
    if paths:
        return min(paths)
    
def find_path(nodes_dict, target, node, dest, count, visited):
    """
    the path between target and its edges
    """
    # Mark node as visited
    visited.append(node)
    count += 1
    edges = nodes_dict[node]
    
    # Node with no edges
    if not edges:
        return -1
    
    if len(edges) == 1 and edges[0] == target:
        return 0

    # Destination is found
    if dest in edges:
        return count

    for i in edges:
        if i == target:
            continue
        
        # Node is not yet visited
        if not i in visited :
            return find_path(nodes_dict, target, i, dest, count, visited)
    return count

def create_degrees_dict(friendships):
    """
    Create a dictionary of nodes with neighbors  
    """
    nodes_dict = {}
    nodes = []
    for i in friendships:
        if i[0] in nodes_dict.keys():
            nodes_dict[i[0]].append(i[1])
        else:
            nodes_dict[i[0]] = [i[1]]
            
        if not i[0] in nodes: nodes.append(i[0])
        if not i[1] in nodes: nodes.append(i[1])
        
    find_neighbors(nodes_dict, nodes)
    
    return nodes_dict, nodes

def find_neighbors(nodes_dict, nodes):
    
    keys = nodes_dict.keys()
        
    for i in nodes:
        if not i in keys:
            nodes_dict[i] = []
            add_neighbor(nodes_dict, i)
        else:
            add_neighbor(nodes_dict, i)                
                
def add_neighbor(nodes_dict, i):
    
    for k, v in nodes_dict.iteritems():
        if i in v and not k in nodes_dict[i]:
            nodes_dict[i].append(k)
            

if __name__ == '__main__':
    friendships = [
     ('bob', 'alice'),
     ('fred', 'candice'),
     ('michael', 'candice'),
     ('bob', 'nancy'),
     ('michael', 'alice'),
     ('nancy', 'alice'),
     ('sally', 'nancy'),
     ]
    print sorted(list_degrees(friendships, 'bob'))
    print sorted(list_degrees(friendships, 'alice'))
    print sorted(list_degrees(friendships, 'sally'))
    print sorted(list_degrees(friendships, 'nancy'))
    print sorted(list_degrees(friendships, 'michael'))
    print sorted(list_degrees(friendships, 'candice'))
    print sorted(list_degrees(friendships, 'fred'))
    
    