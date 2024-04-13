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
    DETAILS_COLUMN = "H"

    def __init__(self, transactionSheet, categorySheet, headers, data, fileSource):
        self.transactionSheet = transactionSheet
        self.categorySheet = categorySheet
        self.headers = headers
        self.fileData = data
        self.startingRow = None
        self.fileSource = fileSource
        self.transactionDataLength = 0

    def printCsvDataToSheet(self):
        self.setStartingRow()
        self.printDateToSheet()
        self.printDescriptionToSheet()
        self.printAmountToSheet()
        self.printSource()
    
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
        self.applyFormatToIncomeValues()
        self.printTransactionColumnToSheet(self.AMOUNT_HEADER, self.AMOUNT_COLUMN, absoluteValue=True)
    
    def printDateColumnToSheet(self, headerName, column):
        dateData = self.getColumnData(headerName)
        standardizedDates = [[parse(date[0]).strftime('%m/%d/%Y')] for date in dateData]
        rangeToUpdate = self.getColumnRange(column, len(standardizedDates))
        self.printRangeToSheet(rangeToUpdate, standardizedDates)

    def printTransactionColumnToSheet(self, headerName, column, absoluteValue = False):
        columnData = self.getColumnData(headerName, absoluteValue)
        self.transactionDataLength = len(columnData)
        rangeToUpdate = self.getColumnRange(column, len(columnData))
        self.printRangeToSheet(rangeToUpdate, columnData)

    def getColumnData(self, headerName, absoluteValue = False):
        columnIndex = self.headers.index(headerName)
        if absoluteValue:
            columnData = [[abs(float(row[columnIndex]))] for row in self.fileData]
        else:
            columnData = [[row[columnIndex]] for row in self.fileData]
        return columnData
    
    def printSource(self):
        if (self.fileSource):
            rangeToUpdate = f'{self.DETAILS_COLUMN}{self.startingRow}:{self.DETAILS_COLUMN}{self.transactionDataLength + self.startingRow}'
            data = [[self.fileSource] for _ in range(self.transactionDataLength)]
            self.printRangeToSheet(rangeToUpdate, data)
            

    def getColumnRange(self, column, dataLength):
        return f'{column}{self.startingRow}:{column}{dataLength + self.startingRow}'
    
    def printRangeToSheet(self, rangeToUpdate, columnData):
        try:
            self.transactionSheet.update(rangeToUpdate, columnData, value_input_option="USER_ENTERED")
        except Exception as ex:
            print(ex)
            # print("Service account did not have edit permissions or could not update for a different reason\nExiting")
            exit()
    
    def applyFormatToIncomeValues(self):
        incomeCells = []
        columnData = self.getColumnData(self.AMOUNT_HEADER)
        for i in range(len(columnData)):
            if float(columnData[i][0]) > 0:
                incomeCells.append(f"{self.AMOUNT_COLUMN}{i + self.startingRow}")

        try:
            self.transactionSheet.format(incomeCells, {"textFormat": {"bold": True}})
        except Exception as ex:
            print(ex)
            exit()