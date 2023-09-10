import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import SHEET_KEY


scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('../creds.json', scope)
client = gspread.authorize(credentials)

spreadsheet = client.open_by_key(SHEET_KEY)
worksheet = spreadsheet.sheet1


def add_entry(user_name, data):
    row = [user_name, data['type'], data['category'], int(data['price'])]
    worksheet.append_row(row)


def show_entrys():
    entrys = worksheet.get_all_values()
    output = ""
    if len(entrys) > 1:
        for entry in entrys[-5:]:
            output += ' - '.join(entry) + '\n'
   
    return output
