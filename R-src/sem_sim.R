# Calculate Semantic similarity for given GO function pairs
library(GOSemSim)

METRIC <- "Wang"
PATH <- "data/functions_sim_wang"

# Read in function-pairs data in a data frame
function_pairs <- unique(read.table(file = "../python-src/util_data/function_pairs",
                                   header = FALSE,
                                   sep = " ",
                                   colClasses = c(rep("character", 2)),
                                   comment.char = "",
                                   nrows = 8348,
                                   stringsAsFactors = FALSE))
f1 <- function_pairs[, 1]
f2 <- function_pairs[, 2]

con <- file(PATH, "w")

for (i in seq_along(f1)) {
  r_sim <- goSim(f1[i], 
                 f2[i], 
                 ont = "MF", 
                 organism = "human", 
                 measure = METRIC)
  
  data = paste(f1[i], f2[i], r_sim, sep = " ")
  writeLines(text = data,
             con = con)
}

close(con)





