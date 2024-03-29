import unittest
from datetime import datetime

from InvoiceContentHelper import InvoiceContentHelper

class TestInvoiceFiles(unittest.TestCase):

    invoiceContentHelper = InvoiceContentHelper()

    def testUpdateInvoiceNumber(self):
        text = "INVOICE #23"

        newText = self.invoiceContentHelper.UpdateInvoiceNumber(text)

        self.assertEqual(newText, "INVOICE #24")        

    def testGetNewInvoiceDate_end_of_month(self):
        currentDateTime = datetime(2022, 8, 31)

        newCurrentDateTime = self.invoiceContentHelper.GetNewInvoiceDate(currentDateTime)

        self.assertEqual(newCurrentDateTime.year, 2022)
        self.assertEqual(newCurrentDateTime.month, 9)
        self.assertEqual(newCurrentDateTime.day, 15)

    def testGetNewInvoiceDate_mid_of_month(self):
        currentDateTime = datetime(2022, 9, 15)

        newCurrentDateTime = self.invoiceContentHelper.GetNewInvoiceDate(currentDateTime)

        self.assertEqual(newCurrentDateTime.year, 2022)
        self.assertEqual(newCurrentDateTime.month, 9)
        self.assertEqual(newCurrentDateTime.day, 30)

    def testGetNewInvoiceDate_next_on_saturday(self):
        currentDateTime = datetime(2023, 3, 31)

        newCurrentDateTime = self.invoiceContentHelper.GetNewInvoiceDate(currentDateTime)

        self.assertEqual(newCurrentDateTime.year, 2023)
        self.assertEqual(newCurrentDateTime.month, 4)
        self.assertEqual(newCurrentDateTime.day, 14)

    def testGetNewInvoiceDate_next_on_sunday(self):
        currentDateTime = datetime(2023, 4, 15)

        newCurrentDateTime = self.invoiceContentHelper.GetNewInvoiceDate(currentDateTime)

        self.assertEqual(newCurrentDateTime.year, 2023)
        self.assertEqual(newCurrentDateTime.month, 4)
        self.assertEqual(newCurrentDateTime.day, 28)

    def testGetNewInvoiceDate_next_year(self):
        currentDateTime = datetime(2022, 12, 31)

        newCurrentDateTime = self.invoiceContentHelper.GetNewInvoiceDate(currentDateTime)

        self.assertEqual(newCurrentDateTime.year, 2023)
        self.assertEqual(newCurrentDateTime.month, 1)
        self.assertEqual(newCurrentDateTime.day, 13)

    def testGetNewInvoiceDate_last_day_on_weekend(self):
        currentDateTime = datetime(2023, 9, 29)

        newCurrentDateTime = self.invoiceContentHelper.GetNewInvoiceDate(currentDateTime)

        self.assertEqual(newCurrentDateTime.year, 2023)
        self.assertEqual(newCurrentDateTime.month, 10)
        self.assertEqual(newCurrentDateTime.day, 13)

    def testGetNewInvoiceDescription_mid_of_month(self):
        description = "Contractor Costs (Informatics Consultancy Services) October 15, 2022 – October 31, 2022 – Marcos Muto"
        newDescription = self.invoiceContentHelper.GetNewInvoiceDescription(description)

        self.assertEqual(newDescription, "Contractor Costs (Informatics Consultancy Services) November 1, 2022 – November 15, 2022 – Marcos Muto")

    def testGetNewInvoiceDescription_end_of_month(self):
        description = "Contractor Costs (Informatics Consultancy Services) October 1, 2022 – October 15, 2022 – Marcos Muto"
        newDescription = self.invoiceContentHelper.GetNewInvoiceDescription(description)

        self.assertEqual(newDescription, "Contractor Costs (Informatics Consultancy Services) October 15, 2022 – October 31, 2022 – Marcos Muto")

    def testGetNewInvoiceDescription_mid_of_month_on_weekend(self):
        description = "Contractor Costs (Informatics Consultancy Services) March 15, 2023 – March 31, 2023 – Marcos Muto"
        newDescription = self.invoiceContentHelper.GetNewInvoiceDescription(description)

        self.assertEqual(newDescription, "Contractor Costs (Informatics Consultancy Services) April 1, 2023 – April 15, 2023 – Marcos Muto")

    def testGetNewInvoiceDescription_end_of_month_on_weekend(self):
        description = "Contractor Costs (Informatics Consultancy Services) April 1, 2023 – April 15, 2023 – Marcos Muto"
        newDescription = self.invoiceContentHelper.GetNewInvoiceDescription(description)

        self.assertEqual(newDescription, "Contractor Costs (Informatics Consultancy Services) April 15, 2023 – April 30, 2023 – Marcos Muto")

    def testGetContractorName(self):
        description = "Contractor Costs (Informatics Consultancy Services) April 1, 2023 – April 15, 2023 – Marcos Muto"
        name = self.invoiceContentHelper.GetContractorName(description)

        self.assertEqual(name, "Marcos Muto")
    