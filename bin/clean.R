#!/usr/bin/env Rscript
library(tidyverse)

# rails-conf-2019 ----

RailsConf2019 <- rjson::fromJSON(file = "data-raw/rails_conf_2019.json") %>%
  map_dfr(function(event) {
    event[sapply(event, is.null)] <- NA
    data.frame(event)
  }) %>%
  as_tibble()

RailsConf2019$hour <- RailsConf2019$start_time %>%
  str_split_fixed(":", n = 2) %>%
  as_tibble() %>%
  rename(hour = 1, minutes = 2) %>%
  mutate(
    hour = as.integer(hour) + as.double(minutes)/60
  ) %>%
  .$hour

write_csv(RailsConf2019, "data/rails_conf_2019.csv")