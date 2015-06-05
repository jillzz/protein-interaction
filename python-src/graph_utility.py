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

def graph_diameter(path):
    """Find the graph diameter from shortest path's files generated with
       save_all_shortest_paths function"""
    max_dist = -1;
    for i in xrange(8):
        with open('%s_%d' % (path, i), 'r') as in_file:
            for line in in_file:
                tokens = line.split()
                d = int(tokens[2])
                if d > max_dist:
                    max_dist = d

    return max_dist


#-------------------------------------------------------------------------------

def combine_and_sort_distance_files(distance_files, path):
    """Combine all distance files into single file with lines sorted by
       distance and save the new file at the given path"""
    diameter = graph_diameter(distance_files)

    for k in xrange(1, diameter + 1):
        for i in xrange(8):
            with open('%s_%d' % (distance_files, i), 'r') as in_file:
                for line in in_file:
                    tokens = line.split()
                    d = int(tokens[2])
                    if d == k:
                        with open(path, 'a') as out:
                            out.write(line)


#-------------------------------------------------------------------------------

def read_in_annotations(annotation_file):
    """ Read in the file that contains the protein annotations, and return
        protein to function dictionary """
    protein_to_functions = {}
    with open(annotation_file, 'r') as in_file:
        for line in in_file:
            tokens = line.split('\t')
            if not tokens[1] in protein_to_functions:
                protein_to_functions[tokens[1]] = set()
            protein_to_functions[tokens[1]].add(tokens[3])

    return protein_to_functions


#-------------------------------------------------------------------------------

def common_elements(set1, set2):
    """ Find if two sets have any common element """
    for element in set1:
        if element in set2:
            return True
    return False


#-------------------------------------------------------------------------------

def main():
    """
    G, id_to_protein = build_graph('../data/human_ppi_data_900')
    print 'Calculating now...'
    save_all_shortest_paths(G, 'shortest_paths_900_improved')
    """

    combine_and_sort_distance_files('distances_data/shortest_paths_900_improved', \
                                    'distances_data/shortest_paths_900_sorted')


#-------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
