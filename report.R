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
    conference_day_label = factor(labels, levels = labels),
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

label_event_category <- function(frame) {
  levels <- c("DayButton", "Swipe", "ToggleOpen", "Pin", "Outbound Link")
  labels <- c("View Day", "Swipe Timeslot", "Dropdown Timeslot", "Pin Event", "Outbound Link")
  map <- tibble(
    category = levels,
    category_label = factor(levels, levels = levels, labels = labels)
  )
  if(missing(frame)) return(map)
  left_join(frame, map)
}

# data ----

Sessions <- read_csv("data/sessions.csv") %>%
  label_conference_day() %>%
  label_hour()

NewUsers <- read_csv("data/new_users.csv") %>%
  label_conference_day() %>%
  label_hour()

Devices <- read_csv("data/devices.csv")
BrowserSizes <- read_csv("data/browser_sizes.csv")

ClientIDs <- read_csv("data/client_ids.csv")

RailsConf <- read_csv("data/rails_conf_2019.csv")

Events <- read_csv("data/events.csv") %>%
  label_conference_day() %>%
  label_hour() %>%
  label_event_category()

UserExplorer <- read_csv("data/user_explorer.csv")

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

# new-users ----
new_users_plot <- NewUsers %>%
  ggplot() +
  aes(hour, value, group = conference_day) +
  geom_line(aes(color = conference_day_label),
            size = 2) +
  scale_x_continuous(breaks = 0:23) +
  scale_color_brewer(palette = "Set2") +
  t_$base_theme +
  theme(
    legend.position = c(0.15, 0.9)
  ) +
  labs(
    x = "Hour",
    color = "",
    y = "New users",
    title = "New users to railsconf.today"
  )

# devices ----
devices_plot <- Devices %>%
  ggplot() +
  aes(fct_reorder(device, value, .desc = TRUE), value) +
  geom_bar(aes(fill = device), stat = "identity", color = "black") +
  geom_text(aes(label = value), nudge_y = 12) +
  scale_fill_brewer(palette = "Set2", guide = FALSE) +
  t_$base_theme +
  theme(
    panel.grid.major.x = element_blank()
  ) +
  labs(
    x = "",
    y = "Devices",
    title = "Device types"
  )

browser_sizes_plot <- BrowserSizes %>%
  ggplot() +
  aes(width, group = device) +
  geom_density(aes(fill = device), alpha = 0.8, bw = 40) +
  scale_fill_brewer(palette = "Set2") +
  t_$base_theme +
  theme(
    legend.position = c(0.5, 0.8),
    axis.text.y = element_blank()
  ) +
  labs(
    x = "Browser width (pixels)",
    y = "Density",
    fill = "",
    title = "Browser widths by device"
  )

# events ----

events_plot <- Events %>%
  group_by(category, conference_day) %>%
  summarize(
    events = sum(value)
  ) %>%
  label_conference_day() %>%
  label_event_category() %>%
  ggplot() +
  aes(conference_day_label, events) +
  geom_bar(aes(fill = conference_day_label), stat = "identity") +
  facet_wrap("category_label", scales = "free_y", nrow = 1) +
  scale_fill_brewer(palette = "Set2", guide = FALSE) +
  labs(
    x = "",
    y = "Total events"
  ) +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1),
    panel.grid.major.x = element_blank()
  )

# user-explorer ----
user_explorer_plot <- ggplot(UserExplorer) +
  aes(sessions, avg_session_duration) +
  geom_point(position = position_jitter(width = 0.2),
             alpha = 0.8, color = t_$colors("blue"), size = 2) +
  coord_cartesian(xlim = c(1, 30))

# in-text-citations ----

c_ <- list(
  before_conference_visits = filter(Sessions, conference_day_type == "before_conference") %>%
    .$value %>%
    sum(),
  during_conference_visits = filter(Sessions, conference_day_type == "during_conference") %>%
    .$value %>%
    sum(),
  num_devices = nrow(ClientIDs),
  pct_mobile = round(100*(filter(Devices, device == "mobile")$value/sum(Devices$value))),
  min_browser_width = min(BrowserSizes$width),
  min_browser_height = min(BrowserSizes$height)
)