import win32com.client

class EmailSender:

    def __init__(self, config):
        self.__config = config

    def SendInvoice(self, invoiceNumber, invoiceFile):
        # Requires outlook to be installed in the local machine and opened
        outlookApp = win32com.client.Dispatch("outlook.application")

        emailItem = 0x0 #size of the new email
        newmail = outlookApp.CreateItem(emailItem)
        newmail.Subject = "Invoice {}".format(invoiceNumber)
        newmail.To = self.__config.get('email', 'email_to')
        newmail.CC = self.__config.get('email', 'email_cc')
        
        newmail.Body = "Hi Team,\r\n\r\nPlease find attached our invoice #{}.\r\n\r\nThank you,\r\nMarcos".format(invoiceNumber)

        attach=invoiceFile
        newmail.Attachments.Add(attach)

        print("Sending email to: {} cc: {}".format(newmail.To, newmail.CC))

        newmail.Send()