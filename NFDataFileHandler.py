import json
import re

class NFDataFileHandler():

    def __init__(self, config):
        self.NF_DATA_FILE = config.get('nf_data', 'extension_file')

    def UpdateFile(self, invoice_number, value):
        print("Updating NF data file")

        nf_data = None

        with open(self.NF_DATA_FILE, encoding="UTF-8") as nf_file:
            file_content = nf_file.read()
            nf_data = json.loads(file_content)

        description = nf_data["discriminacao"]
        nf_data["discriminacao"] = re.sub("\d+", str(invoice_number), description)
        nf_data["valor"] = "{:.2f}".format(value)

        with open(self.NF_DATA_FILE, mode="w+t", encoding="UTF-8") as nf_file:
            json.dump(nf_data, fp=nf_file, ensure_ascii=False, indent=4)

        print("New NF data:")
        print(nf_data)
        