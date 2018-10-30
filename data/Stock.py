from models.LinearRegression import LinearRegression
from models.ElasticNet import ElasticNet
from models.LSTM import LSTM
from models.SVR import SVR
from . import AlphaVantage
import pandas as pd
import models
import json


class Stock:

    def __init__(self, symbol, get_data_flag=False):
        self.symbol = symbol
        self.meta_data = None
        self.points = None

        if get_data_flag:
            self.get_data(0)

    def get_data(self, index):
        if self.meta_data is None or self.points is None:
            data = AlphaVantage.get_data(self.symbol)
            try:
                self.meta_data = data['Meta Data']
                self.points = pd.read_json(json.dumps(data['Time Series (1min)']), orient='index')
                # self.points.columns = ['date', 'open', 'low', 'high', 'close', 'volume']
            except Exception as e:
                print("Data retrieval failed for:", self.symbol, e)

        return self.meta_data if index == 0 else self.points

    def get_meta_data(self):
        return self.get_data(0)

    def get_points(self):
        return self.get_data(1)

    def predict(self, model_index=0):
        values = []
        for forecast_col, result_func in [('2. high', max), ('3. low', min)]:
            # forecast_col = '1. open'
            forecast_out = 5
            test_size = 0.2
            X_train, X_test, y_train, y_test, X_lately = models.prepare_data(self.get_points(), forecast_col, forecast_out,
                                                                             test_size)
            # models = [LinearRegression(), ElasticNet(), LSTM()]
            # models_list = [LinearRegression(), ElasticNet()]
            models_list = [SVR()]
            scores = []
            predictions = []

            for model in models_list:
                model.train(X_train, y_train)
                scores.append(model.score(X_test, y_test))
                y_pred = model.predict(X_lately)
                predictions.append(result_func(y_pred))
                # print(self.symbol, forecast_col, y_pred)

            fav_index = scores.index(max(scores))
            values.append((predictions[fav_index], scores[fav_index], fav_index))

        return values
