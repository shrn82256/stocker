from sklearn import svm
from sklearn.metrics import precision_recall_curve

class SVR:

    def __init__(self, kernel='rbf'):
        self.model = svm.SVR(kernel=kernel, C=1e3, gamma=0.1)

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def predict(self, X_test):
        return self.model.predict(X_test)

    def score(self, X_test, y_test):
        return self.model.score(X_test, y_test)

    """
    def calc_precision_recall(self, X_test, y_test):
        y_score = self.model.decision_function(X_test)
        precision, recall, _ = precision_recall_curve(y_test, y_score)
        return precision, recall
    """
