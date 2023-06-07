import pathlib
import shutil
import zipfile
import re
from datetime import datetime

from UpdateInvoiceContent import getNewInvoiceDate

# unzip the docx file in the directory argument
def extractCurrentDocx(docXFile, directoryToExtract):
    with zipfile.ZipFile(docXFile, "r") as zipDocument:
        zipDocument.extractall(directoryToExtract)

# receive the document.xml file location
# update the date component on the document
# returns the new xml content
def getNewXmlContent(docXmlFile):
    with open(docXmlFile, mode="r", encoding="utf-8") as file:
        xml_data = file.read()
        file.close()

        #Update the date tag
        #<w:date w:fullDate="2023-01-31T00:00:00Z">        
        invoiceDateTag = re.compile("<w:date w:fullDate=\"\d{4}-\d{2}-\d{2}T00:00:00Z\">").findall(xml_data)[0]
        inovoiceDateExtracted = re.search("\d{4}-\d{2}-\d{2}", invoiceDateTag).group(0)
        invoiceDate = datetime.strptime(inovoiceDateExtracted, "%Y-%m-%d")

        newInvoiceDate = getNewInvoiceDate(invoiceDate)
        newInvoiceDateTag = invoiceDateTag.replace(inovoiceDateExtracted, newInvoiceDate.strftime("%Y-%m-%d"))

        newDocXml = xml_data.replace(invoiceDateTag, newInvoiceDateTag)

        # Update the text tag
        #<w:t>January 31, 2023</w:t>
        invoiceTextTag = re.compile("<w:t>\w+ \d{2}, \d{4}</w:t>").findall(xml_data)[0]
        invoiceTextExtracted = re.search("\w+ \d{2}, \d{4}", invoiceTextTag).group(0)
        
        newInvoiceTextTag = invoiceTextTag.replace(invoiceTextExtracted, newInvoiceDate.strftime("%B %d, %Y"))

        newDocXml = newDocXml.replace(invoiceTextTag, newInvoiceTextTag)

        return newDocXml

# receive the docx file name and the docx files directory
# generate the new docx file
def createNewDocx(docXFileName, filesDir):

    directory = pathlib.Path(filesDir)

    with zipfile.ZipFile(docXFileName, mode="w") as newZipFile:
        for file_path in directory.rglob("*"):
            newZipFile.write(
                file_path,
                arcname=file_path.relative_to(directory)
            )

# main function to update the date component on the docx document
def updateDocxDate(invoiceDocxFile):
    # temporary directory to store the files from the unziped docx
    tempdir = "tempZip"

    extractCurrentDocx(invoiceDocxFile, tempdir)
    
    newDocXml = getNewXmlContent(tempdir + "//word//document.xml")

    with open(tempdir + "//word//document.xml", mode="w", encoding="utf-8") as file:
        file.write(newDocXml)
        file.close()

    createNewDocx(invoiceDocxFile, tempdir)

    shutil.rmtree(tempdir)
