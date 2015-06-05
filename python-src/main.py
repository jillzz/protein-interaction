#!/usr/bin/python
# -*- coding: utf-8 -*-

import networkx as nx
from interaction_graph_builder import *
from interaction_graph_info import *

def main():
    G, id_to_protein = build_graph('../data/human_ppi_data_900')
    go700 = '../data/go/split/human_ppi700_go_mf_clean.tsv'
    go900 = '../data/go/split/human_ppi900_go_mf_clean.tsv'

    #save_shortest_paths(G, 'shortest_paths_700_improved.txt')

    #plot_degree_dist (G, 'figures/degree_distribution900.pdf')
    #pearson = nx.degree_pearson_correlation_coefficient(G)
    #plot_clustering_spectrum (G, 'figures/clustering_spectrum700.pdf')
    #plot_shortest_path_spectrum (G, 'figures/distance_spectrum900_new.pdf', \
    #                             'distances_data/shortest_paths_900_improved')
    #plot_closeness_dist (G, 'figures/closeness_distribution700.pdf')
    #plot_betweenness_dist (G, 'figures/betweenness_distribution700.pdf')
    #plot_proteins_sharing_function(id_to_protein, \
    #                               go900, \
    #                               'distances_data/shortest_paths_900_improved', \
    #                               'figures/function_sharing900.pdf')

    plot_function_first_appearance(id_to_protein, \
                                   go900, \
                                   'distances_data/shortest_paths_900_sorted', \
                                   'figures/function_appearance900.pdf', 14)



if __name__ == '__main__':
    main()