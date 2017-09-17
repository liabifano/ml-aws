from sklearn import datasets
from sklearn import svm
from sklearn.externals import joblib

from modelapp import config

def train():

    iris = datasets.load_iris()
    X, y = iris.data, iris.target
    clf = svm.SVC(gamma=0.01, C=100.)
    clf.fit(X, y)
    joblib.dump(clf, config.MODEL_PATH, compress=9)

    print('The model is saved in: {}'.format(config.MODEL_PATH))


if __name__ == '__main__':
    train()