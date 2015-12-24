"""
=========================================
SGD: Maximum margin separating hyperplane
=========================================

Plot the maximum margin separating hyperplane within a two-class
separable dataset using a linear Support Vector Machines classifier
trained using SGD.
"""
print(__doc__)


import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import SGDClassifier
from sklearn.datasets.samples_generator import make_blobs
import random
from sklearn.metrics import classification_report
import sys
import MySQLdb as mdb


def fetch_data(code):

    try:
        con = mdb.connect('127.0.0.1', 'root', '', 'test_algorithm')

        with con:

            cursor = con.cursor()
            cursor.execute("SELECT * FROM history_data WHERE code in ('%s');" % code)
            rows = cursor.fetchall()
            # data = [(row[2], row[3], row[4], row[5], row[7]) for row in rows]
            record = [row for row in rows]

        return record
        # print "MySql version: %s" % result.fetch_row()[0]
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
    finally:
        if con:
            con.close()


def extract_feature(data):
    Y = []
    # data = data[:30]
    # print(data)
    # num_data = [(a[3], a[4], a[5], a[6]) for a in data]
    num_data = [(a[5], a[6]) for a in data]
    count = len(num_data)
    # feature_vector = np.arange(count, dtype=float)
    feature_vector = np.zeros((count, 2))
    np_array_data = np.array(num_data)
    labels = np.zeros((count, 1))
    threhold = 0.02
    for i in range(len(np_array_data)):
        feature_vector[i] = 0
        ratio = 0
        if i > 1:
            diff = np_array_data[i - 1][0] - np_array_data[i - 2][0]
            volume_diff = np_array_data[i - 1][1] - np_array_data[i - 2][1]
            if np_array_data[i - 1][0] != 0:
                ratio = float(np_array_data[i][0] - np_array_data[i - 1][0]) / float(np_array_data[i - 1][0])
            # print(diff)
            # feature_vector[i] = (diff, np_array_data[i - 2][1] != 0 and volume_diff / np_array_data[i - 2][1])
            feature_vector[i] = (diff, 0)
        if ratio > threhold:
            labels[i] = 1
        elif ratio < -threhold:
            labels[i] = -1
        else:
            labels[i] = 0

    # print(feature_vector, labels)
    return feature_vector, labels

if __name__ == '__main__':
    code = '600036.ss'
    # X, Y = fetch_data(code)
    data = fetch_data(code)
    feature_vector, labels = extract_feature(data)
    train_data = feature_vector[-80: -60]
    train_data_labels = labels[-80: -60]

    np.linalg.svd()
    # print train_data[:, 0]
    stocks = train_data[:, 0]
    print np.ravel(stocks, order='K')
    # aa = np.diff(stocks)
    # print stocks
    # print train_data[:0][:-1]
    # print aa / train_data[:0][:-1]

    # for i in range(len(test_data)):
    #     prob = clf.predict(test_data[i])
    #     print(test_labels[i], prob)



