import unittest
from datetime import datetime

from UpdateInvoiceContent import getNewInvoiceDate, getNewInvoiceDescription, updateInvoiceNumber

class TestInvoiceFiles(unittest.TestCase):

    def testUpdateInvoiceNumber(self):
        text = "INVOICE #23"

        newText = updateInvoiceNumber(text)

        self.assertEqual(newText, "INVOICE #24")        

    def testGetNewInvoiceDate_mid_of_month(self):
        currentDateTime = datetime(2022, 10, 15)

        newCurrentDateTime = getNewInvoiceDate(currentDateTime)

        self.assertEqual(newCurrentDateTime.year, 2022)
        self.assertEqual(newCurrentDateTime.month, 10)
        self.assertEqual(newCurrentDateTime.day, 31)

    def testGetNewInvoiceDate_end_of_month(self):
        currentDateTime = datetime(2022, 10, 31)

        newCurrentDateTime = getNewInvoiceDate(currentDateTime)

        self.assertEqual(newCurrentDateTime.year, 2022)
        self.assertEqual(newCurrentDateTime.month, 11)
        self.assertEqual(newCurrentDateTime.day, 15)

    def testGetNewInvoiceDate_next_year(self):
        currentDateTime = datetime(2022, 12, 31)

        newCurrentDateTime = getNewInvoiceDate(currentDateTime)

        self.assertEqual(newCurrentDateTime.year, 2023)
        self.assertEqual(newCurrentDateTime.month, 1)
        self.assertEqual(newCurrentDateTime.day, 15)

    def testGetNewInvoiceDescription_mid_of_month(self):
        description = "Contractor Costs (Informatics Consultancy Services) October 15, 2022 – October 31, 2022 – Marcos Muto"
        newDescription = getNewInvoiceDescription(description)

        self.assertEqual(newDescription, "Contractor Costs (Informatics Consultancy Services) November 1, 2022 – November 15, 2022 – Marcos Muto")

    def testGetNewInvoiceDescription_end_of_month(self):
        description = "Contractor Costs (Informatics Consultancy Services) October 1, 2022 – October 15, 2022 – Marcos Muto"
        newDescription = getNewInvoiceDescription(description)

        self.assertEqual(newDescription, "Contractor Costs (Informatics Consultancy Services) October 15, 2022 – October 31, 2022 – Marcos Muto")