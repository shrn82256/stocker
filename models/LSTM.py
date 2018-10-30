from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM


class LSTM:

    def __init__(self):
        self.model = Sequential()
        self.model.add(LSTM(4, input_shape=(1, look_back)))
        self.model.add(Dense(1))
        self.model.compile(loss='mean_squared_error', optimizer='adam')

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train, epochs=100, batch_size=1, verbose=2)

    def predict(self, X_test):
        return self.model.predict(X_test)

    def score(self, X_test, y_test):
        return self.model.evaluate(X_test, y_test)

