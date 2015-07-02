#!/usr/bin/python
# -*- coding: utf-8 -*-

import networkx as nx
import time
import community
from interaction_graph_builder import *
from interaction_graph_info import *
from graph_utility import *
from graph_creator import *
from clustering_and_prediction import *


#------------------------------------------------------------------------------

def main():
    start = time.time()
    #G, id_to_protein = build_graph('../data/human_ppi_data_900')

    G = build_graph_from_edgelist('graphs/final/rw_wh_900')
    print nx.info(G)
    print nx.number_connected_components(G)

    multilevel = louvain_best(G)

    for level in multilevel:
        print 'Level: ', level
        print 'Number of clusters: ', len(multilevel[level])
        tmp = [len(multilevel[level][c]) for c in multilevel[level]]
        print 'Max. cluster size: ', max(tmp)
        print 'Min. cluster size: ', min(tmp)
        '''
        for cluster in multilevel[level]:
            for node1 in multilevel[level][cluster]:
                 for node2 in multilevel[level][cluster]:
                     #print node1, node2
                     if node1 < node2 and G.has_edge(node1, node2):
                         print G[node1][node2]['weight']
            print
        print
        '''
        print

    end = time.time()
    print 'Task finished in: %f min.' % ((end-start) / 60.0)


#------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
