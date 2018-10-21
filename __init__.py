import models
from mpi4py import MPI
from data import AlphaVantage, Stock
from pprint import pprint
import pandas as pd


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

NASDAQ_LIST_FILE = "db/companylist.csv"
PER_NODE_LIMIT = 100


def main():
    if rank == 0:
        # stock = AlphaVantage.AlphaVantage()
        # stock_data = stock.get_data()
        # print(len([i for i in stock_data['Time Series (1min)'] if i.startswith('2018-10-18')]))
        stocks = pd.read_csv(NASDAQ_LIST_FILE)

        print(stocks.summary_quote.head())


if __name__ == "__main__":
    main()
