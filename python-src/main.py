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

    G = build_graph_from_edgelist('graphs/final/rw_jc_900')


    multilevel = louvain(G)

    '''
    for level in multilevel:
        print 'Level: ', level
        print 'Number of clusters: ', len(multilevel[level])
        tmp = [len(multilevel[level][c]) for c in multilevel[level]]
        print 'Max. cluster size: ', max(tmp)
        print 'Min. cluster size: ', min(tmp)
    '''

    with open('util_data/clusters_rw_jc_900', 'w') as out:
        level = 0
        for cluster in multilevel[level]:
            out.write('Cluster: %d\n' % cluster)
            for node1 in multilevel[level][cluster]:
                out.write('%d ' % node1)
            out.write('\n\n')



    end = time.time()
    print 'Task finished in: %f min.' % ((end-start) / 60.0)


#------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
