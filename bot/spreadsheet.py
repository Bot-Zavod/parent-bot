import os

import gspread
from gspread.spreadsheet import Spreadsheet
from oauth2client.service_account import ServiceAccountCredentials

from bot.database import db_interface

# check this, in case you are not
# familiar with google spreadsheets
# https://github.com/burnash/gspread


def get_spreadsheet() -> Spreadsheet:
    """return games spreadsheet"""
    table = os.getenv("GAMES_SHEET")
    tab = 0

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    path = "google_api.json"
    full_path = os.path.abspath(os.path.expanduser(os.path.expandvars(path)))
    creds = ServiceAccountCredentials.from_json_keyfile_name(full_path, scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key(table)
    sheet = sheet.get_worksheet(tab)
    return sheet


# update Games database from Content spreadsheet
def update_games():
    sheet = get_spreadsheet()
    games = sheet.get_all_values()
    games_num = len(games)
    try:
        db_interface.delete_games()
        games_to_insert = [[game[-1].strip()] + game[:5] for game in games]
        db_interface.set_games(games_to_insert)
    except Exception as e:
        return "Failed with " + str(e)
    return f"Games database was succesfully updated with {games_num} games"


if __name__ == "__main__":
    print(update_games())
