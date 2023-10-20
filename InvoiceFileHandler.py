import os
import re
import shutil
from docx2pdf import convert

class InvoiceFileHandler:

    def __init__(self, invoice_path):
        self.__invoice_path = invoice_path
        self.__last_invoice_file_name = None
        self.__last_invoice_number = 0
        self.__VerifyLatestInvoice()
        self.__new_invoice_file_name = None
        self.__new_invoice_number = 0

    def GetLastInvoiceNumber(self):
        return self.__last_invoice_number
    
    def GetLastInvoiceFile(self):
        return self.__last_invoice_file_name
    
    def GetNewInvoiceNumber(self):
        return self.__new_invoice_number
    
    def GetNewInvoiceFile(self):
        return self.__new_invoice_file_name
    
    # Get the latest invoice file name
    def __VerifyLatestInvoice(self):
        files = os.listdir(self.__invoice_path)
        
        # pull only docx files
        docxFiles = [docx for docx in files if docx.endswith("docx")]
        if len(docxFiles) > 0:
            docxFiles.sort(key = lambda docName: int(re.search("\d+", docName).group(0)))
            docxFiles.reverse()
            self.__last_invoice_file_name = docxFiles[0]
            
        # get the last invoice number
        if self.__last_invoice_file_name is not None:
            lastInvoiceNumberList = re.compile("\d+").findall(self.__last_invoice_file_name)    
            self.__last_invoice_number = int(lastInvoiceNumberList[0])
            print("Last invoice found: " + self.__last_invoice_file_name)
        else:
            print("Last invoice not found")
    
    # Create the new invoice file by copying the lastest file    
    def CreateNewInvoiceFile(self):
        invoicePath = self.__invoice_path
        
        # new invoice number
        newInvoiceNumber = self.__last_invoice_number + 1
        newInvoiceFileName = self.__last_invoice_file_name.replace(str(self.__last_invoice_number), str(newInvoiceNumber))
        
        # create new file
        shutil.copy(invoicePath + "//" + self.__last_invoice_file_name, invoicePath + "//" + newInvoiceFileName)

        print("New invoice file created: " + newInvoiceFileName)

        self.__new_invoice_file_name = newInvoiceFileName
        self.__new_invoice_number = newInvoiceNumber

    def ConvertDocToPDF(self, docFile):
        convert(docFile)
