library(igraph)

# Read in graph data in a data frame
edgelist <- unique(read.table(file = "../python-src/graphs/final/rw_jh_900",
                              header = FALSE,
                              sep = " ",
                              colClasses = c(rep("numeric", 3)),
                              comment.char = "",
                              nrows = 82473,
                              stringsAsFactors = FALSE))

# Build the graph
g <- graph.data.frame(edgelist, directed = FALSE, vertices = NULL)
E(g)$weight 

lc = multilevel.community(g, weights = NULL)
clusters = communities(lc)
dendPlot(clusters)
#print(clusters)
for (i in clusters) {
  print(length(i))
} 


#options(max.print = 99999)
#print(g, full=TRUE, edge.attributes=TRUE)
