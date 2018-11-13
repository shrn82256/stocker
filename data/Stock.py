from models.LinearRegression import LinearRegression
from models.ElasticNet import ElasticNet
# from models.LSTM import LSTM
from models.SVR import SVR
from . import IEX
import pandas as pd
import models
import json


class Stock:

    def __init__(self, symbol, api_key, get_data_flag=False):
        self.symbol = symbol
        self.api_key = api_key
        self.points = None

        if get_data_flag:
            self.get_points()

    def get_points(self):
        if self.points is None:
            data = IEX.get_data(self.symbol)
            try:
                self.points = pd.read_json(json.dumps(data)).drop('label', axis=1).drop('date', axis=1)
                # self.points.columns = ['date', 'open', 'low', 'high', 'close', 'volume']
            except Exception as e:
                print("Data retrieval failed for:", self.symbol, ":", e, ":", self.api_key, list(data))
                return None

        return self.points

    def predict(self, model_index=0):
        values = []
        for forecast_col, result_func in [('high', max), ('low', min)]:
            # forecast_col = '1. open'
            forecast_out = 10
            test_size = 0.2
            X_train, X_test, y_train, y_test, X_lately = models.prepare_data(self.get_points(), forecast_col, forecast_out,
                                                                             test_size)
            # models = [LinearRegression(), ElasticNet(), LSTM()]
            models_list = [LinearRegression(), ElasticNet(), SVR()]
            # models_list = [SVR()]
            scores = []
            predictions = []
            # precision_recall_list = []

            for model in models_list:
                model.train(X_train, y_train)
                scores.append(model.score(X_test, y_test))
                y_pred = model.predict(X_lately)
                predictions.append(result_func(y_pred))
                # precision_recall_list.append(model.calc_precision_recall(X_test, y_test))
                # print(self.symbol, forecast_col, y_pred)

            fav_index = scores.index(max(scores))
            values.append((predictions[fav_index], scores[fav_index], fav_index))

        return values
