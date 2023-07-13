import re
import calendar
from datetime import datetime, timedelta

# Receive the invoice cell content, calculate the invoice new number
# return the same content with the new invoice number
def updateInvoiceNumber(cellText):
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

# Receive current invoice date and return the next invoice date
def getNewInvoiceDate(currentInvoiceDate):
    newInvoiceDate = getNewInvoiceDateForDescription(currentInvoiceDate)

    # verify if the new date is on a weekend, if yes move the first week day
    weekDay = newInvoiceDate.isoweekday() #Monday = 1 ... Sunday = 7
    if weekDay >= 6:
        deltaDays = weekDay - 5
        newInvoiceDate = newInvoiceDate - timedelta(days=deltaDays)

    return newInvoiceDate

def getNewInvoiceDateForDescription(currentInvoiceDate):
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

# Receive the current description, expect the below format:
# Contractor Costs (Informatics Consultancy Services) January 15, 2023 – January 31, 2023 – Marcos Muto
# Return the description with the new dates
def getNewInvoiceDescription(currentDescription):
    description = currentDescription.replace("Contractor Costs (Informatics Consultancy Services) ", "")

    # find all description dates
    descriptionDates = re.compile("\w+ \d+, \d{4}").findall(description)
    
    # get the last date on the description and calculates the new initial and last date
    lastDescriptionDate = datetime.strptime(descriptionDates[1], "%B %d, %Y")
    newDescriptionLastDate = getNewInvoiceDateForDescription(lastDescriptionDate)
    initialDay = 15 if newDescriptionLastDate.day > 15 else 1
    newDescriptionInitialDate = datetime(newDescriptionLastDate.year, newDescriptionLastDate.month, initialDay)
    
    # replace the date range text with the new dates
    newDescription = currentDescription.replace(descriptionDates[1], newDescriptionLastDate.strftime("%B %d, %Y"))
    # create the new initial date string, need to format this way to remove the day trailing zero (01)
    newInitialDate = newDescriptionInitialDate.strftime("%B") + " " + str(newDescriptionInitialDate.day) + ", " + newDescriptionInitialDate.strftime("%Y")
    newDescription = newDescription.replace(descriptionDates[0], newInitialDate)
    
    return newDescription

