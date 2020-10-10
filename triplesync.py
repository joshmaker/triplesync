import os
from typing import Optional, Union

import gspread
import requests
from oauth2client.service_account import ServiceAccountCredentials

BLOCKPOWER_API_URL = os.getenv("BLOCKPOWER_API_URL")
BLOCKPOWER_API_JWT = os.getenv("BLOCKPOWER_API_JWT")

GOOGLE_SERVICE_ACCOUNT_KEYFILE = "service_account.json"
GOOGLE_SHEET_URL = os.getenv("GOOGLE_SHEET_URL")
GOOGLE_WORKSHEET_NAME = os.getenv("GOOGLE_WORKSHEET_NAME", "rawTriplerData")


def main() -> None:
    """
    Load Tripler data from BlockPower, reformat it, then update a Google Sheet.
    """

    # Make an API call to Blockpower
    blockpower_request_headers = {"Authorization": f"Bearer {BLOCKPOWER_API_JWT}"}
    response = requests.get(BLOCKPOWER_API_URL, headers=blockpower_request_headers)
    data = response.json()

    # Authenticate with Google Sheets
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SERVICE_ACCOUNT_KEYFILE, scope)
    client = gspread.authorize(creds)

    # Connect to the correct Google Sheet, then load the correct worksheet tab
    spreadsheet = client.open_by_url(GOOGLE_SHEET_URL)
    worksheet = next(s for s in spreadsheet.worksheets() if s.title == GOOGLE_WORKSHEET_NAME)

    def format_triplee(triplee: Union[dict, str, None]) -> Optional[str]:
        """
        Update a "triplee" column to match the string format expected by the
        existing Google Sheet.
        """
        if not isinstance(triplee, dict):
            return triplee
        return f"{triplee['first_name']} {triplee['last_name']} - {str(triplee['housemate']).lower()}"

    def format_verification(verification: Optional[str]) -> str:
        """
        Update the "verification" column to match the string format expected by
        the existing Google Sheet.

        The existing format is a JSON blob as text with quotation marks replaced
        by backticks.
        """
        if not verification:
            return "null"
        return verification.replace('"', "`")

    # Update worksheet with latest data
    worksheet.update(
        "A2:O",
        [
            [
                r["voter_id"],
                r["first_name"],
                r["last_name"],
                r["address"]["address1"],
                r["address"]["zip"],
                r["status"],
                r["date_claimed"],
                r["date_confirmed"],
                r["ambassador_name"],
                r["ambassador_external_id"],
                r["phone"],
                format_triplee(r["triplee1"]),
                format_triplee(r["triplee2"]),
                format_triplee(r["triplee3"]),
                format_verification(r["verification"]),
            ]
            for r in data
        ],
    )

    # Resize the worksheet to delete any extra rows possibly left over from the
    # previous data (ie, if the new data was shorter than the old data).
    worksheet.resize(rows=len(data) + 1)


if __name__ == "__main__":
    main()
