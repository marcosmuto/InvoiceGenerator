import sys
import configparser
import traceback

from datetime import datetime

from GenerateInvoice import GenerateInvoice
from EmailSender import EmailSender
from CashFlowFileUpdater import CashFlowFileUpdater
from NFDataFileHandler import NFDataFileHandler

def OpenConfigFile(config_file):
    config = configparser.ConfigParser()
    config.read_file(open(config_file, "r", encoding="utf-8"))

    return config

def main():
    args = sys.argv[1:]

    config_file = 'config_test.ini'
    if len(args) > 0:
        config_file = args[0]

    try:
        config = OpenConfigFile(config_file)

        print("Starting execution with config file: " + config_file)

        new_invoice_pdf_file, new_invoice_number = GenerateInvoice(config).Generate()
        EmailSender(config).SendInvoice(new_invoice_number, new_invoice_pdf_file)

        #new_invoice_number = 252
        #currentDateTime = datetime(2023, 10, 13)
        currentDateTime = datetime.now()

        cashFlowFile = CashFlowFileUpdater(config, currentDateTime)
        try:
            cashFlowFile.OpenSpreasheet()
            cashFlowFile.UpdateInvoiceValue()
            cashFlowFile.UpdateExchangeRate()
            nf_value = cashFlowFile.GetNFValue()
            cashFlowFile.SaveAndClose()

            NFDataFileHandler(config).UpdateFile(new_invoice_number, nf_value)
        except:
            error = traceback.format_exc()
            print(error)
            print("Unable to update Excel file.")
            cashFlowFile.CloseWithoutSave()

        print("Completed")
        input("Press [ENTER] to finish")
        return 0
    
    except FileNotFoundError:
        print("Unable to read config file " + config_file)
        return 1

if __name__ == '__main__':
    sys.exit(main())