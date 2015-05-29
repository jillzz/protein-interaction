#!/usr/bin/python
# -*- coding: utf-8 -*-

import networkx as nx


#-------------------------------------------------------------------------------

def build_graph (path):
    """Build the graph from datafile at the given path"""
    tokens = []
    protein_to_id = {}
    ID = 0
    G = nx.Graph()

    with open(path, 'r') as graph_input:
        for line in graph_input:
            tokens = line.split()
            if not tokens[0] in protein_to_id:
                protein_to_id[tokens[0]] = ID
                ID += 1
            if not tokens[1] in protein_to_id:
                protein_to_id[tokens[1]] = ID
                ID += 1
            G.add_edge(protein_to_id[tokens[0]], protein_to_id[tokens[1]])

    id_to_protein = dict((protein_to_id[k], k) for k in protein_to_id.keys())

    return G, id_to_protein


#-------------------------------------------------------------------------------

def get_largest_componenet (graph):
    """Get the largest connected componenet from the graph"""
    SG = sorted( list(nx.connected_component_subgraphs(graph)), \
                 key = lambda sg: sg.order(), \
                 reverse = True)[0]
    return SG