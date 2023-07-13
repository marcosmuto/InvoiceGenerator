import win32com.client
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

def sendInvoiceByEmail(invoiceNumber, invoiceFile):
    # Requires outlook to be installed in the local machine and opened
    outlookApp = win32com.client.Dispatch("outlook.application")

    emailItem = 0x0 #size of the new email
    newmail = outlookApp.CreateItem(emailItem)
    newmail.Subject = 'Invoice ' + str(invoiceNumber)
    newmail.To = config.get('email', 'email_to')
    newmail.CC = config.get('email', 'email_cc')
    
    newmail.Body = 'Hi Team,\r\n\r\nPlease find attached our invoice #' + str(invoiceNumber) + '.\r\n\r\nThank you,\r\nMarcos'

    attach=invoiceFile
    newmail.Attachments.Add(attach)

    newmail.Send()