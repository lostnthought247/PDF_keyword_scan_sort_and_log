import PyPDF2
import shutil
import os
import csv

# Creates filespaths for root file, input file, and outfile folders
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
filePath = os.path.join(desktop, "ScriptTestFolder", "pdf_scanner", "ToScan")
outfilePath_have = os.path.join(desktop, "ScriptTestFolder", "pdf_scanner", "Have")
outfilePath_not = os.path.join(desktop, "ScriptTestFolder", "pdf_scanner", "HaveNot")
outfilePath_unknown = os.path.join(desktop, "ScriptTestFolder", "pdf_scanner", "Unknown")

# Creates csv sorting log file and headers for sorting log
with open('sort_log.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['File Name', 'Sorted Too', 'Based On'])

# Function that appends the log data for each file in CSV file sorting log
def get_log_info(file, status, trigger):
    with open('sort_log.csv', 'a') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow([file, status, trigger])

# Looks through each file in the ToScan folder file path that ends if "f" for pdf
for file in os.listdir(filePath):
    print(file[-1])
    if file[-1] == "f":
        full_file_path = os.path.join(filePath, file)
        print('xxxxxxxxx', file)

        pdfFileObj = open(full_file_path, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

        # Create string object used to collect all pages text into one file string
        all_file_text = ""

        #Iterates through each page in PDF, extracts text, and adds to file string
        for i in range(pdfReader.numPages):
            pageObj = pdfReader.getPage(i)
            page_text = pageObj.extractText()
            all_file_text += page_text
            #print(all_file_text)

        # Searches file text for keywords then routes/copies files and logs result
        if all_file_text.find("if eligible") > 0:
            shutil.copy(full_file_path, outfilePath_not)
            get_log_info(file, 'Ineligible', "if eligible")
        elif all_file_text.find("not eligible") > 0:
            shutil.copy(full_file_path, outfilePath_not)
            get_log_info(file, 'Ineligible', "not eligible")
        elif all_file_text.find("ineligible") > 0:
            shutil.copy(full_file_path, outfilePath_not)
            get_log_info(file, 'Ineligible', "ineligible")
        elif all_file_text.find("is eligible") > 0:
            shutil.copy(full_file_path, outfilePath_have)
            get_log_info(file, 'Eligible', "is eligible")
        elif all_file_text.find("is considered eligible") > 0:
            shutil.copy(full_file_path, outfilePath_have)
            get_log_info(file, 'Eligible', "is considered eligible")
        else:
            shutil.copy(full_file_path, outfilePath_unknown)
            get_log_info(file, 'Unknown', "No Keyword/Phrase Match Found")
