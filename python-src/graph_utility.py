#!/usr/bin/python
# -*- coding: utf-8 -*-

import networkx as nx
import multiprocessing
import math
import numpy as np
import scipy
from interaction_graph_builder import *
from graph_preprocessing import *
from operator import itemgetter


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

def all_functions(graph, id_to_protein, annotation_file, path):
    """ Finds all functions with which proteins in the graph are annotated with
        and saves the list at the given path
    """
    protein_to_functions = read_in_annotations(annotation_file)
    functions = set()

    for node in graph.nodes_iter():
        p = id_to_protein[node]
        p_f = protein_to_functions.get(p, set())
        functions.update(p_f)

    with open(path, 'w') as out:
        for f in functions:
            out.write('%s\n' % f)


#-------------------------------------------------------------------------------

def common_elements(set1, set2):
    """ Find if two sets have any common element """
    for element in set1:
        if element in set2:
            return True
    return False


#-------------------------------------------------------------------------------

def function_to_function(graph, id_to_protein, annotation_file, path):
    """ Build function-to-function edgelist for all functions pairs with which
        connected nodes in the graph are annotated. The edgelist is savet at
        the given path. This file is later used for Resnik sematic metric
        calculation in R
    """
    protein_to_functions = read_in_annotations(annotation_file)
    function_pairs = set()
    for edge in graph.edges_iter():
        n1 = id_to_protein[edge[0]]
        n2 = id_to_protein[edge[1]]
        set1 = protein_to_functions.get(n1, set())
        set2 = protein_to_functions.get(n2, set())
        for f1 in set1:
            for f2 in set2:
                pair = (min(f1, f2), max(f1, f2))
                function_pairs.add(pair)

    with open(path, 'w') as out:
        for pair in function_pairs:
            out.write('%s %s\n' % (pair[0], pair[1]))


#-------------------------------------------------------------------------------

def save_pageranks(graph, restart_prob, path, seed_node = None):
    """ Find stationary distribution of the random walk of the graph with restart
        probability of restart_prob and personalization if the seed_node is given.
        The results are saved at the given path with the seed_node in the first line
        (if given) and proceeded by 'node pagerank' lines for every node
    """
    #TODO: Probably unnecessary

    pr = pagerank(graph, restart_prob, seed_node, 50, 1e-04)
    #pr = sorted([item for item in pr.items()], key = itemgetter(1), reverse = True)

    with open(path, 'a') as out:
        if seed_node != None:
            out.write('%d\n' % seed_node)
        for i in xrange(len(pr)):
            out.write('%d %f\n' % (i, pr[i]))


#-------------------------------------------------------------------------------

def remove_zero_weights_from_edgelist (in_path, out_path):
    """ Read in graph output as edgelist in the in_path file and
        write it back to out_path file with 0-weight edges removed
    """
    with open(in_path, 'r') as in_file:
        with open(out_path, 'w') as out_file:
            for line in in_file:
                tokens = line.split()
                if int(tokens[2]) > 0 or int(tokens[2]) < 0:
                    out_file.write(line)


#-------------------------------------------------------------------------------

def remove_zero_weights_from_graph (graph):
    """ Remove all 0-weight edges from the graph """
    for_removal = []
    for edge in graph.edges_iter():
        if graph[edge[0]][edge[1]]['weight'] >= 0 and graph[edge[0]][edge[1]]['weight'] <= 0:
            for_removal.append(edge)

    graph.remove_edges_from(for_removal)


#------------------------------------------------------------------------------

def pagerank(graph, alpha, start_node, max_iterations = 100, threshold = 1e-06):
    # google matrix (row stochastic)
    Q = set_transition_probabilities(graph, alpha, start_node)
    Q = Q.transpose() # column stochastic

    p = np.zeros(graph.order())
    p[start_node] = 1.0
    it = max_iterations

    while(it > 0):
        it -= 1
        #old_p = np.copy(p)
        p = Q.dot(p)
        #if np.linalg.norm(p - old_p) <= threshold: break

    return p


#------------------------------------------------------------------------------

def multiply(G, p, old_p, start_node):
    """ One iteration of the power method used for personalized pagerank calculation """
    for i in xrange(len(p)):
        p[i] = 0.0

    for node1 in G.nodes_iter():
        for node2 in G.predecessors_iter(node1):
            p[node1] += (G[node2][node1]['transition']*old_p[node2])

    if not p[start_node] > 0:
        p[start_node] += (G[start_node][start_node]['transition']*old_p[start_node])


#-------------------------------------------------------------------------------

def set_transition_probabilities(graph, damping, start_node):
    # transition probabilities
    for_removal = []
    for node in graph.nodes_iter():
        # sum the weights
        weights_sum = 0.0
        for neighbor in graph.successors_iter(node):
            weights_sum += graph.get_edge_data(node, neighbor)['weight']

        # set the transition probability multiplied by (1 - damping)
        for neighbor in graph.successors_iter(node):
            transition = ((1-damping) * (graph[node][neighbor]['weight'] / weights_sum))
            nx.set_edge_attributes(graph, 'transition', {(node, neighbor): transition})

        # add the restart
        if graph.has_edge(node, start_node):
            graph[node][start_node]['transition'] += damping
        else:
            for_removal.append((node, start_node))
            if weights_sum > 0:
                graph.add_edge (node, start_node, {'weight': 0, 'transition': damping})
            else:
                graph.add_edge (node, start_node, {'weight': 0, 'transition': 1.0})

    return for_removal


#-------------------------------------------------------------------------------

def pagerank2(graph, alpha, start_node, max_iterations = 50, threshold = 1e-04):
    """ Personalized pagerank implementation """
    for_removal = set_transition_probabilities(graph, alpha, start_node)

    it = max_iterations
    p = np.zeros(graph.order())
    p[start_node] = 1.0
    old_p = np.zeros(graph.order())

    while(it > 0):
        it -= 1
        for i in xrange(len(p)):
            old_p[i] = p[i]

        multiply(graph, p, old_p, start_node)
        if max(np.absolute(p - old_p)) <= threshold: break

    for e in for_removal:
        graph.remove_edge(e[0], e[1])

    return p


#-------------------------------------------------------------------------------

def filter_unexisting_edges (graph, edgelist_path, path):
    """ Filter out all the edges from edgelist_path that do not exist in the graph.
        Save the new edgelist graph at the given path
    """
    print 'Filtering', edgelist_path
    with open (edgelist_path, 'r') as in_file:
        with open (path, 'w') as out_file:
            for line in in_file:
                tokens = line.split()
                if graph.has_edge(int(tokens[0]), int(tokens[1])):
                    out_file.write(line)


#-------------------------------------------------------------------------------

def main():
	 """
    G, id_to_protein = build_graph('../data/human_ppi_data_900')
    print nx.info(G)
    filter_unexisting_edges(G, 'graphs/wang_hybrid_900', 'graphs/wang_hybrid_900_filtered')
    """

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
