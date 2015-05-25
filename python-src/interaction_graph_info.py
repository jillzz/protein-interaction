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
