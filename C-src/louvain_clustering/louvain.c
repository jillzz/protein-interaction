#include <igraph.h>
#include <igraph_interface.h>


void show_results (igraph_t *g, igraph_vector_t *membership,
            igraph_matrix_t *memberships, igraph_vector_t *modularity, FILE* f) {
    long int i, j, no_of_nodes = igraph_vcount(g);

    j = igraph_vector_which_max(modularity);
    for (i=0; i<igraph_vector_size(membership); i++) {
        if (VECTOR(*membership)[i] != MATRIX(*memberships, j, i)) {
            fprintf(f, "WARNING: best membership vector element %li does not match the best one in the membership matrix\n", i);
        }
    }

    //fprintf(f, "Modularities:\n");
    //igraph_vector_print(modularity);
    //printf("%f", sizeof(membership)/sizeof(membership))

    for (i=0; i < igraph_matrix_nrow(memberships); i++) {
        fprintf(f, "Cluster %d:\n", i);
        for (j=0; j < no_of_nodes; j++) {
            fprintf(f, "%ld ", (long int)MATRIX(*memberships, i, j));
        }
        fprintf(f, "\n");
    }

    fprintf(f, "\n");
}


int main() {

    igraph_t G;
    FILE * input, * output;
    igraph_vector_t membership, modularity;
    igraph_matrix_t memberships;

    // Read in the graph
    input = fopen("../../python-src/graphs/final/rw_jh_900", "r");
    if (!input) {
        return 1;
    }
    //igraph_read_graph_edgelist(&G, input, 0, 0);
    igraph_read_graph_ncol(&G, input, NULL, 0, IGRAPH_ADD_WEIGHTS_YES, IGRAPH_UNDIRECTED);
    fclose(input);

    // Initialize vector
    igraph_vector_init(&modularity,0);
    igraph_vector_init(&membership,0);
    igraph_matrix_init(&memberships,0,0);

    // Louvain multilevel clustering
    igraph_community_multilevel(&G, NULL, &membership, &memberships, &modularity);

    output = fopen("/home/verica/Desktop/louvain_clustering", "w");
    if (!output) {
        return 2;
    }
    show_results(&G, &membership, &memberships, &modularity, output);
    fclose(output);

    return 0;
}
