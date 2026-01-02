# Overview
The purpose of this application is to simplify the process of importing bank and credit card transactions into Google Sheets for budgeting. The steps below will walk you through how to install and use the Python script that will easily be able to read transaction data from CSV files and automatically popuplate a Google Sheet with relevant details such as name, date, and amount.

## Key Features
- <b>Automated Data Import</b>: Download your transaction CSV, run the script, and import data into your Google Sheet without manual entry.
- <b>Transaction Categorization</b>: Set up a dedicated tab for category names in your Google Sheet, allowing the script to automatically categorize transactions based on predifined names (e.g. tagging "Walmart", "Costco", or "Target" as "Groceries")

# How to use the Finance Importer

## Required Installations
1. Install python if it isn't already (https://www.python.org/downloads/) 
2. From either powershell (windows) or terminal (mac) you can now install the rest of the necessary python packages by running the following command:

    ```pip install gspread oauth2client python-dateutil```

## Download this Repository
1. Click the `Code` dropdown
2. Click Download ZIP
3. Unzip wherever you'd like on your machine

## Give the App Access to Your Google Sheet
1. Navigate to https://console.cloud.google.com/apis/dashboard
2. Make a new project and name it something like Import Finances
3. Enable Google Api Sheets for your project
4. Go to credentials and add a Service Account, make sure it has Role = Owner
5. You will need to share your sheet with the email provided here
6. Go to the service account (IAM & ADMIN, three elipsis on right - manage keys) and add a key as JSON.
7. This should download a file that you should put in the same directory as where you put your app code

## Update Constraints File
1. Navigate to the constants.py
2. You will need to update each value
    - <b>TRANSACTION_SHEET_TITLE</b> : the title on the bottom of your page for the sheet you're using to hold transactions
    - <b>CATEGORY_SHEET_TITLE</b> : the title on the bottom of your page for the sheet you're using to hold categories
    - <b>GOOGLE_SHEET_ID</b> : this will be found in your url e.g. spreadsheets/d/\<this-id-here\>/edit#gid=
    - <b>GOOGLE_API_CREDENTIALS_FILE</b> : the file name of the service account key you downloaded

## Notes and Possible Setup
Unless you specify the file you want to use, this script will grab the most recent .csv file from your downloads folder. Please download your transactions as CSV files

This code assumes the following from your google sheet on the <u>Transactions</u> tab:
  - Date column is in D
  - Description column is in F
  - Amount column is in G
and the following from your google sheet on the <u>Categories</u> tab:
  - First category column is C
  - Titles are on row 3 with their data listed beneath them

If any of these change for you, you will need to edit the constants at the top of budgetSheetManager accordingly (also DATE_COLUMN_INDEX)

This code also assumes that the files downloaded will have the columns
  - TransactionDate or Date
  - Description
  - Amount

If they do not, we may need to write some custom code for your file

## Running the Script
There are two options for running the script. The first option will be to drag a file to your Desktop and then you can double click to run it. The second is to run it directly from the command line. 

### Desktop App
Edit `runImportFinances.bat` and put in the *path to the importfinances.py to your Desktop and you can double click from there. Note: you can only specify the downloaded file you want to run the script on if you run this script from a terminal

### Running Manually
This will be easier if you download gitbash (https://git-scm.com/downloads) which is a Unix based terminal

To run, open gitbash and navigate to the directory. This terminal view is very similar to your file explorer except you can run more commands from here. Some helpful tips for navigating around
- `ls` will list all items in the current directory
- `cd <folder_name>` will move you into a folder
- `cd c:` will move you into the c drive
- `winpty python importfinances.py <path/to/file>` will run the script once you're in the correct directory (just `python importfinances.py` if on mac)
    - You'll note that you can provide your file if you do it this way. Your file could be anywhere in your directory, you'll just have to make sure you get the *path correct

### *Finding a File or Folders Path
Find the file in file explorer and then click on the top bar that shows the breadcrumb trail pointing to your current location. That should then highlight the current path which you can copy and paste

#### TODO
If fail at any point, loop back to start instead of quitting
