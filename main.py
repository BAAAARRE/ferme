import os
from dotenv import load_dotenv

from tools import load_data as ld

load_dotenv()
spreadsheet_id = os.environ.get("SPREADSHEET_ID")


def main():
    ld_gs = ld.GSheets(spreadsheet_id)
    ld_gs.connect()
    ld_gs.load_sheets()

    ld_l = ld.Local()
    ld_l.load_sheets()
    raw_data = ld_l.raw_data
    print(raw_data)


if __name__ == "__main__":
    main()
