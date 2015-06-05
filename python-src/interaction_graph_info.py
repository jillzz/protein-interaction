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

def plot_proteins_sharing_function(id_to_protein, \
                                   annotation_file, distance_file, path):
    """Plot histogram of proteins sharing al least one common functiopn depending
       on the distance between them and save the figure at the given path.
       On X-axis we have the distance and on Y-axis we have percentage of pairs
       that have at least one common function.
       id_to_protein: dictionary where each node in the graph maps to a protein
       annotation_file: path to the file that cointains proteins and their functions
       distance_file: path to the file that contains shortest paths between the nodes"""

    protein_to_functions = read_in_annotations(annotation_file)

    distance_to_count = {}
    distance_to_common = {}
    for i in xrange(8):
        with open('%s_%d' % (distance_file, i), 'r') as in_file:
            for line in in_file:
                tokens = line.split()
                p1 = id_to_protein[int(tokens[0])]
                p2 = id_to_protein[int(tokens[1])]
                d = int(tokens[2])
                distance_to_count[d] = 1 + distance_to_count.get(d, 0)
                if p1 in protein_to_functions and \
                        p2 in protein_to_functions and \
                        common_elements(protein_to_functions[p1], protein_to_functions[p2]):
                    distance_to_common[d] = 1 + distance_to_common.get(d, 0)

    for d in distance_to_common:
        distance_to_common[d] *= (100.0 / distance_to_count[d])

    # Plotting
    diameter = graph_diameter(distance_file)
    x = range(0, diameter + 1)
    y = [distance_to_common.get(i, 0) for i in x]

    plt.bar(x, y, width = 1, color = 'b')
    plt.title("Proteins sharing common functions\n depending on the distance between them")
    plt.ylabel("Percent of pairs sharing common functions")
    plt.xlabel("Distance")
    plt.axis('tight')
    plt.savefig(path)


#-------------------------------------------------------------------------------

def plot_function_first_appearance(id_to_protein, annotation_file, \
                                   distance_file, path, diameter):
    """ TODO: Write documentation
       Plot histogram of proteins sharing al least one common functiopn depending
       on the distance between them and save the figure at the given path.
       On X-axis we have the distance and on Y-axis we have percentage of pairs
       that have at least one common function.
       id_to_protein: dictionary where each node in the graph maps to a protein
       annotation_file: path to the file that cointains proteins and their functions
       distance_file: path to the file that contains shortest paths between the nodes"""

    protein_to_functions = read_in_annotations(annotation_file)

    distance_to_appearance = {}
    with open(distance_file, 'r') as in_file:
        for line in in_file:
            tokens = line.split()
            p1 = int(tokens[0])
            pp1 = id_to_protein[p1]
            p2 = int(tokens[1])
            pp2 = id_to_protein[p2]
            d = int(tokens[2])
            if pp1 in protein_to_functions and pp2 in protein_to_functions:
                intersection = protein_to_functions[pp1].intersection(protein_to_functions[pp2])
                protein_to_functions[pp1].difference_update(intersection)
                protein_to_functions[pp2].difference_update(intersection)
                distance_to_appearance[d] = distance_to_appearance.get(d, 0) + \
                                            (2 * len(intersection))

    normalizer = float(sum(distance_to_appearance.values()))

    # Plotting
    x = range(0, diameter + 1)
    y = [distance_to_appearance.get(i, 0) / normalizer for i in x]

    plt.bar(x, y, width = 1, color = 'b')
    plt.title("Number of functions first appearing at given distance")
    plt.ylabel("Normalized number of functions")
    plt.xlabel("Distance")
    plt.axis('tight')
    plt.savefig(path)