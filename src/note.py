import gspread
import pytz

from oauth2client.service_account import ServiceAccountCredentials

from config import TABLE_KEY


scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('../creds.json', scope)
client = gspread.authorize(credentials)

spreadsheet = client.open_by_key(TABLE_KEY)
worksheet = spreadsheet.sheet1

moscow_time = pytz.timezone('Europe/Moscow')


def add_note(user_name, date, data):
    date = str(date.astimezone(moscow_time)).split("+")[0]
    row = [user_name, date, data['type'], data['category'], int(data['price']), data['comment']]
    worksheet.append_row(row)


