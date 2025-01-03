import csv
import glob
import os
import argparse
from ExitException import Exit
from FileDetails import FileDetails

#This class will find the most recently downloaded csv file and will verify with the user to use that file and to delete it when done
class LocalFileHandler:
    YES_NO_MESSAGE = "\nFor yes, press enter or type 'yes'\nFor no, type 'no'\n"
    NO_INPUT_OPTIONS = ['n','no']
    YES_INPUT_OPTIONS = ['', 'yes', 'y']

    def __init__(self):
        self.fileDetails = []
        self.parsedFileFromArguments = False

    def openFileAndSetData(self):
        fileName = self.getFileName()
        self.confirmFileSelection(fileName)
        # fileSource = self.requestFileSource() # can keep over here if file type is uncertain
        
        with open(fileName, 'r') as file:
            print("Reading file...")
            csv_data = csv.reader(file)
            data = list(csv_data)
            if not data:
                print("File is empty.")
                self.exitScript()
            # WellsFargo does not have headers
            if "CreditCard1" in fileName:
                fileSource = "WellsFargo"
                # fileHeaders = ["Date","Amount", "", "", "Description"]
                dateIndex = 0
                amountIndex = 1
                descriptionIndex = 4
                fileData = data
            elif "Chase" in fileName:
                fileSource = "Chase"
                # fileHeaders = ["Date", "", "Description", "", "", "Amount", ""]
                dateIndex = 0
                amountIndex = 5
                descriptionIndex = 2
                fileData = data[1:]
            else:
                fileSource = self.requestFileSource()
                # fileHeaders = ["Date", "", "Amount", "", "Description"]
                dateIndex = 0
                amountIndex = 2
                descriptionIndex = 4
                fileData = data[1:]
            dates = self.getColumnData(dateIndex, fileData)
            amounts = self.getColumnData(amountIndex, fileData)
            descriptions = self.getColumnData(descriptionIndex, fileData)

        self.fileDetails.append(FileDetails(fileName, fileSource, dates, amounts, descriptions))

    def getColumnData(self, columnIndex, fileData):
        return [[row[columnIndex]] for row in fileData]

    def getFileName(self):
        args = self.parseArguments()
        if args.filename:
            self.parsedFileFromArguments = True
            self.filename = args.filename
        else:
            return self.getMostRecentFileFromDownloads()
    
    def requestFileSource(self):
        return input("Would you like to provide a source? (Enter to skip)\n")

    def confirmFileSelection(self, fileName):
        validReadFromFileInput = False
        while not validReadFromFileInput:
            readFromFile = input(f"Read from file {fileName}?").lower()
            if readFromFile in self.NO_INPUT_OPTIONS:
                print("Will not read file.")
                self.exitScript()
            elif readFromFile in self.YES_INPUT_OPTIONS:
                validReadFromFileInput = True
            else:
                print("Invalid option")

    def confirmFileDeletion(self):
        deleteFile = input(f"Would you like to delete csv files?").lower()
        if deleteFile in self.YES_INPUT_OPTIONS:
            for fileDetails in self.fileDetails:
                os.remove(fileDetails.fileName)
                print(f'{fileDetails.fileName} deleted.')
        elif deleteFile in self.NO_INPUT_OPTIONS:
            print("Will not delete file.")
        else:
            print("Not a valid input, will not delete file.")


    def exitScript(self):
        raise Exit

    def getMostRecentFileFromDownloads(self):
        downloads_path = os.path.join(os.getenv('USERPROFILE'), 'Downloads')
        allDownloadItems = glob.glob(os.path.join(downloads_path, '*'))
        allDownloadFiles = [file for file in allDownloadItems if os.path.isfile(file)]
        allCsvFiles = [file for file in allDownloadFiles if os.path.splitext(file)[1].lower() == '.csv']
        allCsvFiles.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        
        numberOfFilesRead = len(self.fileDetails)
        if allCsvFiles and numberOfFilesRead < len(allCsvFiles):
            return allCsvFiles[numberOfFilesRead]
        else:
            print(f"No csv files found in {downloads_path}")
            self.exitScript()


    def parseArguments(self):
        parser = argparse.ArgumentParser(description="Import budget transactional data into google sheets.")
        parser.add_argument("--filename", type=self.csv_file, default=None, help="Name of the file to be imported.")
        return parser.parse_args()

    def csv_file(self, param):
        base, ext = os.path.splitext(param)
        if ext.lower() != '.csv':
            raise argparse.ArgumentTypeError('File must have a csv extension')
        return param

    def shouldReadAnotherFile(self):
        if self.parsedFileFromArguments:
            return False
        readAnother = input("Would you like to try to upload another file?").lower()
        if readAnother in self.YES_INPUT_OPTIONS:
            return True
        return False