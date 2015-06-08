# Calculate Semantic similarity for given GO functions
library(GOSemSim)

METRIC <- "Resnik"
PATH <- "data/functions_sim_resnik_all"

# Read in function-pairs data in a data frame
functions <- unique(read.table(file = "../python-src/util_data/functions_list",
                               header = FALSE,
                               sep = " ",
                               colClasses = "character",
                               comment.char = "",
                               nrows = 236,
                               stringsAsFactors = FALSE))

con <- file(PATH, "w")

for (i in 1:nrow(functions)) {
  for (j in (i+1):nrow(functions)) {
    sim <- goSim(functions[i, 1], 
                   functions[j, 1], 
                   ont = "MF", 
                   organism = "human", 
                   measure = METRIC)
  
    data = paste(functions[i, 1], functions[j, 1], sim, sep = " ")
    writeLines(text = data,
               con = con)
  }
}

close(con)