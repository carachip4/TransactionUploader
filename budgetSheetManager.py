from dateutil.parser import parse
from categoryUpdater import CategoryUpdater

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


    def __init__(self, transactionSheet, categorySheet, headers, data):
        self.transactionSheet = transactionSheet
        self.categorySheet = categorySheet
        self.headers = headers
        self.fileData = data
        self.startingRow = None


    def printCsvDataToSheet(self):
        self.setStartingRow()
        self.printDateToSheet()
        self.printDescriptionToSheet()
        self.printAmountToSheet()
    
    def updateCategories(self):
        descriptionData = self.getColumnData(self.DESCRIPTION_HEADER)
        categoryUpdater = CategoryUpdater(self.transactionSheet, self.categorySheet, self.startingRow, descriptionData)
        categoryUpdater.updateCategories()


    def setStartingRow(self):
        # find first empty row in date column
        dateColumnValues = self.transactionSheet.col_values(self.DATE_COLUMN_INDEX)
        self.startingRow = len(dateColumnValues) + 1

    def printDateToSheet(self):
        # If 'Transaction Date' is in headers, use that for Chase, otherwise use 'Date' for Ally
        try:
            self.headers.index(self.CHASE_DATE_HEADER)
            self.printDateColumnToSheet(self.CHASE_DATE_HEADER, self.DATE_COLUMN)
        except ValueError:
            self.printDateColumnToSheet(self.ALLY_DATE_HEADER, self.DATE_COLUMN)
            
    def printDescriptionToSheet(self):
        self.printTransactionColumnToSheet(self.DESCRIPTION_HEADER, self.DESCRIPTION_COLUMN)
    
    def printAmountToSheet(self):
        self.printTransactionColumnToSheet(self.AMOUNT_HEADER, self.AMOUNT_COLUMN)
    
    def printTransactionColumnToSheet(self, headerName, column):
        columnData = self.getColumnData(headerName)
        self.printRangeToSheet(column, columnData)
    
    def printDateColumnToSheet(self, headerName, column):
        dateData = self.getColumnData(headerName)
        standardizedDates = [[parse(date[0]).strftime('%m/%d/%Y')] for date in dateData]
        self.printRangeToSheet(column, standardizedDates)

    def getColumnData(self, headerName):
        columnIndex = self.headers.index(headerName)
        columnData = [[row[columnIndex]] for row in self.fileData]
        return columnData
    
    def printRangeToSheet(self, column, columnData):
        range = f'{column}{self.startingRow}:{column}{len(columnData) + self.startingRow}'
        try:
            self.transactionSheet.update(range, columnData)
        except:
            print("Service account did not have edit permissions or could not update for a different reason\nExiting")
            exit()