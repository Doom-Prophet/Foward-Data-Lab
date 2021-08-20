'''
Graph Building unit (Updated on 2021.8.19 by Ma Zicheng)

In this unit, all lexical units that pass the syntactic filter are added to the graph, and an edge is added between
those lexical units that co-occur within a window of N words. After the graph is constructed (undirected unweighted
graph), the score associated with each vertex is set to an initial value of 1, and the ranking algorithm is run on
the graph for several iterations until convergence. Finally, once final score is obtained for each vertex in the
graph, vertices are sorted in reversed order to retain top T vertexes for postprocessing.
'''
from Public import Set_graph
import nltk
import numpy as np
import math


'''
Function: edge_init
Input:
    Filtered_units(list of tokens that pass the syntactic filter, type:list)
    text(input script to be handled,type:string)
    N(window size, ranging from 2 to 10, type:int)
Output:
    edges(lists of tuples containing all edges satisfying co-occur condition, used for graph building, type: list)
Effect:
    Form edges for those lexical units that co-occur within a window of N words, and collect them into a list
'''

def edge_init(text, Filtered_units, N):
    edges = []
    Tokenized_data = nltk.word_tokenize(text)

    for i in range(len(Tokenized_data)):
        if Tokenized_data[i] in Filtered_units:
            # detect if co-occur within a window of N words
            for j in range(1, N + 1):
                if (i + j < len(Tokenized_data) and Tokenized_data[i + j] != Tokenized_data[i] and Tokenized_data[i + j] in Filtered_units):
                    edges.append((Tokenized_data[i], Tokenized_data[i + j]))

    return edges


'''
Function: graph_iter
Input:
    Filtered_units (list of tokens that pass the syntactic filter, type:list)
    edges (lists of tuples containing all edges satisfying co-occur condition, used for graph building, type: list)
    d (a damping factor that can be set between 0 and 1)
    threshold (used for convergence detection)
Output:
    graph (final version of graph, built upon proper edges and gone through score iteration for convergence)
Effect:
    Building graph based on input edges, and then iterate back and forth to update scores for convergence
'''

def graph_iter(Filtered_units, edges, d=0.85, threshold=0.0001):
    graph = Set_graph.Graph(edges)

    # This buffer is used to record kth S(Vi), convenient for (k+1)th S(Vi) - kth S(Vi) calculation
    score_buffer = np.ones(len(Filtered_units))

    while (1):
        # counter here used to count how many vertex has converged, loop breaks when all vertexes converges
        count = 0
        for i in range(len(Filtered_units)):
            # all following codes are implementing the algorithm mentioned in section 2
            current_item = graph.vertexList.__getitem__(i)
            ingoing_scoresum = 0
            for node in graph.All_connecting_vertexs(current_item, edges):
                outsum = 0
                for previous_node in graph.All_connecting_vertexs(node, edges):
                    outsum += graph.vertexList.__getscore__(graph.vertexList.index(previous_node))
                ingoing_scoresum += graph.vertexList.__getscore__(graph.vertexList.index(node)) / np.abs(outsum)
            previous_score = graph.vertexList.__getscore__(i)
            new_score = (1 - d) + d * ingoing_scoresum
            score_buffer[i] = new_score - previous_score
            graph.vertexList.__setnewscore__(i, new_score)

        # convergence detection
        for diff in score_buffer:
            if diff < threshold:
                count += 1
        if count >= len(Filtered_units):
            break

    return graph

'''
Function:top_retain
Input:
    graph (final version of graph, built upon proper edges and gone through score iteration for convergence)
    length (total number of filtered lexical units)
Output:
    res ( top T vertices in the ranking are retained here, type:list)
    vertex_score_dict ( vertex-score dictionary for whole graph)
Effect:
    pick up top T vertices for postprocessing
'''
#notice that here T = (1/3)*length is floored
def top_retain(graph, length):
    vertex_score_dict = {}
    res = []
    counter = 0
    for i in range(length):
        vertex_score_dict[graph.vertexList.__getitem__(i)] = graph.vertexList.__getscore__(i)

    sorted_dict = sorted(vertex_score_dict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)

    while counter < math.floor(length / 3):
        res.append(sorted_dict[counter][0])
        counter += 1

    return res,vertex_score_dict
