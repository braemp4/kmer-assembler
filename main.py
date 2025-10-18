from collections import deque
import networkx as nx
import matplotlib.pyplot as plt
import sys 

def dfs(graph, node):
    visited = []
    stack = deque()

    visited.append(node)
    stack.append(node)

    while stack:
        s = stack.pop()
        #print(s)
        if s in graph.keys(): 
            for n in reversed(graph[s]): 
                if n not in visited:
                    visited.append(n)
                    stack.append(n)
    return visited



def de_bruijn_ize(st, k):
    '''
    Test function 

    Take a sequence, split into L and R k minus - 1. Return nodes (unique) and edges (repeated)
    '''

    edges = [] #edges can be repeated
    nodes = set() #nodes are unique
    for i in range(len(st) - k + 1):
        #left and right k -1 mers
        left, right = st[i:i+k-1], st[i+1:i+k]
        
        #append edges as tuples
        edges.append((left, right))
        
        #add to nodes
        nodes.add(left)
        nodes.add(right)
    return nodes, edges 

#nodes, edges = de_bruijn_ize("ACGCTCGCGTATA", 3)


#print("nodes:", nodes)
#print("edges:", edges)

def build_debruijn(kmers):
    edges = [] 

    nodes = set()
    for kmer in kmers:
        left = kmer[:len(kmer)-1]
        right = kmer[1:]
        
        nodes.add(left)
        nodes.add(right)
    #print(nodes)
    nodes = list(nodes)

    for i in range(len(nodes)):
        for j in range(len(nodes)):
            #print((nodes[i], nodes[j]))

            potential_edge = (nodes[i], nodes[j])
            potential_kmer = potential_edge[0] + potential_edge[1][1:] if nodes[i][len(nodes[i]) - 1] == nodes[j][0] else None

            #if potential_kmer:
            #    print(potential_kmer)
            if potential_kmer in kmers:
                edges.append(potential_edge)

    #print(f"Original kmers {kmers}")

    return nodes, edges  

def edges_to_dict(edges):
    edge_dict = {}

    for edge in edges:
        edge_dict.update({edge[0]:[]})
    for edge in edges:
        edge_dict[edge[0]].append(edge[1])
    return edge_dict


def assemble_genome(kmers):
    '''
    Start from edge[0] that is never an edge[1]

    find all all its childen (edge[1]s) 

    need to keep track of nodes we've visited for sequence
    we also shouldnt traverse the same edge more than once 

    dfs so from edge[1], find where its edge[0], find that edge[1], it becomes edge[0] until we get to edge[1] that is never an edge[0]

    may be helpful to turn tuples into dictionaries (edge_dict)
    '''
    nodes, edges = build_debruijn(kmers)
    edge_dict = edges_to_dict(edges)

    seq_start = list(edge_dict.keys())[0] #IT FREKIN WORKED!
    print(edge_dict.keys())
    print(edge_dict.values())
    for key in edge_dict.keys():
        all_values = []
        for ls in edge_dict.values():
            for mer in ls:
                all_values.append(mer) 

        if key not in all_values:
            seq_start = key
    seq = dfs(edge_dict, seq_start) 
    return str(seq)

#test_seq = "ACTTTAT"
#test_mers = ["ACT", "TTT", "CTT", "TTA", "TAT"]
#print(build_debruijn(test_mers))
#nodes, edges = build_debruijn(test_mers)
#print(edges_to_dict(edges))

def main():

    mers_file = sys.argv[1]
    with open(mers_file, "r") as f:
        test_mers = f.read().splitlines()
        print(test_mers)

    graph = nx.DiGraph()
    nodes, edges = build_debruijn(test_mers)
    graph.add_edges_from(edges)
    nx.draw_networkx(graph,arrows=True)
    plt.tight_layout()


    #print(f"Original seq: {test_seq}")
    print(f"Using DFS: {assemble_genome(test_mers)}")
    nx_eul = [u for u, v in nx.eulerian_path(graph)]
    print(f"Using networkx: {nx_eul}")

    plt.show()
if __name__ == "__main__":
    main()
