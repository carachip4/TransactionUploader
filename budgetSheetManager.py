from dateutil.parser import parse
from categoryUpdater import CategoryUpdater
from ExitException import Exit

# this class handles printing the information from the transaction file on your computer to the google sheet
class BudgetSheetManager:
    DATE_COLUMN = "D"
    DATE_COLUMN_INDEX = 4
    DESCRIPTION_COLUMN = "F"
    AMOUNT_COLUMN = "G"
    DETAILS_COLUMN = "H"

    def __init__(self, transactionSheet, categorySheet):
        self.transactionSheet = transactionSheet
        self.categorySheet = categorySheet
        self.startingRow = None
        self.fileNames = []
        self.fileDates = []
        self.fileAmounts = []
        self.fileDescriptions = []
        self.fileSources = []

    # Handle all at once to minimize number of writes since google services has a limit per minute
    def setFileData(self, fileDetails):
        for fileDetail in fileDetails:
            self.fileNames.append(fileDetail.fileName)
            self.fileDates.extend([parse(date[0]).strftime('%m/%d/%Y')] for date in fileDetail.dates)
            self.fileAmounts.extend(fileDetail.amounts)
            self.fileDescriptions.extend(fileDetail.descriptions)
            self.fileSources.extend([fileDetail.source] for i in range(len(fileDetail.dates)))

    def printCsvDataToSheet(self):
        self.setStartingRow()
        self.applyFormatToIncomeValues()
        self.convertAmountsToAbsoluteValues()

        self.printColumn(self.DATE_COLUMN, self.fileDates)
        self.printColumn(self.DESCRIPTION_COLUMN, self.fileDescriptions)
        self.printColumn(self.AMOUNT_COLUMN, self.fileAmounts)
        self.printColumn(self.DETAILS_COLUMN, self.fileSources)

    def updateCategories(self):
        print("Setting categories, please wait")
        categoryUpdater = CategoryUpdater(self.transactionSheet, self.categorySheet, self.startingRow, self.fileDescriptions)
        categoryUpdater.updateCategories()

    def setStartingRow(self):
        # find first empty row in date column
        dateColumnValues = self.transactionSheet.col_values(self.DATE_COLUMN_INDEX)
        self.startingRow = len(dateColumnValues) + 1
            
    def printColumn(self, header, data):
        rangeToUpdate = self.getColumnRange(header, len(data))
        self.printRangeToSheet(rangeToUpdate, data)     

    def getColumnRange(self, column, dataLength):
        return f'{column}{self.startingRow}:{column}{dataLength + self.startingRow}'
    
    def printRangeToSheet(self, rangeToUpdate, columnData):
        try:
            self.transactionSheet.update(rangeToUpdate, columnData, value_input_option="USER_ENTERED")
        except Exception as ex:
            print(ex)
            # print("Service account did not have edit permissions or could not update for a different reason\nExiting")
            raise Exit
    
    def applyFormatToIncomeValues(self):
        incomeCells = []
        for i in range(len(self.fileAmounts)):
            if float(self.fileAmounts[i][0]) > 0:
                incomeCells.append(f"{self.AMOUNT_COLUMN}{i + self.startingRow}")

        try:
            if len(incomeCells) > 0:
                self.transactionSheet.format(incomeCells, {"textFormat": {"bold": True}})
        except Exception as ex:
            print(ex)
            raise Exit
    
    def convertAmountsToAbsoluteValues(self):
        self.fileAmounts = [[abs(float(amount[0]))] for amount in self.fileAmounts]