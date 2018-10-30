import requests


_function_name = "TIME_SERIES_INTRADAY"
_symbol = "MSFT"
_interval = "1min"
_apikey = "GUPPO7FAKF3SENRJ"
_apiurl = "https://www.alphavantage.co/query?"
_outputsize = "full"


def get_data(symbol):
    if symbol is None:
        symbol = _symbol

    url = "https://www.alphavantage.co/query?function=%s&symbol=%s&interval=%s&apikey=%s&outputsize=%s" \
          % (_function_name, symbol, _interval, _apikey, _outputsize)

    return requests.get(url).json()
