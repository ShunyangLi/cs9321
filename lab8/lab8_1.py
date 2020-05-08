"""
Name: lab8_1.py
Author: lsy
Time: 2020/4/5
"""
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.utils import shuffle
from sklearn.metrics import precision_score, accuracy_score, recall_score


def load_data(filename, percentage):
    """
    load the data and split the data
    :param filename: the data filename
    :param percentage: split percentage
    :return:
    """
    df = pd.read_csv(filename)
    # 打乱数据，为了更好的训练
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
    # read data
    x_train, y_train, x_test, y_test = load_data('iris.csv', 0.7)
    knn = KNeighborsClassifier()
    knn.fit(x_train, y_train)

    prediction = knn.predict(x_test)

    print("confusion_matrix:\n", confusion_matrix(y_test, prediction))
    print("precision:\t", precision_score(y_test, prediction, average=None))
    print("recall:\t\t", recall_score(y_test, prediction, average=None))
    print("accuracy:\t", accuracy_score(y_test, prediction))
