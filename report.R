# ---- report
library(tidyverse)

set.seed(213)

# theme elements ----

t_ <- list(
  base_theme = theme(
    panel.grid.minor = element_blank()
  ),
  scale_y_visits = scale_y_continuous("Visits", breaks = seq(0, 100, by = 10)),
  ylim_visits = c(0, 100),
  colors = function(...) {
    theme_colors <- RColorBrewer::brewer.pal(4, "Set2")
    names(theme_colors) <- c("blue", "orange", "green", "pink")
    unname(theme_colors[c(...)])
  }
)


label_conference_day <- function(frame) {
  types <- c("before_conference", rep("during_conference", 3))
  labels <- c("Day before", "Day 1", "Day 2", "Day 3")
  map <- tibble(
    conference_day = c(-1, 1, 2, 3),
    conference_day_label = labels,
    conference_day_type = types
  )
  if(missing(frame)) return(map)
  left_join(frame, map)
}

label_hour <- function(frame) {
  levels <- c("during_conference", "after_hours")
  labels <- c("During conference", "After hours")
  during_conference <- 9:18
  after_hours <- setdiff(0:23, during_conference)
  types <- rep(levels, times = c(length(during_conference), length(after_hours)))
  map <- tibble(
    hour = c(during_conference, after_hours) %>% as.double(),
    hour_type = types,
    hour_type_label = factor(types, levels = levels, labels = labels)
  )
  if(missing(frame)) return(map)
  left_join(frame, map)
}

# data ----

Sessions <- read_csv("data/sessions.csv") %>%
  label_conference_day() %>%
  label_hour()

ClientIDs <- read_csv("data/client_ids.csv")

RailsConf <- read_csv("data/rails_conf_2019.csv")

# visits ----

sessions_per_hour_plot <- Sessions %>%
  ggplot() +
  aes(hour, group = conference_day) +
  geom_line(aes(y = value, color = conference_day_label),
            size = 2) +
  geom_rug(data = distinct(RailsConf, hour, conference_day),
           color = "gray", size = 1.2) +
  scale_x_continuous(breaks = 0:23) +
  t_$scale_y_visits +
  scale_color_brewer(palette = "Set2") +
  coord_cartesian(ylim = t_$ylim_visits, expand = FALSE) +
  labs(
    x = "Hour",
    color = "",
    title = "Visits per hour to railsconf.today"
  ) +
  t_$base_theme +
  theme(
    legend.position = c(0.1, 0.9)
  )

conference_day_type_plot <- Sessions %>%
  filter(hour_type == "during_conference") %>%
  ggplot() +
  aes(conference_day_type, value) +
  geom_point(aes(color = conference_day_type),
             position = position_jitter(width = 0.1, height = 0)) +
  scale_x_discrete(labels = c("Before conference", "During conference")) +
  t_$scale_y_visits +
  scale_color_manual(values = t_$colors("blue", "green"), guide = FALSE) +
  coord_cartesian(ylim = t_$ylim_visits) +
  labs(
    x = "",
    y = "Visits",
    color = "",
    title = "Days before and during",
    subtitle = "Visits per hour before the conference\ncompared to during the conference"
  ) +
  t_$base_theme +
  theme(
    panel.grid.major.x = element_blank()
  )

hour_type_plot <- Sessions %>%
  filter(conference_day_type == "during_conference") %>%
  ggplot() +
  aes(hour_type_label, value) +
  geom_point(aes(color = hour_type_label),
             position = position_jitter(width = 0.1, height = 0)) +
  scale_color_manual(values = t_$colors("green", "blue"), guide = FALSE) +
  t_$scale_y_visits +
  coord_cartesian(ylim = t_$ylim_visits) +
  labs(
    x = "",
    title = "Hours during and after",
    subtitle = "Visits per hour during conference hours\ncompared to after hours."
  ) +
  t_$base_theme +
  theme(
    panel.grid.major.x = element_blank()
  )

# in text citations

c_ <- list(
  before_conference_visits = filter(Sessions, conference_day_type == "before_conference") %>%
    .$value %>%
    sum(),
  during_conference_visits = filter(Sessions, conference_day_type == "during_conference") %>%
    .$value %>%
    sum(),
  num_devices = nrow(ClientIDs)
)
