import models
from data import AlphaVantage


def main():
    stock = AlphaVantage.AlphaVantage()
    print(stock.get_data())


if __name__ == "__main__":
    main()
