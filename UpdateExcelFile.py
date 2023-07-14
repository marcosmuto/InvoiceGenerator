import win32com.client
import configparser

from datetime import datetime, timedelta
from PullDollarPTAX import getExchangeRate

config = configparser.ConfigParser()
config.read_file(open("config.ini", encoding="utf8"))

SPREADSHEET_FILE = config.get('nf_data', 'spreadsheet_path')

month_on_spreadsheet = {
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

today = datetime.now()
yesterday = today - timedelta(days=1)

rate = getExchangeRate(yesterday)
print("Exchange rate: " + str(rate))

MID_MONTH_PTAX_ROW = 13
END_MONTH_PTAX_ROW = 14
PTAX_DATE_COLUMN = 10
PTAX_RATE_COLUMN = 11

MID_MONTH_NF_ROW = 5
END_MONTH_NF_ROW = 6
NF_DATE_COLUMN = 10
NF_VALUE_COLUMN = 11

CURRENT_SHEET_NAME = month_on_spreadsheet[today.strftime("%m")] + "_" + today.strftime("%Y")

excelApp = win32com.client.Dispatch("Excel.Application")
excelApp.Visible = False

print("Updating file: " + SPREADSHEET_FILE)
workBook = excelApp.Workbooks.Open(SPREADSHEET_FILE)
print("Updating sheet: " + CURRENT_SHEET_NAME)
worksheet = workBook.Sheets[CURRENT_SHEET_NAME]

nf_value = 0
# Set PTAX date and rate
if today.day <= 15:
    worksheet.Cells(MID_MONTH_PTAX_ROW, PTAX_DATE_COLUMN).Value = yesterday.strftime("%d/%b")
    worksheet.Cells(MID_MONTH_PTAX_ROW, PTAX_RATE_COLUMN).Value = rate

    worksheet.Cells(MID_MONTH_NF_ROW, NF_DATE_COLUMN).Value = today.strftime("%d/%m/%y")
    nf_value = worksheet.Cells(MID_MONTH_NF_ROW, NF_VALUE_COLUMN).Value
else:
    worksheet.Cells(END_MONTH_PTAX_ROW, PTAX_DATE_COLUMN).Value = yesterday.strftime("%d/%b")
    worksheet.Cells(END_MONTH_PTAX_ROW, PTAX_RATE_COLUMN).Value = rate

    worksheet.Cells(END_MONTH_NF_ROW, NF_DATE_COLUMN).Value = today.strftime("%d/%m/%y")
    nf_value = worksheet.Cells(END_MONTH_NF_ROW, NF_VALUE_COLUMN).Value

print("NF value: " + "%.2f" % round(nf_value, 2))

workBook.Save()
workBook.Close()
excelApp.Quit()

print("Update complete")

