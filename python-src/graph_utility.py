#!/usr/bin/python
# -*- coding: utf-8 -*-

import networkx as nx
import multiprocessing
import math
from interaction_graph_builder import *


#-------------------------------------------------------------------------------

def calculate_shortest_paths(graph, start_node, end_node, path):
    """Calculates shortest paths going from all nodes within the range
       start_node - end_node, calculated distances are saved at the given path"""
    #distances = {}
    for i in xrange(start_node, end_node):
        if graph.has_node(i):
            for j in xrange(i+1, graph.order()):
                if graph.has_node(i):
                    try:
                        distance = nx.shortest_path_length(graph, i, j)
                        with open(path, 'a') as out:
                            out.write('%d %d %d\n' % (i, j, distance))
                    except nx.NetworkXNoPath:
                        continue




#-------------------------------------------------------------------------------

def save_all_shortest_paths(graph, path):
    """Calculate with multiprocessing all shortest paths within the graph"""
    cpus = multiprocessing.cpu_count()
    step = graph.order() / float(cpus)
    starting = 0

    jobs = []
    for i in range(cpus):
        p = multiprocessing.Process(target = calculate_shortest_paths, \
                                    args = (graph, \
                                            int(starting), \
                                            int(math.ceil(starting + step)), \
                                            '%s_%d' % (path, i)))
        jobs.append(p)
        p.start()
        starting = math.ceil(starting + step)


#-------------------------------------------------------------------------------

def main():
    """
    G, id_to_protein = build_graph('../data/human_ppi_data_900')
    print 'Calculating now...'
    save_all_shortest_paths(G, 'shortest_paths_900_improved')
    """


#-------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
