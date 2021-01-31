import requests
from pprint import pprint
from datetime import datetime


class CurrencyExchangeRates:
    def __init__(self):
        self.EXCHANGE_RATES_API_URL = "https://api.exchangeratesapi.io/latest"
        self.EXCHANGE_RATES_API_URL2 = "https://api.exchangeratesapi.io/history?symbols=USD,GBP"

    def download_exchange_data(self):
        """
        This is a method that download exchange rates from different
        :return:
        """

        start_date = datetime.now().date().replace(year=2020,month=12, day=1)
        end_date = datetime.now().date().replace(month=2, day=28)
        print(start_date, end_date)

        # 2021-01-01
        batch_dates = "&start_at=%s&end_at=%s" % (start_date, end_date)
        data = requests.get(self.EXCHANGE_RATES_API_URL2 + batch_dates)
        pprint(data.json())
