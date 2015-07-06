#!/usr/bin/python
# -*- coding: utf-8 -*-

import community


#-------------------------------------------------------------------------------

def to_clusters_dict (partition):
    """ Get partition as returned by community implementation of louvain clustering
        and return a dictionary where each cluster is a key, and the values are
        sets of nodes that belong to that cluster
    """
    cluster_dict = {}
    for node in partition:
        cluster = partition[node]
        if not cluster in cluster_dict:
            cluster_dict[cluster] = set()
        cluster_dict[cluster].add(node)
    return cluster_dict


def louvain (graph):
    """ Louvain clustering, returns dictionary where each key is the level of
        clustering and the values are the clustering themselfs as returned by
        to_clusters_dict method.
    """
    community.__MIN = 1e-12
    dendo = community.generate_dendrogram(graph)
    multilevel = {}
    for level in range(len(dendo) - 1):
        tmp = community.partition_at_level(dendo, level)
        # tmp is a dictionary where keys are the nodes and the values are the set it belongs to
        multilevel[level] = to_clusters_dict(tmp)

    return multilevel


def louvain_best(graph):
    """ Lovain clustering, returns only the best clustering """
    partition = community.best_partition(graph)
    return {0: to_clusters_dict (partition)}