# Thumbtrack Analytics

Thumbtrack is a "mobile first" web app for conferences. Users can browse
the conference schedule, swipe and dropdown to view events in parallel sessions,
and pin events they want to see.

This repo contains an analysis of the site traffic and user events during
RailsConf 2019.

## Google Analytics

### Service Account Credentials

1. Create a new project through the [Google Developer's Console](https://console.developers.google.com).
1. Enable the Google Analytics Reporting API.
1. Find out what kind of credentials are needed:
    * Which API are you using? **Analytics Reporting API**
    * Where will you be calling the API from? **Other UI (e.g. Windows, CLI tool)**
    * What data will you be accessing? **Application data**
1. Create a service account.
    * Service account name: **thumbtrack-analytics**
    * Role: Project Viewer
    * Service account ID: thumbtrack-analytics (@thumbtrack.iam.gserviceaccount.com)
    * Key type: JSON
1. Move the key into the project as "google-service-account-key.json"

### Analytics Reporting

1. Extract the email address from the generated service account key, and add it as a User to the Google Analytics project.
1. Grab the View ID for the web site, and store it in "google-analytics-view.json".

### Helpful links

* [Creating a Report](https://developers.google.com/analytics/devguides/reporting/core/v4/basics)
* [Analytics Reporting API](https://developers.google.com/analytics/devguides/reporting/core/v4/rest/)
* [Dimensions & Metrics Explorer](https://developers.google.com/analytics/devguides/reporting/core/dimsmets)

## Python environment

```bash
pipenv install --dev
```

## Getting the data

The code for downloading and processing data via the Google Analytics API
is in the python module "analytics".

```bash
python -m analytics --list  # list available reports
python -m analytics --all   # collect all report data 
```

## Compiling the report

The report, [report.Rmd](./report.Rmd) is written in Rmarkdown,
and compiled to output formats using the R package "rmarkdown".
The build process is contained in the "Makefile" for the project.

```bash
make
```
