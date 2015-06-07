# Calculate Resnik similarity
library(GOSemSim)

# Read in the protein interactions data in a data frame
# interactions <- read.table(file = "../data/human_ppi_data_900",
#                            header = FALSE,
#                            sep = " ",
#                            #only use first two columns
#                            colClasses = c(rep("character", 2), rep("NULL", 13)),
#                            comment.char = "",
#                            nrows = 165376,
#                            stringsAsFactors = FALSE)

annotations <- unique(read.table(file = "../data/go/split/human_ppi900_go_mf_clean.tsv",
                                 header = FALSE,
                                 sep = "\t",
                                 colClasses = c(rep(c("NULL", "character"), 2), rep("NULL", 4)),
                                 comment.char = "",
                                 nrows = 11019,
                                 stringsAsFactors = FALSE))


print(dim(annotations)) 



s <- goSim("GO:0005525", "GO:0005525", ont = "MF", organism = "human", measure = "Resnik")

print(s)


