"""
Name: lab8_3.py
Author: lsy
Time: 2020/4/5
"""
import pandas as pd
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.utils import shuffle


def load_data(filename, percentage):
    """
    load the data and split the data
    :param filename: the data filename
    :param percentage: split percentage
    :return:
    """
    df = pd.read_csv(filename)
    df = shuffle(df)
    # x train data
    x = df.iloc[:, 0:4]
    # y train data
    y = df.iloc[:, 4]

    split_len = int(len(x) * percentage)

    x_train = x[:split_len]
    y_train = y[:split_len]
    x_test = x[split_len:]
    y_test = y[split_len:]

    return x_train, y_train, x_test, y_test


if __name__ == '__main__':
    x_train, y_train, x_test, y_test = load_data('iris.csv', 0.7)
    classifiers = [
        KNeighborsClassifier(),
        DecisionTreeClassifier(),
        LinearDiscriminantAnalysis(),
        LogisticRegression(),
        GaussianNB(),
        SVC(),
    ]
    accuracy_list = []
    for index, classifier in enumerate(classifiers):
        accuracies = cross_val_score(classifier, x_train, y_train, cv=5)
        accuracy_list.append((accuracies.mean(), type(classifier).__name__))

    accuracy_list = sorted(accuracy_list, reverse=True)

    for ac in accuracy_list:
        print("classifier: {}, accuracy: {}".format(ac[1], ac[0]))
