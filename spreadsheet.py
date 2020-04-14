from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pprint

from src.Logic.database import DB

"""
#to get all the values inside the file
sheet.get_all_values()

#to get exact row values in a second row (Since 1st row is the header)
sheet.row_values(2)

#to get all the column values in the column 'place'
sheet.col_values(16)

#to extract a particular cell value
sheet.cell(1, 1).value
"""

def spreadsheet():
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('Pandemia parser-751d2a06ae54.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open('Контент').get_worksheet(0)
    return sheet

def data_filler(sheet):
    # pp = pprint.PrettyPrinter()
    games = sheet.get_all_values()
    for game in games:
        game = [game[-1].strip()] + game[:5]
        DB.set_game(*game)
    
    print("\n\nUPDATE was finished succesfully\n\n")

if __name__ == "__main__":
    sheet = spreadsheet()
    data_filler(sheet)