#!/usr/bin/python
# -*- coding: utf-8 -*-

import networkx as nx
import time
from interaction_graph_builder import *
from interaction_graph_info import *
from graph_utility import *
from graph_creator import *


#------------------------------------------------------------------------------

def main():
    start = time.time()
    G, id_to_protein = build_graph('../data/human_ppi_data_900')
    random_walk_graph (G,
                      'graphs/random_walk_wang_hybrid_900',
                      'graphs/final/rw_wh_900')
    end = time.time()
    print 'Task finished in: %f min.' % ((end-start) / 60.0)


#------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
