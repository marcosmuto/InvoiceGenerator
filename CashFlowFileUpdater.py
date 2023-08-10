import win32com.client
import re

from datetime import datetime, timedelta

from InvoiceContentHelper import InvoiceContentHelper
from BacenInterface import BacenInterface

MONTH_MAP = {
    "01": "Jan",
    "02": "Fev",
    "03": "Mar",
    "04": "Abr",
    "05": "Mai",
    "06": "Jun",
    "07": "Jul",
    "08": "Ago",
    "09": "Set",
    "10": "Out",
    "11": "Nov",
    "12": "Dez"
}

"""
Constants with the position of the data in the spreadsheet
"""
MID_MONTH_PTAX_ROW = 13
END_MONTH_PTAX_ROW = 14
PTAX_DATE_COLUMN = 10
PTAX_RATE_COLUMN = 11

MID_MONTH_NF_ROW = 5
END_MONTH_NF_ROW = 6
NF_DATE_COLUMN = 10
NF_VALUE_COLUMN = 11

MID_MONTH_INVOICE_COLUMN = 16
END_MONTH_INVOICE_COLUMN = 17
INVOICE_NAMES_COLUMN = 13
INVOICE_TOTAL_ROW = 6

class CashFlowFileUpdater:

    def __init__(self, config):
        self.__config = config
        self.SPREADSHEET_FILE = config.get('nf_data', 'spreadsheet_path')
        self.today = datetime.now()

    def OpenSpreasheet(self):
        CURRENT_SHEET_NAME = MONTH_MAP[self.today.strftime("%m")] + "_" + self.today.strftime("%Y")

        self.excelApp = win32com.client.Dispatch("Excel.Application")
        self.excelApp.Visible = False

        print("Updating file: " + self.SPREADSHEET_FILE)
        self.workBook = self.excelApp.Workbooks.Open(self.SPREADSHEET_FILE)
        print("Updating sheet: " + CURRENT_SHEET_NAME)
        self.worksheet = self.workBook.Sheets[CURRENT_SHEET_NAME]

    def SaveAndClose(self):
        self.workBook.Save()
        self.workBook.Close()
        self.excelApp.Quit()

    def UpdateInvoiceValue(self):
        invoice_values = InvoiceContentHelper().LoadInvoiceValues(self.__config.get('invoice', 'values_file'))

        INVOICE_COLUMN = END_MONTH_INVOICE_COLUMN
        if self.today.day <= 15:
            INVOICE_COLUMN = MID_MONTH_INVOICE_COLUMN
        
        for invoice_name in invoice_values:
            if invoice_name == "Total":
                self.worksheet.Cells(INVOICE_TOTAL_ROW, INVOICE_COLUMN).Value = invoice_values[invoice_name].value
                print("Updating total with new value {}".format(invoice_values[invoice_name].value))
            else:
                current_formula = self.worksheet.Cells(invoice_values[invoice_name].position, INVOICE_COLUMN).Formula
                new_formula = re.sub("\d+\.\d+", str(invoice_values[invoice_name].value), current_formula)
                self.worksheet.Cells(invoice_values[invoice_name].position, INVOICE_COLUMN).Formula = new_formula
                print("Updating formula for {:>25} new formula: {}".format(invoice_name, new_formula))
        
        print("Invoice values updated")

    def UpdateExchangeRate(self):
        rate_value = 0
        pull_rate_tries = 0
        rate_date = self.today
        # exchange rates are not computed during the weekend or holidays
        # so it tries to pull from yesterday to 7 days earlier until finds a value
        # if today is Monday, tries Sunday, Saturday and Friday, if Friday was a holiday, try ealier until a workday.
        while (rate_value == 0 and pull_rate_tries < 7):
            rate_date = rate_date - timedelta(days=1)
            rate_value = BacenInterface().GetExchangeRate(rate_date)
            pull_rate_tries += 1

        print("Exchange rate: {} on date: {}".format(rate_value, rate_date.strftime("%d/%m/%y")))

        nf_value = 0
        # Set PTAX date and rate
        if self.today.day <= 15:
            self.worksheet.Cells(MID_MONTH_PTAX_ROW, PTAX_DATE_COLUMN).Value = rate_date.strftime("%d/%b")
            self.worksheet.Cells(MID_MONTH_PTAX_ROW, PTAX_RATE_COLUMN).Value = rate_value

            self.worksheet.Cells(MID_MONTH_NF_ROW, NF_DATE_COLUMN).Value = self.today.strftime("%d/%m/%y")
            nf_value = self.worksheet.Cells(MID_MONTH_NF_ROW, NF_VALUE_COLUMN).Value
        else:
            self.worksheet.Cells(END_MONTH_PTAX_ROW, PTAX_DATE_COLUMN).Value = rate_date.strftime("%d/%b")
            self.worksheet.Cells(END_MONTH_PTAX_ROW, PTAX_RATE_COLUMN).Value = rate_value

            self.worksheet.Cells(END_MONTH_NF_ROW, NF_DATE_COLUMN).Value = self.today.strftime("%d/%m/%y")
            nf_value = self.worksheet.Cells(END_MONTH_NF_ROW, NF_VALUE_COLUMN).Value

        print("NF value: {:.2f}".format(nf_value))
        print("Exchange rate update complete")

        return round(nf_value, 2)

