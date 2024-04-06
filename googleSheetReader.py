import gspread
from oauth2client.service_account import ServiceAccountCredentials
from constants import GOOGLE_SHEET_ID, GOOGLE_API_CREDENTIALS_FILE, TRANSACTION_SHEET_TITLE, CATEGORY_SHEET_TITLE

#This class authenticates with google and finds your google sheet
class GoogleSheetReader:
    def __init__(self):
        self.client = None
        self.transactionSheet = None
        self.categorySheet = None
        self.headers = None
        self.fileData = None
    
    def getGoogleSheet(self):
        self.authenticateCredentials()
        try:
            spreadsheet = self.client.open_by_key(GOOGLE_SHEET_ID)
            self.transactionSheet = spreadsheet.worksheet(TRANSACTION_SHEET_TITLE)
            self.categorySheet = spreadsheet.worksheet(CATEGORY_SHEET_TITLE)
        except:
            print("You have not hooked up the correct document or have not yet shared it with the service_account email\nExiting")
            quit()
            

    def authenticateCredentials(self):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_API_CREDENTIALS_FILE, scope)
        self.client = gspread.authorize(creds)
        