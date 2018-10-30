from keras import models, layers


class LSTM:

    def __init__(self):
        self.model = models.Sequential()

    def train(self, X_train, y_train):
        self.model.add(layers.LSTM(4, input_shape=X_train.shape))
        self.model.add(layers.Dense(1))
        self.model.compile(loss='mean_squared_error', optimizer='adam')
        self.model.fit(X_train, y_train, epochs=100, batch_size=64, verbose=2, shuffle=False)

    def predict(self, X_test):
        return self.model.predict(X_test)

    def score(self, X_test, y_test):
        return self.model.evaluate(X_test, y_test)

