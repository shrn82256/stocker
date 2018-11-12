import requests


_function_name = "TIME_SERIES_INTRADAY"
_symbol = "MSFT"
_interval = "1min"
_apikey = "GUPPO7FAKF3SENRJ"
_apiurl = "https://www.alphavantage.co/query?"
_outputsize = "full"


def get_data(symbol, apikey):
    if symbol is None:
        symbol = _symbol
    if apikey is None:
        apikey = _apikey

    url = "%sfunction=%s&symbol=%s&interval=%s&apikey=%s&outputsize=%s" \
          % (_apiurl, _function_name, symbol, _interval, apikey, _outputsize)
    # print(symbol, url)
    return requests.get(url).json()
