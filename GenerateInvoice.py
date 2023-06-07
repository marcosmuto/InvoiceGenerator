from InvoiceFiles import createNewInvoiceFile, getLastInvoiceFile
from UpdateDocxContent import updateInvoice
from UpdateDocxDateComponent import updateDocxDate

INVOICE_PATH = "C://Users//MarcosMuto//Documents//Personal//InvoiceGenerator//sample"

# create the the invoice file based on the last invoice file
lastInvoiceFile, lastInvoiceNumber = getLastInvoiceFile(INVOICE_PATH)
newInvoiceFileName, newInvoiceNumber = createNewInvoiceFile(INVOICE_PATH, lastInvoiceFile, lastInvoiceNumber)

#update the invoice content
updateInvoice(INVOICE_PATH + "//" + newInvoiceFileName)
updateDocxDate(INVOICE_PATH + "//" + newInvoiceFileName)