import unittest
import os

from InvoiceFiles import createNewInvoiceFile, getLastInvoiceFile

class TestInvoiceFiles(unittest.TestCase):

    TEST_FILE_PATH = "tests"

    def testGetLastInvoiceFile_no_file_on_folder(self):
        #no test setup

        invoiceFile, invoiceNumber = getLastInvoiceFile(self.TEST_FILE_PATH)

        self.assertEqual(invoiceFile, None)
        self.assertEqual(invoiceNumber, 0)

    def testGetLastInvoiceFile_one_file_on_folder(self):
        #test setup
        testInvoiceNumber = 10
        testInvoiceName = "invoice " + str(testInvoiceNumber) + ".docx"
        f = open(self.TEST_FILE_PATH + "//" + testInvoiceName, "x")
        f.close()

        invoiceFile, invoiceNumber = getLastInvoiceFile(self.TEST_FILE_PATH)
        self.assertEqual(invoiceFile, testInvoiceName)
        self.assertEqual(invoiceNumber, testInvoiceNumber)

        #after test setup
        os.remove(self.TEST_FILE_PATH + "//" + testInvoiceName)


    def testGetLastInvoiceFile_three_files_on_folder(self):
        #test setup
        f = open(self.TEST_FILE_PATH + "//" + "invoice 9.docx", "x")
        f.close()
        testInvoiceNumber = 10
        testInvoiceName = "invoice " + str(testInvoiceNumber) + ".docx"
        f = open(self.TEST_FILE_PATH + "//" + testInvoiceName, "x")
        f.close()

        invoiceFile, invoiceNumber = getLastInvoiceFile(self.TEST_FILE_PATH)
        self.assertEqual(invoiceFile, testInvoiceName)
        self.assertEqual(invoiceNumber, testInvoiceNumber)

        #after test setup
        os.remove(self.TEST_FILE_PATH + "//" + testInvoiceName)
        os.remove(self.TEST_FILE_PATH + "//" + "invoice 9.docx")

    def testCreateNewInvoiceFile(self):
        #test setup
        testInvoiceNumber = 10
        testInvoiceName = "invoice " + str(testInvoiceNumber) + ".docx"
        f = open(self.TEST_FILE_PATH + "//" + testInvoiceName, "x")
        f.close()

        newInvoiceFile, newInvoiceNumber = createNewInvoiceFile(self.TEST_FILE_PATH, testInvoiceName, testInvoiceNumber)
        
        self.assertEqual(newInvoiceFile, "invoice " + str(testInvoiceNumber + 1) + ".docx")
        self.assertEqual(newInvoiceNumber, testInvoiceNumber + 1)
        self.assertTrue(os.path.isfile(self.TEST_FILE_PATH + "//" + newInvoiceFile))

        #after test setup
        os.remove(self.TEST_FILE_PATH + "//" + testInvoiceName)
        os.remove(self.TEST_FILE_PATH + "//" + newInvoiceFile)