from models.LinearRegression import LinearRegression
from . import AlphaVantage
import pandas as pd
import models
import json


class Stock:

    def __init__(self, symbol):
        self.symbol = symbol
        self.meta_data = None
        self.points = None

    def get_data(self, index):
        if self.meta_data is None or self.points is None:
            data = AlphaVantage.get_data(self.symbol)
            try:
                self.meta_data = data['Meta Data']
                self.points = pd.read_json(json.dumps(data['Time Series (1min)']), orient='index')
            except Exception as e:
                print(self.symbol)

        return self.meta_data if index == 0 else self.points

    def get_meta_data(self):
        return self.get_data(0)

    def get_points(self):
        return self.get_data(1)

    def predict(self, model_index=0):
        forecast_col = '1. open'
        forecast_out = 5
        test_size = 0.2

        X_train, X_test, y_train, y_test, X_lately = models.prepare_data(self.get_points(), forecast_col, forecast_out, test_size)
        model = LinearRegression()
        model.train(X_train, y_train)
        # y_pred = model.predict(X_test)
        return model.score(X_test, y_test)
