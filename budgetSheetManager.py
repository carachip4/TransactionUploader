# this class handles printing the information from the transaction file on your computer to the google sheet
class BudgetSheetManager:
    CHASE_DATE_HEADER = "Transaction Date"
    ALLY_DATE_HEADER = "Date"
    DATE_COLUMN = "D"
    DATE_COLUMN_INDEX = 4
    DESCRIPTION_HEADER = "Description"
    DESCRIPTION_COLUMN = "F"
    AMOUNT_HEADER = "Amount"
    AMOUNT_COLUMN = "G"


    def __init__(self, budgetSheet, headers, data):
        self.budgetSheet = budgetSheet
        self.headers = headers
        self.fileData = data
        self.startingRow = None


    def printAllDataToSheet(self):
        self.setStartingRow()
        self.printDateToSheet()
        self.printDescriptionToSheet()
        self.printAmountToSheet()


    def setStartingRow(self):
        dateColumnValues = self.budgetSheet.col_values(self.DATE_COLUMN_INDEX)
        self.startingRow = len(dateColumnValues) + 1

    def printDateToSheet(self):
        try:
            self.headers.index(self.CHASE_DATE_HEADER)
            self.printTransactionColumnToSheet(self.CHASE_DATE_HEADER, self.DATE_COLUMN)
        except ValueError:
            self.printTransactionColumnToSheet(self.ALLY_DATE_HEADER, self.DATE_COLUMN)
            
    def printDescriptionToSheet(self):
        self.printTransactionColumnToSheet(self.DESCRIPTION_HEADER, self.DESCRIPTION_COLUMN)
    
    def printAmountToSheet(self):
        self.printTransactionColumnToSheet(self.AMOUNT_HEADER, self.AMOUNT_COLUMN)
    
    def printTransactionColumnToSheet(self, headerName, column):
        columnIndex = self.headers.index(headerName)
        columnData = [[row[columnIndex]] for row in self.fileData]
        range = f'{column}{self.startingRow}:{column}{len(columnData) + self.startingRow}'
        try:
            self.budgetSheet.update(range, columnData)
        except:
            print("Service account did not have edit permissions\nExiting")
            exit()