import re
import calendar
import json
from collections import namedtuple
from datetime import datetime, timedelta

class InvoiceContentHelper:

    """
    Read the json file with the invoice values per person
    Returns a list with a tuple with values and the invoice total
    """
    def LoadInvoiceValues(self, invoice_values_file):
        InvoiceValue = namedtuple('InvoiceValue', ['name', 'value'])
        invoice_values = []

        with open(invoice_values_file, encoding="UTF-8") as values_file:
            values_content = values_file.read()
            names_values = json.loads(values_content)
            
            total = 0.0
            for name in names_values['base']:
                invoice_value = float(names_values['base'][name])
                if (name in names_values['bonus']):
                    invoice_value += float(names_values['bonus'][name])
                
                total += invoice_value
                invoice_values.append(InvoiceValue(name, invoice_value))

            invoice_values.append(InvoiceValue("Total", total))

        return invoice_values

    """
    Receive the invoice cell content, calculate the invoice new number
    return the same content with the new invoice number
    """
    def UpdateInvoiceNumber(self, cellText):
        currentInvoice = ""
        newInvoice = ""

        words = cellText.split()
        for word in words:
            if word.startswith("#"):
                currentInvoice = word
                
                invoiceNumber = int(word.replace("#", ""))
                newInvoiceNumber = invoiceNumber + 1
                newInvoice = "#" + str(newInvoiceNumber)

        return cellText.replace(currentInvoice, newInvoice)

    """
    Receive current invoice date and returns the next invoice day that is a work day
    """
    def GetNewInvoiceDate(self, currentInvoiceDate):
        newInvoiceDate = self.GetNewInvoiceDateForDescription(currentInvoiceDate)

        # verify if the new date is on a weekend, if yes move to the first week day
        weekDay = newInvoiceDate.isoweekday() #Monday = 1 ... Sunday = 7
        if weekDay >= 6:
            deltaDays = weekDay - 5
            newInvoiceDate = newInvoiceDate - timedelta(days=deltaDays)

        return newInvoiceDate

    """
    Receive current invoice date and returns the next invoice date
    Invoices are generated on the 15th or the last day of the month
    """
    def GetNewInvoiceDateForDescription(self, currentInvoiceDate):
        newInvoiceDate = datetime(currentInvoiceDate.year, currentInvoiceDate.month, currentInvoiceDate.day)

        # verify what is the last day of the month of the current invoice month
        lastDayOfInvoiceMonth = calendar.monthrange(currentInvoiceDate.year, currentInvoiceDate.month)[1]
        if currentInvoiceDate.day == lastDayOfInvoiceMonth:
            # is last day of the month, so add some days to jump to the next month
            nextMonthDate = currentInvoiceDate + timedelta(days=10)
            newInvoiceDate = datetime(nextMonthDate.year, nextMonthDate.month, 15)
        else:
            newInvoiceDate = datetime(currentInvoiceDate.year, currentInvoiceDate.month, lastDayOfInvoiceMonth)

        return newInvoiceDate

    """
    Receive the current description, expect the below format:
    Contractor Costs (Informatics Consultancy Services) January 15, 2023 – January 31, 2023 – Marcos Muto
    Return the description with the new dates
    """    
    def GetNewInvoiceDescription(self, currentDescription):
        description = currentDescription.replace("Contractor Costs (Informatics Consultancy Services) ", "")

        # find all description dates
        descriptionDates = re.compile("\w+ \d+, \d{4}").findall(description)
        
        # get the last date on the description and calculates the new initial and last date
        lastDescriptionDate = datetime.strptime(descriptionDates[1], "%B %d, %Y")
        newDescriptionLastDate = self.GetNewInvoiceDateForDescription(lastDescriptionDate)
        initialDay = 15 if newDescriptionLastDate.day > 15 else 1
        newDescriptionInitialDate = datetime(newDescriptionLastDate.year, newDescriptionLastDate.month, initialDay)
        
        # replace the date range text with the new dates
        newDescription = currentDescription.replace(descriptionDates[1], newDescriptionLastDate.strftime("%B %d, %Y"))
        # create the new initial date string, need to format this way to remove the day trailing zero (01)
        newInitialDate = newDescriptionInitialDate.strftime("%B") + " " + str(newDescriptionInitialDate.day) + ", " + newDescriptionInitialDate.strftime("%Y")
        newDescription = newDescription.replace(descriptionDates[0], newInitialDate)
        
        return newDescription

    """
    Extract the contractor name from the description, example below
    Contractor Costs (Informatics Consultancy Services) January 15, 2023 – January 31, 2023 – Marcos Muto
    """
    def GetContractorName(self, description):
        splited_description = description.split('–')
        return splited_description[2].strip()