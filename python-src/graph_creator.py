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

def sum_max_similarities (set1, set2, functions_to_similarity):
    """ Every function in set1 is compared with every other in set2. The maximums
        for every function in set1 are then summed."""
    sum1 = 0.0
    for f1 in set1:
        m1 = 0.0
        for f2 in set2:
            pair = (min(f1, f2), max(f1, f2))
            sim = functions_to_similarity.get(pair, 0)
            if sim > m1:
                m1 = sim
        sum1 += m1

    return sum1


def semantic(set1, set2, functions_to_similarity):
    """ Calculate the semantic similarity metric (Resnik or Wankg) of two sets.
        Similarities between functions are given in functions_to_similarity
        dictionary
    """
    if not set1 or not set2:
        return 0.0

    sim1 = sum_max_similarities(set1, set2, functions_to_similarity) / len(set1)
    sim2 = sum_max_similarities(set2, set1, functions_to_similarity) / len(set2)

    sim = max(sim1, sim2)
    return sim


#-------------------------------------------------------------------------------

def graph_content_jaccard(graph, id_to_protein, annotation_file, path):
    """ Builds interaction graph with content based weighs using Jaccard
        similarity metric, and save it at the given path """
    protein_to_functions = read_in_annotations(annotation_file)
    with open(path, 'w') as out:
        for e in graph.edges_iter():
            terms1 = protein_to_functions.get(id_to_protein[e[0]], None)
            terms2 = protein_to_functions.get(id_to_protein[e[1]], None)
            if terms1 and terms2:
                J = jaccard(terms1, terms2)
                out.write('%d %d %f\n' % (e[0], e[1], J))
            else:
                out.write('%d %d %f\n' % (e[0], e[1], 0.0))


#-------------------------------------------------------------------------------

def read_in_semantic_sim_file (path):
    """ Read in the semantic similarity file with format
        'function function similarity' in a pair-to-similarity dictionary. """

    functions_to_similarity = {}
    with open(path, 'r') as in_file:
        for line in in_file:
            tokens = line.split()
            pair = (min(tokens[0], tokens[1]), max(tokens[0], tokens[1]))
            if tokens[2] != 'NA':
                functions_to_similarity[pair] = float(tokens[2])

    return functions_to_similarity


def graph_content_semantic(graph, id_to_protein, annotation_file, semantic_sim_file, path):
    """ Builds interaction graph with content based weighs using Rasnik
        similarity metric, and save it at the given path """
    protein_to_functions = read_in_annotations(annotation_file)
    functions_to_similarity = read_in_semantic_sim_file(semantic_sim_file)

    with open(path, 'w') as out:
        for e in graph.edges_iter():
            terms1 = protein_to_functions.get(id_to_protein[e[0]], None)
            terms2 = protein_to_functions.get(id_to_protein[e[1]], None)
            if terms1 and terms2:
                w = semantic(terms1, terms2, functions_to_similarity)
                out.write('%d %d %f\n' % (e[0], e[1], w))
            else:
                out.write('%d %d %f\n' % (e[0], e[1], 0.0))


#-------------------------------------------------------------------------------

def graph_structure(graph, content_graph, path):
    """ Builds interaction graph with structure based weighs
        similarity metric, and save it at the given path """
    A = scipy.sparse.csr_matrix(nx.google_matrix(graph, alpha = 1, weight = 'weight'))
    W = nx.to_scipy_sparse_matrix(content_graph)
    W2 = (W.dot(A) + A.transpose().dot(W)) * 0.5
    # rescaling in range 0-1
    max_val = W2.max()
    W2 = W2.multiply(1.0 / max_val)

    save_matrix_to_edgelist(W2, path)


#-------------------------------------------------------------------------------

def graph_hybrid(content_graph, structure_graph, path):
    """ Builds interaction graph with hybrid based weighs
        similarity metric, and save it at the given path """
    W1 = nx.to_scipy_sparse_matrix(content_graph)
    W2 = nx.to_scipy_sparse_matrix(structure_graph)
    W3 = (W1 + W2) * 0.5

    save_matrix_to_edgelist(W3, path)


#-------------------------------------------------------------------------------

def protein_term_graph(graph, id_to_protein, annotation_file, path, nodes_path):
    """ Builds protein-term graph and saves it at the given path. The nodes
        (proteins and terms) and their IDs are saved at nodes_path
    """
    protein_to_functions = read_in_annotations(annotation_file)
    ID = graph.order()
    function_to_id = {}

    for node in graph.nodes():
        p = id_to_protein[node]
        functions = protein_to_functions.get(p, set())
        for f in functions:
            if not f in function_to_id:
                function_to_id[f] = ID
                ID += 1
            graph.add_edge(node, function_to_id[f])

    with open(path, 'w') as out:
        for e in graph.edges_iter():
            out.write('%d %d\n' % (e[0], e[1]))

    with open(nodes_path, 'w') as out:
        for i in id_to_protein:
            out.write('%d %s\n' % (i, id_to_protein[i]))

    with open(nodes_path, 'a') as out:
        for f in function_to_id:
            out.write('%d %s\n' % (function_to_id[f], f))


#-------------------------------------------------------------------------------

def main():
    G, id_to_protein = build_graph('../data/human_ppi_data_900')
    go900 = '../data/go/split/human_ppi900_go_mf_clean.tsv'

    """JACCARD"""
    #graph_content_jaccard(G, id_to_protein, go900, 'graphs/jaccard_content_900')
    #G1 = build_graph_from_edgelist('graphs/jaccard_content_900', G.order())
    #graph_structure(G, G1, 'graphs/jaccard_structure_900')

    #G2 = build_graph_from_edgelist('graphs/jaccard_structure_900', G.order())
    #graph_hybrid(G1, G2, 'graphs/jaccard_hybrid_900')

    """RESNIK"""
    #function_to_function(G, id_to_protein, go900, 'util_data/function_pairs')
    #graph_content_semantic(G, id_to_protein, go900, \
    #                      '../R-src/data/functions_sim_resnik', \
    #                      'graphs/resnik_content_900')
    #G1 = build_graph_from_edgelist('graphs/resnik_content_900', G.order())
    #graph_structure(G, G1, 'graphs/resnik_structure_900')
    #G2 = build_graph_from_edgelist('graphs/resnik_structure_900', G.order())
    #graph_hybrid(G1, G2, 'graphs/resnik_hybrid_900')

    """WANG"""
    #graph_content_semantic(G, id_to_protein, go900, \
    #                      '../R-src/data/functions_sim_wang', \
    #                      'graphs/wang_content_900')
    #G1 = build_graph_from_edgelist('graphs/wang_content_900', G.order())
    #graph_structure(G, G1, 'graphs/wang_structure_900')
    #G2 = build_graph_from_edgelist('graphs/wang_structure_900', G.order())
    #graph_hybrid(G1, G2, 'graphs/wang_hybrid_900')

    """PROTEIN_TERM"""
    #protein_term_graph(G, id_to_protein, go900, \
    #                   'graphs/protein_term_900', \
    #                   'graphs/protein_term_nodes')


#-------------------------------------------------------------------------------

if __name__ == '__main__':
    main()