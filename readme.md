# Triple Sync

Syncing Tripler data from BlockPower.vote to Google Sheets.

Useful links:
- [How to update a Google Sheet with Python](https://www.analyticsvidhya.com/blog/2020/07/read-and-update-google-spreadsheets-with-python/)

## Credentials:

- Google Sheet Credentials are handled through a Google Cloud service account associated with dev@blockpower.vote
- Service Account in Google Cloud is named `google-sheets@triplesync.iam.gserviceaccount.com`
- The Google Sheets must be shared with the Google Cloud Service Account to give it access

## Environment Variables

- `BLOCKPOWER_API_URL` URL to the blockpower API endpoint (prod or stage) used to load the JSON data
- `BLOCKPOWER_API_JWT` A JWT used to authenticate with Blockpower, expires every 10 days
- `GOOGLE_SHEET_URL` URL of the Google Sheet to update
- `GOOGLE_WORKSHEET_NAME` Name of the worksheet tab of the Google Sheet to update (defaults to "rawTriplerData")


## Install and Run Locally

```
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ python ./triplesync.py
```
