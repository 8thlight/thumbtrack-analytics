## Google Analytics

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


