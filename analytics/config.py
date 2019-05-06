import json

KEY_FILE_LOCATION = "google-service-account-key.json"
VIEW_ID = json.load(open("google-analytics-view.json"))["view_id"]

RAILS_CONF_DATE_RANGE = {"startDate": "2019-04-28", "endDate": "2019-05-02"}
