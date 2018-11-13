import requests


_symbol = "MSFT"


def get_data(symbol):
    if symbol is None:
        symbol = _symbol

    url = "https://api.iextrading.com/1.0/stock/%s/chart/5y" % symbol

    # print(symbol, url)
    return requests.get(url).json()
