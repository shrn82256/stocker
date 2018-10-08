import requests


class AlphaVantage:

    def __init__(self):
        # data = self.data

        self.function_name = "TIME_SERIES_INTRADAY"
        self.symbol = "MSFT"
        self.interval = "1min"
        self.apikey = "GUPPO7FAKF3SENRJ"
        self.apiurl = "https://www.alphavantage.co/query?"

    def get_data(self):
        url = "https://www.alphavantage.co/query?function=%s&symbol=%s&interval=%s&apikey=%s" \
              % (self.function_name, self.symbol, self.interval, self.apikey)
        return url
