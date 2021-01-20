## open log connection to file
sink(here::here("log"))

## import libraries
library('dplyr')
library('tidyr')
library('readr')
library('here')
library('ggplot2')

## import data
df_input <- read_csv(here::here("output", "output.csv"))

## select crcl 

crcl <- select(df_input, crcl)

## plot histogram 

crcl_hist <- ggplot(crcl, aes(x=crcl)) + geom_density() 
ggsave(crcl_hist, file = 'crcl_hist.png', path=here::here("output"))
















