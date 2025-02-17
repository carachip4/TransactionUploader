import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials
from constants import GOOGLE_SHEET_ID, GOOGLE_API_CREDENTIALS_FILE, TRANSACTION_SHEET_TITLE, CATEGORY_SHEET_TITLE
from ExitException import Exit

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
        except:
            print("You have not hooked up the correct document or have not yet shared it with the service_account email")
            raise Exit
        try:
            self.transactionSheet = spreadsheet.worksheet(TRANSACTION_SHEET_TITLE)
            self.categorySheet = spreadsheet.worksheet(CATEGORY_SHEET_TITLE)
        except:
            print(f"Cannot find either '{TRANSACTION_SHEET_TITLE}' or '{CATEGORY_SHEET_TITLE}' in your google sheet")
            raise Exit
            

    def authenticateCredentials(self):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        currentDirectory = os.path.dirname(os.path.realpath(__file__))
        pathToCredentialsFile = os.path.join(currentDirectory, GOOGLE_API_CREDENTIALS_FILE)
        creds = ServiceAccountCredentials.from_json_keyfile_name(pathToCredentialsFile, scope)
        self.client = gspread.authorize(creds)
        