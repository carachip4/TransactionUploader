from budgetSheetManager import BudgetSheetManager
from localFileHandler import LocalFileHandler
from googleSheetReader import GoogleSheetReader
from ExitException import Exit

#This file will create classes to 
# 1. Open your google sheet
# 2. Open your transaction file(s)
# 3. Print the transaction data to the sheet
def main():
    try :
        googleSheetReader = GoogleSheetReader()
        googleSheetReader.getGoogleSheet()

        budgetSheetManager = BudgetSheetManager(googleSheetReader.transactionSheet, googleSheetReader.categorySheet)
        localFileHandler = LocalFileHandler()    

        continueToRead = True
        while continueToRead:
            try:
                localFileHandler.openFileAndSetData()
                continueToRead = localFileHandler.shouldReadAnotherFile()
            except Exit as ex:
                continueToRead = localFileHandler.shouldReadAnotherFile()
            except Exception as ex:
                print(ex)
                return
        budgetSheetManager.setFileData(localFileHandler.fileDetails)
        budgetSheetManager.printCsvDataToSheet()
        budgetSheetManager.updateCategories()
        localFileHandler.confirmFileDeletion()
    except Exception as ex:
        print(ex)
        return

if __name__ == '__main__':
    main()
    input("Press enter to exit")