#!/usr/bin/python
# -*- coding: utf-8 -*-

import networkx as nx
from interaction_graph_builder import *
from interaction_graph_info import *

def main():
    G, id_to_protein = build_graph('../data/human_ppi_data_700')

    print nx.info(G)
    print
    print nx.is_connected(G)
    print nx.number_connected_components(G)
    print
    #sg = list(nx.connected_component_subgraphs(g))[0]
    plot_degree_dist (G, 'figures/degree_distribution700.pdf')




if __name__ == '__main__':
    main()