## open log connection to file
sink(here::here("log"))

## import libraries
library('dplyr')
library('tidyr')
library('readr')
library('here')
library('ggplot2')

## import data
df_input <- read_csv(here::here("output", "input_2.csv"))

#mean arterial pressure 
#df_input <- mutate(df_input, map = bp_dys + 0.33*(bp_sys-bp_dys))

#cockgroft-gault equation 
df_input <- mutate(df_input, crcl = ifelse(sex=="M",((140 - age)*weight)/(0.814*baseline_creatinine), ((0.85*(140 - age)*weight)/(0.814*baseline_creatinine))))


write.csv(df_input, 'output/output.csv')



