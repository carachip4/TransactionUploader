from budgetSheetManager import BudgetSheetManager
from localFileHandler import LocalFileHandler
from googleSheetReader import GoogleSheetReader

#This file will create classes to 
# 1. Open your transaction file
# 2. Open your google sheet
# 3. Print the transaction data to the sheet
def main():
    continueToRead = True
    try:
        localFileHandler = LocalFileHandler()
        localFileHandler.openFile()
        
        googleSheetReader = GoogleSheetReader()
        googleSheetReader.getGoogleSheet()

        budgetSheetManager = BudgetSheetManager(googleSheetReader.transactionSheet, googleSheetReader.categorySheet, headers=localFileHandler.headers, data=localFileHandler.fileData, fileSource=localFileHandler.fileSource)
        budgetSheetManager.printCsvDataToSheet()
        
        localFileHandler.settingCategoriesMessage()
        budgetSheetManager.updateCategories()
        
        localFileHandler.confirmFileDeletion()

        continueToRead = localFileHandler.shouldReadAnotherFile()
    except SystemExit as ex:
        continueToRead = False
        print("Exiting")
        input("")
    except Exception as ex:
        continueToRead = False
        print(ex)
        input("")
    finally:
        return continueToRead

if __name__ == '__main__':
    continueToRead = True
    while continueToRead:
        continueToRead = main()