import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.naive_bayes import BernoulliNB, GaussianNB
from sklearn.svm import LinearSVC, NuSVC, NuSVR
from sklearn.metrics import accuracy_score, recall_score, f1_score, roc_auc_score, precision_score
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split
from prepocessing.preprocess import *

class model(object):
    def __init__(self, data):
        self.data = data
        self.LR = LogisticRegression() #LogisticClassifier
        self.RC = RidgeClassifier() #RidgeClassifier
        self.DTC = DecisionTreeClassifier()
        self.DTR = DecisionTreeRegressor()
        self.BNB = BernoulliNB()
        self.GNB = GaussianNB()
        self.LSVC = LinearSVC()
        self.NSVR = NuSVR()
        self.NSVC = NuSVC()
        self.classifiers = [self.LR, self.RC, self.DTC, self.DTR, self.BNB, self.GNB, self.LSVC, self.NSVR, self.NSVC]

    def data_split(self, data):
        feature = data.drop(["category"], axis = 1)
        label = data["category"]
        Xtrain, Ytrain, Xtest, Ytest = train_test_split(feature, label)
        return Xtrain, Ytrain, Xtest, Ytest

    def run_session(self, classifier, Xtrain, Ytrain, Xtest, Ytest):
        classifier.fit(Xtrain, Ytrain)
        Ypredict = classifier.predict(Xtest)
        return accuracy_score(Ytest, Ypredict), precision_score(Ypredict, Ytest), recall_score(Ytest, Ypredict), f1_score(Ytest, Ypredict)

    # def text2vec(self, data):
    #     pass






if __name__ == "__main__":
    pass
