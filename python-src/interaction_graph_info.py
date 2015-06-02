#!/usr/bin/python
# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt
from graph_utility import *


#-------------------------------------------------------------------------------

def plot_degree_dist (graph, path):
    """Plot log-log degree distribution of the graph and save the figure
       at the given path. On X-axis we have degrees and on Y-axis we have
       the percentage of nodes that have that degree"""

    node_to_degree = graph.degree()
    N = float(graph.order())
    degree_to_percent = {}

    # calculate percentages of nodes with certain degree
    for node in node_to_degree:
        degree_to_percent[node_to_degree[node]] = 1 + degree_to_percent.get(node_to_degree[node], 0)
    for degree in degree_to_percent:
        degree_to_percent[degree] = degree_to_percent[degree] / N * 100

    x = sorted(degree_to_percent.keys(), reverse = True)
    y = [degree_to_percent[i] for i in x]

    plt.loglog(x, y, 'b-', marker = '.')
    plt.title("Degree Distribution")
    plt.ylabel("Log percentage")
    plt.xlabel("Log degree")
    plt.axis('tight')
    plt.savefig(path)


#-------------------------------------------------------------------------------

def plot_clustering_spectrum (graph, path):
    """Plot the clusttering spectrum of the graph and save the figure
       at the given path. On X-axis we have degrees and on Y-axis we have
       average clustering coefficients of the nodes that have that degree"""

    node_to_degree = graph.degree()
    node_to_clustering = nx.clustering(graph)
    degree_to_clustering = {}

    # calculate average clustering coefficients for nodes with certain degree
    for node in node_to_degree:
        deg = node_to_degree[node]
        tmp = degree_to_clustering.get(deg, [])
        tmp.append(node_to_clustering[node])
        degree_to_clustering[deg] = tmp

    for degree in degree_to_clustering:
        tmp = degree_to_clustering[degree]
        degree_to_clustering[degree] = float(sum(tmp)) / len(tmp)

    x = sorted(degree_to_clustering.keys(), reverse = True)
    y = [degree_to_clustering[i] for i in x]

    plt.loglog(x, y, 'b-', marker = '.')
    plt.title("Clustering Spectrum")
    plt.ylabel("Average clustering coefficient")
    plt.xlabel("Degree")
    plt.axis('tight')
    plt.savefig(path)


#-------------------------------------------------------------------------------

def plot_shortest_path_spectrum (graph, path, paths_data):
    """Plot distribution of shortest paths of the graph and save the figure
       at the given path. On X-axis we have distance values and on Y-axis we
       have percentage of node pairs that have that distance value"""

    diameter = graph_diameter(paths_data)
    pairs = graph.order() * (graph.order()-1) * 0.5

    distances_count = [0 for i in xrange(diameter + 1)]
    for i in xrange(8):
        with open('%s_%d' % (paths_data, i), 'r') as in_file:
            for line in in_file:
                tokens = line.split()
                distances_count[int(tokens[2])] += 1

    for i in xrange(diameter + 1):
        distances_count[i] *= (100.0 / pairs)

    y = distances_count
    plt.loglog(y, 'b-', marker = '.')
    plt.title("Shortest Paths Spectrum")
    plt.ylabel("Percent of pairs")
    plt.xlabel("Distance")
    plt.axis('tight')
    plt.savefig(path)


#-------------------------------------------------------------------------------

def plot_closeness_dist (graph, path):
    """Plot distribution of closeness centrality of the graph and save the figure
       at the given path. On X-axis we have closeness centrality values and on
       Y-axis we have percentage of the nodes that have that closeness value"""

    N = float(graph.order())
    node_to_closeness = nx.closeness_centrality(graph)
    closeness_to_percent = {}

    # calculate percentages of nodes with certain closeness value
    for node in node_to_closeness:
        closeness_to_percent[node_to_closeness[node]] = 1 + \
                closeness_to_percent.get(node_to_closeness[node], 0)
    for c in closeness_to_percent:
        closeness_to_percent[c] = closeness_to_percent[c] / N * 100

    x = sorted(closeness_to_percent.keys(), reverse = True)
    y = [closeness_to_percent[i] for i in x]

    plt.loglog(x, y, 'b-', marker = '.')
    plt.title("Closeness Centrality Distribution")
    plt.ylabel("Percentage")
    plt.xlabel("Closeness value")
    plt.axis('tight')
    plt.savefig(path)


