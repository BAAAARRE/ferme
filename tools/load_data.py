import pandas as pd
import gspread
from google.oauth2.service_account import Credentials


class GSheets:
    def __init__(self, spreadsheet_id):
        self.spreadsheet_id = spreadsheet_id
        self.spreadsheet = None

    def connect(self):
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]

        # Read the .json file and authenticate with the links
        credentials = Credentials.from_service_account_file(
            'config/credentials.json',
            scopes=scopes
        )

        # Request authorization and open the selected spreadsheet
        spreadsheet = gspread.authorize(credentials).open_by_key(self.spreadsheet_id)
        self.spreadsheet = spreadsheet

    def load_sheets(self):
        list_ws = self.spreadsheet.worksheets()
        for ws in list_ws:
            ws_name = ws.title
            ws_records = ws.get_all_records()
            df = pd.DataFrame(ws_records)
            df.to_csv(f'data/sheets/{ws_name}.csv', index=False)
