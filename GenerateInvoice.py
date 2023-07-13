import os
import configparser

from InvoiceFiles import createNewInvoiceFile, getLastInvoiceFile
from UpdateDocxContent import updateInvoiceContent
from UpdateDocxDateComponent import updateDocxDate
from ConvertDocToPDF import convertDocToPDF
from EmailSender import sendInvoiceByEmail

config = configparser.ConfigParser()
config.read("config.ini")

INVOICE_PATH = config.get('invoice', 'invoice_path')

# create the invoice file based on the last invoice file
lastInvoiceFile, lastInvoiceNumber = getLastInvoiceFile(INVOICE_PATH)
newInvoiceFileName, newInvoiceNumber = createNewInvoiceFile(INVOICE_PATH, lastInvoiceFile, lastInvoiceNumber)

#update the invoice content
wordFile = INVOICE_PATH + "//" + newInvoiceFileName
updateInvoiceContent(wordFile)
updateDocxDate(wordFile)

#convert invoice docx document to pdf
if (os.path.exists(wordFile)):
    convertDocToPDF(wordFile)

pdfFile = wordFile.replace(".docx", ".pdf")

sendInvoiceByEmail(newInvoiceNumber, pdfFile)