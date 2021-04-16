#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)
if (length(args) != 2) {
  stop('Check number of arguments')
}
s.fp_in <- args[1]
s.fp_out <- args[2]

# Libraries
library(reshape2)

# Data
d <- read.table(s.fp_in, header=TRUE, sep=',')

# Get values for output
v.relationship_op_map <- list(
  'GreaterThan'='>',
  'Equals'='',
  'LessThan'='<'
)
d$mic_text <- paste0(v.relationship_op_map[d$relationship_operator], d$mic)

# Cast
d.long <- dcast(
  d,
  id + labid + isolate_number + creation_date_timestamp + final_date_timestamp ~ long_name,
  fun.aggregate=identity,
  fill=NA_character_,
  value.var='mic_text'
)

# Write
write.table(d.long, s.fp_out, sep=',', row.names=FALSE)