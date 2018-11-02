from mpi4py import MPI
from data.Stock import Stock
from pprint import pprint
from statistics import mean
import pickle
import socket
import pandas as pd


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# NASDAQ_LIST_FILE = "/mnt/d/Projects/stocker/db/companylist.csv"
NASDAQ_LIST_FILE = "http://www.asisodia.com/datasets/companylist.csv"
# NASDAQ_LIST_FILE = "db/companylist.csv"
PER_NODE_LIMIT = 2
# TOTAL_NODES = int(MPI.INFO_ENV.get("soft"))
TOTAL_NODES = comm.Get_size()


def main():
    if rank == 0:
        stocks = pd.read_csv(NASDAQ_LIST_FILE).sample(frac=1)
        
        for i in range(1, TOTAL_NODES):
            comm.send(stocks[(i-1)*PER_NODE_LIMIT: i*PER_NODE_LIMIT], dest=i)
        
        best_stock = None
        best_stock_profit = -1
        for i in range(1, TOTAL_NODES):
            stock = comm.recv(source=i)
            if stock[1] > best_stock_profit:
                best_stock = stock[0]
                best_stock_profit = stock[1]
        
        print("P", rank, best_stock, best_stock_profit)
    else:
        # pickle_off = open("db/%s.pickle" % rank, "rb")
        # stocks = pickle.load(pickle_off)
        stocks = [Stock(stock, True) for stock in comm.recv(source=0).symbol]
        # pickling_on = open("db/%s.pickle" % rank, "wb")
        # pickle.dump(stocks, pickling_on)
        # pickling_on.close()
        predictions = []
        highest_diff = 0
        highest_diff_stock = stocks[highest_diff]
        for i in range(PER_NODE_LIMIT):
            stock = stocks[i]
            # try:
            # print(stock.points.head())
            prediction = stock.predict()
            # print(rank, stock.symbol, prediction)
            diff = prediction[0][0]-prediction[1][0]
            if highest_diff < diff:
                highest_diff = diff
                highest_diff_stock = stock
            # predictions.append(mean(prediction))
            # except Exception as e:
            #     print(rank, stock.symbol, e)
            #     print(stock.points.head())
        print("P", rank, socket.gethostname(), [stock.symbol for stock in stocks], highest_diff_stock.symbol, diff)
        comm.send([highest_diff_stock.symbol, diff], dest=0)

        # print(rank, len(stocks), mean(predictions), len(predictions))
        # print(stocks[0].get_points().head())


if __name__ == "__main__":
    main()
