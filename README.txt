How to use the Finance Importer

Install python and gspread and oauth2client and python-dateutil
 - pip install gspread oauth2client python-dateutil

Navigate to https://console.cloud.google.com/apis/dashboard
Make a new project (I named mine Import Finances)
Enable Google Api Sheets for your project
Go to credentials and add a Service Account, make sure it has Role = Owner
You will need to share your sheet with the email provided here
Go to the service account (IAM & ADMIN, three elipsis on right - manage keys) and add a key as JSON.
This should download a file that you should put in the same directory as this one.

Edit the constants.py file with your constants
TRANSACTION_SHEET_TITLE is the title on the bottom of your page for the sheet you're using to hold transactions
CATEGORY_SHEET_TITLE is the title on the bottom of your page for the sheet you're using to hold categories
GOOGLE_SHEET_ID = this will be found in your url e.g. spreadsheets/d/<this-id-here>/edit#gid=
GOOGLE_API_CREDENTIALS_FILE = the name of the service account key file you downloaded

As a note - this code assumes the following from your transaction sheet:
Date column is in D
Description column is in F
Amount column is in G
 - and the following from your category sheet:
First category column is C
Titles are on row 3 with their data listed beneath them

If any of these change for you, you will need to edit the constants at the top of budgetSheetManager accordingly (also DATE_COLUMN_INDEX)

This code also assumes that the files downloaded will have the columns
TransactionDate or Date
Description
Amount

If they do not, we may need to write some custom code for your file

To run, type winpty python importfinances.py in the current directory (may exclude "winpty" if on mac)