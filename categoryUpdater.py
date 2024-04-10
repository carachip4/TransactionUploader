#This class will update the categories based on matches to categories found in your Category sheet
class CategoryUpdater:
    TRANSACTION_CATEGORY_COLUMN = 'C'
    CATEGORY_STARTING_COLUMN = 1
    CATEGORY_TITLES_ROW = 1

    def __init__(self, transactionSheet, categorySheet, startingTransactionRow, descriptionData):
        self.transactionSheet = transactionSheet
        self.categorySheet = categorySheet
        self.startingTransactionRow = startingTransactionRow
        self.descriptionData = descriptionData
        self.categoryInfo = {}
        self.descriptionMatches = {}
        self.loadCategoriesSheet()

    def loadCategoriesSheet(self):
        for column in range(self.CATEGORY_STARTING_COLUMN, len(self.categorySheet.row_values(self.CATEGORY_TITLES_ROW)) + self.CATEGORY_STARTING_COLUMN):
            cellsUnderCategoryHeader = self.categorySheet.col_values(column)
            if len(cellsUnderCategoryHeader) > self.CATEGORY_TITLES_ROW: #it may pick up some extra empty columns we need to filter out
                categoryColumn = cellsUnderCategoryHeader[self.CATEGORY_TITLES_ROW - 1:]
                self.categoryInfo[categoryColumn[0]] = categoryColumn[1:]

    def updateCategories(self):
        categoriesToSet = []

        for i in range(len(self.descriptionData)):
            descriptionValue = self.descriptionData[i][0]
            category = self.findCategory(descriptionValue)
            categoriesToSet.append([category])

        rangeToUpdate = f'{self.TRANSACTION_CATEGORY_COLUMN}{self.startingTransactionRow}:{self.TRANSACTION_CATEGORY_COLUMN}{len(self.descriptionData) + self.startingTransactionRow}'
        try:
            self.transactionSheet.update(rangeToUpdate, categoriesToSet)
        except:
            print("Service account did not have edit permissions or could not update for a different reason\nExiting")
            exit()

    def findCategory(self, description):
        if not description:
            return ""
        
        #skip for loop if we've already seen this description before
        if description in self.descriptionMatches:
            return self.descriptionMatches[description]

        for categoryTitle, keywords in self.categoryInfo.items():
            for keyword in keywords:
                if keyword and keyword.lower() in description.lower():
                    self.descriptionMatches[description.lower()] = categoryTitle
                    return categoryTitle
        return ""
        