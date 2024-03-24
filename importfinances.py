from budgetSheetManager import BudgetSheetManager
from localFileHandler import LocalFileHandler
from googleSheetReader import GoogleSheetReader

#This file will create classes to 
# 1. Open your transaction file
# 2. Open your google sheet
# 3. Print the transaction data to the sheet
def main():
    localFileHandler = LocalFileHandler()
    localFileHandler.openFile()
    
    googleSheetReader = GoogleSheetReader()
    googleSheetReader.getGoogleSheet()

    budgetSheetManager = BudgetSheetManager(googleSheetReader.sheet, headers=localFileHandler.headers, data=localFileHandler.fileData)
    budgetSheetManager.printAllDataToSheet()
    
    localFileHandler.confirmFileDeletion()

if __name__ == '__main__':
    main()