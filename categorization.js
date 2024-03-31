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
  if (!transactionTitle) {
    return "";
  }
  var globalVariables = PropertiesService.getScriptProperties();
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var categoriesSheet = ss.getSheetByName(globalVariables.getProperty('categorySheetName'));
  var lastColumn = categoriesSheet.getLastColumn();
  
  for (var column = 1; column <= lastColumn; column++) {
    var categoryTitle = categoriesSheet.getRange(1, column).getValue();
    var keywords = categoriesSheet.getRange(2, column, categoriesSheet.getLastRow()-1, 1).getValues().flat();
    
    for (var row = 1; row <= keywords.length; row++) {
      if (keywords[row-1] == "") {
        break;
      }
      if (transactionTitle.toLowerCase().includes(keywords[row-1].toLowerCase())) {
        return categoryTitle;
      }
    }
  }
  
  return "";
}
