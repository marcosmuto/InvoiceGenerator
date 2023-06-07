import os
import re
import shutil

# Receive the file path returns:
# 1 - The latest invoice file name
# 2 - The latest invoice #, 0 if there is no file
def getLastInvoiceFile(invoicePath):
    files = os.listdir(invoicePath)
    lastInvoice = None
    lastInvoiceNumber = 0

    # pull only docx files
    docxFiles = [docx for docx in files if docx.endswith("docx")]
    if len(docxFiles) > 0:
        docxFiles.sort(key = lambda docName: int(re.search("\d+", docName).group(0)))
        docxFiles.reverse()
        lastInvoice = docxFiles[0]
        
    # get the last invoice number
    if lastInvoice is not None:
        lastInvoiceNumberList = re.compile("\d+").findall(lastInvoice)    
        lastInvoiceNumber = int(lastInvoiceNumberList[0])

    return lastInvoice, lastInvoiceNumber
    
# Receive the file path, last invoice file name and last invoice #
# Create the new invoice file by copying the last and returns:
# 1 - The new invoice file name
# 2 - The new invoice #
def createNewInvoiceFile(invoicePath, lastInvoice, lastInvoiceNumber):
    
    # new invoice number
    newInvoiceNumber = lastInvoiceNumber + 1
    newInvoiceFileName = lastInvoice.replace(str(lastInvoiceNumber), str(newInvoiceNumber))
    
    # create new file
    shutil.copy(invoicePath + "//" + lastInvoice, invoicePath + "//" + newInvoiceFileName)

    return newInvoiceFileName, newInvoiceNumber
