import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn import preprocessing
from sklearn import model_selection


def prepare_data(df, forecast_col, forecast_out, test_size):
    scaler = preprocessing.MinMaxScaler(feature_range=(0, 1))
    df = scaler.fit_transform(df)

    label = df[forecast_col].shift(-forecast_out)
    X = np.array(df[[forecast_col]])
    X = preprocessing.scale(X)
    X_lately = X[-forecast_out:]
    X = X[:-forecast_out]
    label.dropna(inplace=True)
    y = np.array(label)
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=test_size)

    response = [X_train, X_test, y_train, y_test, X_lately]
    return response


def calc_accuracy(y_true, y_pred):
    return metrics.accuracy_score(y_true, y_pred)
