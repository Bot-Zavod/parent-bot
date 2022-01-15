from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pprint
import os
from os

from src.database import DB

"""
check this, in case you are not
familiar with google spreadsheets

https://github.com/burnash/gspread
"""

# return one of two spreadsheets


def spreadsheet(tab: int) -> object:
    if tab == 0:
        table = os.getenv("GAMES")
    elif tab == 1:
        table = os.getenv("PAYMENTS")
    else:
        raise ValueError(f"Not known tab {tab}")

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    path = 'Vargan-API.json'
    full_path = os.path.abspath(os.path.expanduser(
        os.path.expandvars(path)))
    creds = ServiceAccountCredentials.from_json_keyfile_name(full_path, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(table)
    sheet = sheet.get_worksheet(0)
    return sheet


# update Games database from Content spreadsheet
def update_games():
    sheet = spreadsheet(0)
    games = sheet.get_all_values()
    games_num = len(games)
    try:
        DB.delete_games()
        games_to_insert = [[game[-1].strip()] + game[:5] for game in games]
        DB.set_games(games_to_insert)
    except Exception as e:
        return "Failed with " + str(e)
    return f"Games database was succesfully updated with {games_num} games"


# update payments spredsheet from Payments database
def update_users():
    try:
        payments = DB.get_payments_data()
        users_num = len(payments)
        sheet = spreadsheet(1)
        sheet.update("A2", payments)
    except Exception as e:
        return "Failed with " + str(e)
    return f"Payments spredsheet was succesfully updated with {users_num} users\n\n" +\
        "https://docs.google.com/spreadsheets/d/1ntVH1ze2jd5XjfajdAQu9cBMKkCeWsl__PxQtDmC-eQ"


if __name__ == "__main__":
    print(update_games())
