function onEdit(e) {
  var globalVariables = PropertiesService.getScriptProperties();
  var range = e.range;
  var sheet = range.getSheet();
  var sheetName = sheet.getName();
  var editedColumn = range.getColumn();
  var watchColumn = globalVariables.getProperty('transactionDescriptionColumn');
  
  if (sheetName == globalVariables.getProperty('transactionSheetName') && editedColumn == watchColumn) {
    var firstRow = range.getRow();
    var numberOfRows = range.getLastRow() - range.getRow();
    assignCategory(firstRow, numberOfRows);
  }
}

function assignCategory(firstRow, numberOfRows) {
  var globalVariables = PropertiesService.getScriptProperties();
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var transactionsSheet = ss.getSheetByName(globalVariables.getProperty('transactionSheetName'));

  for (var row = firstRow; row < firstRow + numberOfRows + 1; row ++) {
    var descriptionColumn = globalVariables.getProperty('transactionDescriptionColumn');
    var searchValue = transactionsSheet.getRange(row, descriptionColumn).getValue().toLowerCase();
    var category = findCategory(searchValue);
    var categoryColumn = globalVariables.getProperty('transactionCategoryColumn');
    transactionsSheet.getRange(row, categoryColumn).setValue(category);
  }
}

function findCategory(transactionTitle) {
  var CATEGORY_STARTING_COLUMN = 3;
  var CATEGORY_STARTING_ROW = 3;
  if (!transactionTitle) {
    return "";
  }
  var globalVariables = PropertiesService.getScriptProperties();
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var categoriesSheet = ss.getSheetByName(globalVariables.getProperty('categorySheetName'));
  var lastColumn = categoriesSheet.getLastColumn();
  
  for (var column = CATEGORY_STARTING_COLUMN; column <= lastColumn; column++) {
    var categoryTitle = categoriesSheet.getRange(CATEGORY_STARTING_ROW, column).getValue();
    var keywords = categoriesSheet.getRange(CATEGORY_STARTING_ROW + 1, column, categoriesSheet.getLastRow()-1, 1).getValues().flat();
    for (var row = 0; row <= keywords.length; row++) {
      if (keywords[row] == "") {
        break;
      }
      // console.log(`${categoryTitle} - ${keywords[row]} - ${transactionTitle}`)
      if (transactionTitle.toLowerCase().includes(keywords[row].toLowerCase())) {
        return categoryTitle;
      }
    }
  }
  
  return "";
}
