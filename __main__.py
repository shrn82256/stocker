from mpi4py import MPI
from data.Stock import Stock
from pathlib import Path
from pprint import pprint
from statistics import mean
import json
import pickle
import socket
import pandas as pd
from flask import Flask


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# NASDAQ_LIST_FILE = "/mnt/d/Projects/stocker/db/companylist.csv"
# NASDAQ_LIST_FILE = "http://www.asisodia.com/datasets/companylist.csv"
NASDAQ_LIST_FILE = Path("stocker/db/companylist.csv")
PER_NODE_LIMIT = 2
STOCK_BUFFER = PER_NODE_LIMIT * 3 // 2
# TOTAL_NODES = int(MPI.INFO_ENV.get("soft"))
TOTAL_NODES = comm.Get_size()
API_KEYS = ["GUPPO7FAKF3SENRJ", "066F5B6VQS6TH2N0", "9BTNEH3XG5J4S7KW"]
KEY_IDX = 0

app = Flask(__name__)
@app.route("/")
def main():
    print("hit1")
    if rank == 0:
        stocks = pd.read_csv(NASDAQ_LIST_FILE, engine='python').sample(frac=1)

        for i in range(1, TOTAL_NODES):
            comm.send(stocks[(i-1)*STOCK_BUFFER: i*STOCK_BUFFER], dest=i)

        result = {}
        best_stock = None
        best_stock_profit = -1
        best_stock_score = None
        for i in range(1, TOTAL_NODES):
            temp_result = comm.recv(source=i)
            if not temp_result:
                continue
            else:
                result[i] = temp_result
            if result[i]["diff"] > best_stock_profit:
                best_stock = result[i]["best_stock"]
                best_stock_profit = result[i]["diff"]
                best_stock_score = result[i]["score"]

        result[0] = {
            "name": socket.gethostname(),
            "best_stock": best_stock,
            # "best_stock_info": ,
            "diff": best_stock_profit,
            "best_stock_score": best_stock_score
        }
        
        # print("P", rank, best_stock, best_stock_profit)
        # pprint(result)
        return json.dumps(result)


def work():
    print("hit2")
    global KEY_IDX
    if rank != 0:
        # pickle_off = open("db/%s.pickle" % rank, "rb")
        # stocks = pickle.load(pickle_off)
        key_idx = KEY_IDX
        stocks = []
        predictions = []
        highest_diff = 0
        highest_diff_stock = None
        highest_diff_score = None
        for stock_symbol in comm.recv(source=0).symbol:
            stock = Stock(stock_symbol, API_KEYS[key_idx], True)
            key_idx = (key_idx + 1) % len(API_KEYS)
            # if stock.points is None:
            #     continue
            try:
                prediction = stock.predict()
                # print(rank, stock.symbol, prediction)
                diff = prediction[0][0] - prediction[1][0]
                if highest_diff < diff:
                    highest_diff = diff
                    highest_diff_stock = stock
                    highest_diff_score = (prediction[0][1], prediction[1][1])

                stocks.append(stock)
            except Exception as e:
                continue

            if len(stocks) == PER_NODE_LIMIT:
                break

        KEY_IDX = key_idx
        """
        pickling_on = open("db/%s.pickle" % rank, "wb")
        pickle.dump(stocks, pickling_on)
        pickling_on.close()
        # for i in range(PER_NODE_LIMIT):
            # stock = stocks[i]
            # try:
            # print(stock.points.head())
            # predictions.append(mean(prediction))
            # except Exception as e:
            #     print(rank, stock.symbol, e)
            #     print(stock.points.head())
        """
        if highest_diff_stock is not None:
            result = {
                "name": socket.gethostname(),
                "stocks": [stock.symbol for stock in stocks],
                "best_stock": highest_diff_stock.symbol,
                "diff": diff,
                "score": highest_diff_score
            }
            # print("P", rank, socket.gethostname(), , highest_diff_stock.symbol, diff, highest_diff_score)
            comm.send(result, dest=0)
        else:
            comm.send(False, dest=0)
        work()

        # print(rank, len(stocks), mean(predictions), len(predictions))
        # print(stocks[0].get_points().head())


if __name__ == "__main__":
    if rank == 0:
        app.run()
    else:
        work()
#     main()
