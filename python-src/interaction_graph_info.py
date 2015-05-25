#!/usr/bin/python
# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt

def plot_degree_dist (graph, path = "figure.pdf"):
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