#This class will update the categories based on matches to categories found in your Category sheet
class CategoryUpdater:
    TRANSACTION_CATEGORY_COLUMN = 'C'
    CATEGORY_STARTING_COLUMN = 3
    CATEGORY_TITLES_ROW = 3

    def __init__(self, transactionSheet, categorySheet, startingTransactionRow, descriptionData):
        self.transactionSheet = transactionSheet
        self.categorySheet = categorySheet
        self.startingTransactionRow = startingTransactionRow
        self.descriptionData = descriptionData
        self.categoryInfo = {}
        self.loadCategoriesSheet()

    def loadCategoriesSheet(self):
        for column in range(self.CATEGORY_STARTING_COLUMN, len(self.categorySheet.row_values(self.CATEGORY_TITLES_ROW)) + self.CATEGORY_STARTING_COLUMN):
            allCategoryColumns = self.categorySheet.col_values(column)
            if len(allCategoryColumns) > self.CATEGORY_TITLES_ROW: #it may pick up some extra empty columns we need to filter out
                categoryColumn = self.categorySheet.col_values(column)[self.CATEGORY_TITLES_ROW - 1:]
                self.categoryInfo[categoryColumn[0]] = categoryColumn[1:]

    def updateCategories(self):
        for i in range(len(self.descriptionData)):
            descriptionValue = self.descriptionData[i][0]
            category = self.findCategory(descriptionValue)
            rowToUpdate = self.startingTransactionRow + i
            self.transactionSheet.update_acell(f'{self.TRANSACTION_CATEGORY_COLUMN}{rowToUpdate}', category)

    def findCategory(self, description):
        if not description:
            return ""
        
        for categoryTitle, keywords in self.categoryInfo.items():
            for keyword in keywords:
                if keyword and keyword.lower() in description.lower():
                    return categoryTitle
        return ""
        