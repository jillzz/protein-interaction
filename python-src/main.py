#!/usr/bin/python
# -*- coding: utf-8 -*-

import networkx as nx
from interaction_graph_builder import *
from interaction_graph_info import *

def main():
    G, id_to_protein = build_graph('../data/human_ppi_data_900')
    print 'Graph built!'

    """
    print nx.info(G)
    print
    print nx.is_connected(G)
    print nx.number_connected_components(G)
    print
    #sg = list(nx.connected_component_subgraphs(g))[0]
    """

    #plot_degree_dist (G, 'figures/degree_distribution900.pdf')
    #pearson = nx.degree_pearson_correlation_coefficient(G)
    #plot_clustering_spectrum (G, 'figures/clustering_spectrum700.pdf')
    plot_shortest_path_spectrum (G, 'figures/distance_spectrum900.pdf', 'shortest_paths_900.txt')
    #plot_closeness_dist (G, 'figures/closeness_distribution700.pdf')
    #plot_betweenness_dist (G, 'figures/betweenness_distribution700.pdf')



if __name__ == '__main__':
    main()