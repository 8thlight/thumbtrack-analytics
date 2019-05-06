## Google Analytics

### Service Account Credentials

1. Create a new project through the [Google Developer's Console](https://console.developers.google.com).
1. Enable the Google Analytics Reporting API.
1. Find out what kind of credentials are needed:
    * Which API are you using? **Analytics Reporting API**
    * Where will you be calling the API from? **Other UI (e.g. Windows, CLI tool)
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

### Documentation

* [Creating a Report](https://developers.google.com/analytics/devguides/reporting/core/v4/basics)
* [Analytics Reporting API](https://developers.google.com/analytics/devguides/reporting/core/v4/rest/)
* [Dimensions & Metrics Explorer](https://developers.google.com/analytics/devguides/reporting/core/dimsmets)
