#!/usr/bin/python
# -*- coding: utf-8 -*-

import networkx as nx
import scipy.io
import itertools
from graph_utility import *
from interaction_graph_builder import *


#-------------------------------------------------------------------------------

def save_matrix_to_edgelist(M, path):
    """ Save the matrix M as edgelist at the given path """
    tmp = M.tocoo()
    with open(path, 'w') as out:
        for i, j, w in itertools.izip(tmp.row, tmp.col, tmp.data):
            out.write('%d %d %f\n' % (i, j, w))


#-------------------------------------------------------------------------------

def jaccard(set1, set2):
    """ Calculate the Jaccard similarity metric of two sets """
    intersect = float(len(set1.intersection(set2)))
    J = (intersect / len(set1) + intersect / len(set2)) * 0.5
    return J


#-------------------------------------------------------------------------------

def graph_content_jaccard(graph, id_to_protein, annotation_file, path):
    """ Builds interaction graph with content based weighs using Jaccard
        similarity metric, and save it at the given path """
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
        similarity metric, and save it at the given path """
    A = scipy.sparse.csr_matrix(nx.google_matrix(graph, alpha = 1, weight = 'weight'))
    W = nx.to_scipy_sparse_matrix(graph_jaccard)
    W2 = ( (W * A) + (A.transpose() * W) )*0.5

    # rescaling  (max'-min')/(max-min)(v-min)+min'
    max_w = W.max()
    max_w2 = W2.max()
    W2 = W2.multiply(max_w / max_w2)

    save_matrix_to_edgelist(W2, path)


#-------------------------------------------------------------------------------

def graph_hybrid_jaccard(content_graph, structure_graph, path):
    """ Builds interaction graph with hybrid based weighs using Jaccard
        similarity metric, and save it at the given path """
    W1 = nx.to_scipy_sparse_matrix(content_graph)
    W2 = nx.to_scipy_sparse_matrix(structure_graph)
    W3 = (W1 + W2) * 0.5

    save_matrix_to_edgelist(W3, path)


#-------------------------------------------------------------------------------

def main():
    G, id_to_protein = build_graph('../data/human_ppi_data_900')
    #go900 = '../data/go/split/human_ppi900_go_mf_clean.tsv'
    #graph_content_jaccard(G, id_to_protein, go900, 'graphs/jaccard_content_900')
    G1 = build_graph_from_edgelist('graphs/jaccard_content_900', G.order())
    #graph_structure_jaccard(G, G1, 'graphs/jaccard_structure_900')
    G2 = build_graph_from_edgelist('graphs/jaccard_structure_900', G.order())
    graph_hybrid_jaccard(G1, G2, 'graphs/jaccard_hybrid_900')
    G3 = build_graph_from_edgelist('graphs/jaccard_hybrid_900', G.order())

    print nx.info(G1)
    print
    print nx.info(G2)
    print
    print nx.info(G3)


#-------------------------------------------------------------------------------

if __name__ == '__main__':
    main()