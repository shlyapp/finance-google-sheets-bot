import gspread
from oauth2client.service_account import ServiceAccountCredentials

import pytz

from config import SHEET_KEY


scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('../creds.json', scope)
client = gspread.authorize(credentials)

spreadsheet = client.open_by_key(SHEET_KEY)
worksheet = spreadsheet.sheet1

moscow_time = pytz.timezone('Europe/Moscow')


def add_entry(user_name, date, data):
    date = str(date.astimezone(moscow_time)).split("+")[0]
    row = [user_name, date, data['type'], data['category'], int(data['price'])]
    worksheet.append_row(row)


def show_entrys():
    entrys = worksheet.get_all_values()
    output = ""
    if len(entrys) > 1:
        for entry in entrys[-5:]:
            output += ' - '.join(entry) + '\n'
   
    return output
