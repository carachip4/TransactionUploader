import gspread
from oauth2client.service_account import ServiceAccountCredentials
from constants import GOOGLE_SHEET_ID, GOOGLE_API_CREDENTIALS_FILE, WORKSHEET_TITLE

#This class authenticates with google and finds your google sheet
class GoogleSheetReader:
    def __init__(self):
        self.client = None
        self.sheet = None
        self.headers = None
        self.fileData = None
    
    def getGoogleSheet(self):
        self.authenticateCredentials()
        spreadsheet = self.client.open_by_key(GOOGLE_SHEET_ID)
        self.sheet = spreadsheet.worksheet(WORKSHEET_TITLE)

    def authenticateCredentials(self):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_API_CREDENTIALS_FILE, scope)
        self.client = gspread.authorize(creds)
        