#-------------------------------------------------------------------------------

def plot_betweenness_dist (graph, path):
    """Plot distribution of betweenness centrality of the graph and save the figure
       at the given path. On X-axis we have betweenness centrality values and on
       Y-axis we have percentage of the nodes that have that betweenness value.
       k is the number of samples for estimating the betweenness centrality."""

    N = float(graph.order())
    node_to_betweenness = nx.betweenness_centrality(graph)
    betweenness_to_percent = {}

    # calculate percentages of nodes with certain betweeness value
    for node in node_to_betweenness:
        betweenness_to_percent[node_to_betweenness[node]] = 1 + \
                betweenness_to_percent.get(node_to_betweenness[node], 0)
    for c in betweenness_to_percent:
        betweenness_to_percent[c] = betweenness_to_percent[c] / N * 100

    x = sorted(betweenness_to_percent.keys(), reverse = True)
    y = [betweenness_to_percent[i] for i in x]

    plt.loglog(x, y, 'b-', marker = '.')
    plt.title("Betweenness Centrality Distribution")
    plt.ylabel("Percentage")
    plt.xlabel("Betweenness value")
    plt.axis('tight')
    plt.savefig(path)


#-------------------------------------------------------------------------------


def read_in_annotations(annotation_file):
    """Read in the file that contains the protein annotations"""
    protein_to_functions = {}
    with open(annotation_file, 'r') as in_file:
        for line in in_file:
            tokens = line.split('\t')
            print tokens[1], tokens[3]
            if tokens[1] not in protein_to_functions:
                protein_to_functions[tokens[1]] = set()
            protein_to_functions[tokens[1]].add(tokens[3])

    return protein_to_functions


def common_elements(set1, set2):
    """Find if two sets have any common element"""
    for element in set1:
        if element in set2:
            return True
    return False


def plot_proteins_sharing_function(id_to_protein, \
                                   annotation_file, distance_file, path):
    """Plot histogram of proteins sharing al least one common functiopn depending
       on the distance between them and save the figure at the given path.
       On X-axis we have the distance and on Y-axis we have percentage of pairs
       that have at least one common function.
       id_to_protein: dictionary where each node in the graph maps to a protein
       annotation_file: path to the file that cointains proteins and their functions
       distance_file: path to the file that contains shortest paths between the nodes"""

    paths_dict = read_in_shortest_paths(distance_file)
    protein_to_functions = read_in_annotations(annotation_file)

    distance_to_count = {}
    for pair in paths_dict:
        distance_to_count[paths_dict[pair]] = \
                    1 + distance_to_count.get(paths_dict[pair], 0)

    distance_to_common = {}
    for pair in paths_dict:
        pp1 = id_to_protein[pair[0]]
        pp2 = id_to_protein[pair[1]]
        if pp1 in protein_to_functions and pp2 in protein_to_functions and \
                common_elements(protein_to_functions[pp1], protein_to_functions[pp2]):
            distance_to_common[paths_dict[pair]] = \
                        1 + distance_to_common.get(paths_dict[pair], 0)

    print distance_to_count
    print distance_to_common

    for d in distance_to_common:
        distance_to_common[d] *= (100.0 / distance_to_count[d])

    # Plotting
    x = range(0, max(distance_to_common.keys())+1)
    y = [distance_to_common.get(i, 0) for i in x]

    plt.loglog(x, y, 'b-', marker = '.')
    plt.title("Proteins sharing common functions depending on the distance between them")
    plt.ylabel("Percentage of protein pairs with atleast one common function")
    plt.xlabel("Distance")
    plt.axis('tight')
    plt.savefig(path)



