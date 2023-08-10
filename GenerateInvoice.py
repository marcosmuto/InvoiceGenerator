from InvoiceFileHandler import InvoiceFileHandler
from InvoiceContentUpdate import InvoiceContentUpdate
from UpdateDocxDateComponent import UpdateDateComponent

class GenerateInvoice:

    def __init__(self, config):
        self.config = config

    def Generate(self):
        INVOICE_PATH = self.config.get('invoice', 'invoice_path')
        INVOICE_VALUE_FILE = self.config.get('invoice', 'values_file')

        # create the invoice file based on the last invoice file
        invoiceHandler = InvoiceFileHandler(INVOICE_PATH)
        invoiceHandler.CreateNewInvoiceFile()
        
        #update the invoice content
        wordFile = INVOICE_PATH + "//" + invoiceHandler.GetNewInvoiceFile()
        InvoiceContentUpdate(wordFile, INVOICE_VALUE_FILE).UpdateInvoiceContent()
        UpdateDateComponent(wordFile).UpdateDocxDate()

        #convert invoice docx document to pdf
        invoiceHandler.ConvertDocToPDF(wordFile)
        pdfFile = wordFile.replace(".docx", ".pdf")
        print("PDF version generated: " + pdfFile)

        return pdfFile, invoiceHandler.GetNewInvoiceNumber()