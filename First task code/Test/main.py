'''
Main function for stage tests (Updated on 2021.8.20 by Ma Zicheng)
'''

import sys
import nltk
sys.path.append('.\\Public')
from Public import Graph_Building_unit, Postprocessing_unit, Preprocessing_unit, Set_graph, Keyword_Cloud

# Testcodes:
print('-------Test 1  Preprocessing---------\n')

POSlist = ['NN', 'NNS', 'JJ', 'VBP']

# This text is the one used in 'TextRank: Bringing Order into Texts' Figure 2 on page 4
# Convenient for result comparison
text = "Compatibility of systems of linear constraints over the set of natural numbers.\
       Criteria of compatibility of a system of linear Diophantine equations, strict \
       inequations, and nonstrict inequations are considered. Upper bounds for \
       components of a minimal set of solutions and algorithms of construction of \
       minimal generating sets of solutions for all types of systems are given.\
       These criteria and the corresponding algorithms for constructing a minimal \
       supporting set of solutions can be used in solving all the considered types \
       systems and systems of mixed types.".lower()

Tokens = Preprocessing_unit.Tokenize(text)
Tags = Preprocessing_unit.POS_tagging(Tokens)
print('Tokens:', Tokens)
print('Corresponding tags:', Tags)
Filtered_units = Preprocessing_unit.syntactic_filter(Tags, POSlist)
print('Filtered_units:', Filtered_units, '\n')

print('-------Test 2 Building graph---------\n')

edges = Graph_Building_unit.edge_init(text, Filtered_units, 2)
graph = Graph_Building_unit.graph_iter(Filtered_units, edges)
print('Graph printed')
graph.plot_graph()
res, vertex_score_dict = Graph_Building_unit.top_retain(graph, len(Filtered_units))

print('-------Test 3 Postprocessing---------\n')

sorted_new_keyword = Postprocessing_unit.keyword_collapse(nltk.word_tokenize(text), Filtered_units, res, vertex_score_dict)
print('Final keywords and their scores:', sorted_new_keyword, '\n')

print('-------Test 4 Visualization---------\n')

Keyword_Cloud.visualization(sorted_new_keyword)
