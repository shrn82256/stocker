from mpi4py import MPI
from data.Stock import Stock
from pprint import pprint
import pandas as pd


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

NASDAQ_LIST_FILE = "db/companylist.csv"
PER_NODE_LIMIT = 10
# TOTAL_NODES = MPI.INFO_ENV.get("soft")
TOTAL_NODES = int(MPI.INFO_ENV.get("maxprocs"))


def main():
    if rank == 0:
        stocks = pd.read_csv(NASDAQ_LIST_FILE)

        for i in range(1, TOTAL_NODES):
            comm.send(stocks[(i-1)*PER_NODE_LIMIT: i*PER_NODE_LIMIT], dest=i)
    else:
        stocks = [Stock(stock) for stock in comm.recv(source=0).symbol]
        print(rank, len(stocks), stocks[0].predict())
        # print(stocks[0].get_points().head())


if __name__ == "__main__":
    main()
