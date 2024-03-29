import requests

class BacenInterface:

    def GetExchangeRate(self, date):
        exchangeRate = 0

        formattedDate = date.strftime("%m-%d-%Y")
        print("Getting exchange rate for: " + formattedDate)

        bacen_url = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao='" + formattedDate + "'&$format=json"

        response = requests.get(bacen_url)

        if response:
            json_response = response.json()
            if len(json_response['value']) > 0:
                exchangeRate = json_response['value'][0]['cotacaoVenda']

        return exchangeRate
