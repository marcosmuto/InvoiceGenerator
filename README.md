# Introduction

- Generate a new invoice file based on a previous one.
- Fill out the values and dates of the invoice based on the previous invoice data.
- Convert the invoice to PDF and send via email.
- Update the cash flow update
    - Update invoice values
    - Pull exchange rate and calculate the NF (Nota Fiscal) value
- Update the data of the browser extension that automatically fills out the NF-e data

# Usage

`py main.py [config_file]`

If config file is not present, try to use the file config_test.ini

Example:

`py main.py config.ini`

# Requirements

Modules are described on `install_dependencies.sh` file

**IMPORTANT** Microsoft Excel and Outlook are required to update the cash flow file and send email. Scripts uses the win32com lib to manipulate the MS apps.

