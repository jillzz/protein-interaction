#!/usr/bin/python
# -*- coding: utf-8 -*-

import networkx as nx
from graph_utility import *
from interaction_graph_builder import *


#-------------------------------------------------------------------------------

def jaccard(set1, set2):
    intersect = float(len(set1.intersection(set2)))
    J = (intersect / len(set1) + intersect / len(set2)) * 0.5
    return J


def graph_content_jaccard(graph, id_to_protein, annotation_file, path):
    """ Builds interaction graph with content based weighs using Jaccard
        similarity metric. """
    protein_to_functions = read_in_annotations(annotation_file)
    with open(path, 'w') as out:
        for e in graph.edges_iter():
            #TODO:
            terms1 = protein_to_functions.get(id_to_protein[e[0]], None)
            terms2 = protein_to_functions.get(id_to_protein[e[1]], None)
            if terms1 and terms2:
                J = jaccard(terms1, terms2)
                out.write('%d %d %f\n' % (e[0], e[1], J))
            else:
                out.write('%d %d %f\n' % (e[0], e[1], 0.0))

#-------------------------------------------------------------------------------

def graph_structure_jaccard(graph, graph_jaccard, path):
    """ Builds interaction graph with structure based weighs using Jaccard
        similarity metric. """
    A = nx.to_scipy_sparse_matrix(graph)
    W = nx.to_scipy_sparse_matrix(graph_jaccard)
    #TODO


#-------------------------------------------------------------------------------

def main():
    G, id_to_protein = build_graph('../data/human_ppi_data_900')
    go900 = '../data/go/split/human_ppi900_go_mf_clean.tsv'
    #graph_content_jaccard(G, id_to_protein, go900, 'graphs/jaccard_content_900')

    G1 = build_graph_from_edgelist('graphs/jaccard_content_900')

    A = nx.to_scipy_sparse_matrix(G)
    A1 = nx.to_scipy_sparse_matrix(G1)
    print A.get_shape()
    print A1.get_shape()

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    main()