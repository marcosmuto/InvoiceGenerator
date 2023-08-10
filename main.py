import sys
import configparser

from GenerateInvoice import GenerateInvoice
from EmailSender import EmailSender
from CashFlowFileUpdater import CashFlowFileUpdater
from NFDataFileHandler import NFDataFileHandler

def main():
    args = sys.argv[1:]

    config_file = 'config_test.ini'
    if len(args) > 0:
        config_file = args[0]

    config = configparser.ConfigParser()
    if len(config.read(config_file)) == 0:
        print("Unable to read config file " + config_file)
        return 1

    print("Starting execution with config file: " + config_file)

    new_invoice_pdf_file, new_invoice_number = GenerateInvoice(config).Generate()
    EmailSender(config).SendInvoice(new_invoice_number, new_invoice_pdf_file)

    cashFlowFile = CashFlowFileUpdater(config)
    cashFlowFile.OpenSpreasheet()
    cashFlowFile.UpdateInvoiceValue()
    nf_value = cashFlowFile.UpdateExchangeRate()
    cashFlowFile.SaveAndClose()

    NFDataFileHandler(config).UpdateFile(new_invoice_number, nf_value)

    print("Completed")
    input("Press [ENTER] to finish")
    return 0

if __name__ == '__main__':
    sys.exit(main())