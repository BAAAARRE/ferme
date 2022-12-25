import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import glob


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


class Local:
    def __init__(self):
        self.raw_data = None

    def load_sheets(self):
        """
        Load all csv file in a pandas dataframe from data folder, and put it in dict with file name as key and dataframe as value
        :return: dict.
        """
        list_data_all_path = glob.glob("data/sheets/*.csv")
        data_raw_dict = {}

        for data_all_path in list_data_all_path:
            df = pd.read_csv(data_all_path)
            data_all_path = data_all_path.replace('\\', '/')
            file_name = data_all_path.split('/')[-1]
            file_name_without_extension = file_name.split('.')[0]
            data_raw_dict[f'df_{file_name_without_extension}'] = df
        self.raw_data = data_raw_dict
