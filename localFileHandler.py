import argparse
import csv
import glob
import os
from ExitException import Exit

#This class will find the most recently downloaded csv file and will verify with the user to use that file and to delete it when done
class LocalFileHandler:
    YES_NO_MESSAGE = "\nFor yes, press enter or type 'yes'\nFor no, type 'no'\n"
    NO_INPUT_OPTIONS = ['n','no']
    YES_INPUT_OPTIONS = ['', 'yes', 'y']

    def __init__(self):
        self.filename = ""
        self.fileSource = ""
        self.headers = None
        self.fileData = None

    def openFile(self):
        self.getFileName()
        self.confirmFileSelection()
        self.requestFileSource()

        with open(self.filename, 'r') as file:
            print("Reading file...")
            csv_data = csv.reader(file)
            data = list(csv_data)
            if not data:
                self.confirmFileDeletion(empty=True)
                self.exitScript()
            # WellsFargo does not have headers
            if "CreditCard1" in self.filename:
                self.headers = ["Date","Amount", "", "", "Description"]
                self.fileData = data
            elif "Chase" in self.filename:
                self.headers = ["Date", "", "Description", "", "", "Amount", ""]
                self.fileData = data[1:]
            else:
                self.headers = ["Date", "", "Amount", "", "Description"]
                self.fileData = data[1:]

    def getFileName(self):
        args = self.parseArguments()
        if args.filename:
            self.filename = args.filename
        else:
            self.filename = self.getMostRecentFileFromDownloads()
    
    def requestFileSource(self):
        self.fileSource = input("Would you like to provide a source? (Enter to skip)\n")

    def confirmFileSelection(self):
        validReadFromFileInput = False
        while not validReadFromFileInput:
            readFromFile = input(f"Read from file {self.filename}?").lower()
            if readFromFile in self.NO_INPUT_OPTIONS:
                print("Will not read file.")
                self.exitScript()
            elif readFromFile in self.YES_INPUT_OPTIONS:
                validReadFromFileInput = True
            else:
                print("Invalid option")

    def confirmFileDeletion(self, empty = False):
        if not empty:
            print("Finished reading from file")
        else:
            print("File was empty.")
        deleteFile = input(f"Would you like to delete {self.filename}?").lower()
        if deleteFile in self.YES_INPUT_OPTIONS:
            os.remove(self.filename)
            print("File deleted.")
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
        
        if allCsvFiles:
            return allCsvFiles[0]
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
        
    def settingCategoriesMessage(self):
        print("Setting categories, please wait")

    def shouldReadAnotherFile(self):
        readAnother = input("Would you like to try to upload another file?").lower()
        if readAnother in self.YES_INPUT_OPTIONS:
            return True
        return False