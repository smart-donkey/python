import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import SGDClassifier
from sklearn.datasets.samples_generator import make_blobs
import random
from sklearn.metrics import classification_report
import sys
import MySQLdb as mdb
import update


def fetch_data(code, start_date):

    try:
        con = mdb.connect('127.0.0.1', 'root', '', 'test_algorithm')

        with con:

            cursor = con.cursor()
            cursor.execute("SELECT * FROM history_data WHERE code in ('%s') and date >= '%s';" % (code, start_date))
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


def low_get(records, x, start_index=0, sell=0.1, buy=0.1, beta=1):
    # if start_index > len(records):
    # print(start_index, len(records))
    start_value = records[start_index]
    total_cost = x * records[start_index]
    # print 'intial buy', total_cost
    total_share = x
    last_close = 0
    win = 0.0

    day = 1
    for close_value in records[start_index:]:
        last_close = close_value
        if (close_value / start_value) < 1 - buy:
            total_cost += beta * x * close_value
            total_share += beta * x
            start_value = close_value
            # print 'buy', close_value
        elif (total_share * close_value) / total_cost > 1 + sell:
            # print ("win:", (total_share * close_value - total_cost))
            # print ("total_share:", total_share)
            # print ("day:", day)
            # print 'sell', close_value
            break
            # print total_share * close_value
        day += 1

    win = total_share * last_close - total_cost
    # print ("total cost:", total_cost)
    # print ("total share:", total_share)

    # print day, win, total_cost
    return day, win, total_cost


def strategy_2(records, x, start_index=0, sell=0.1, buy=0.1, beta=1):
    start_value = records[start_index]
    # total_cost = x * records[start_index]
    # total_share = x
    total_cost = 0
    total_share = 0

    last_close = 0
    win = 0.0

    day = 1
    for close_value in records[start_index:]:
        last_close = close_value
        if (close_value / start_value) < 1 - buy:
            total_cost += beta * x * close_value
            total_share += beta * x
            start_value = close_value
            # print 'buy', close_value
        elif total_cost > 0 and (total_share * close_value) / total_cost > 1 + sell:
            # print ("win:", (total_share * close_value - total_cost))
            # print ("total_share:", total_share)
            # print ("day:", day)
            # print 'sell', close_value
            break
            # print total_share * close_value
        day += 1

    win = total_share * last_close - total_cost
    # print ("total cost:", total_cost)
    # print ("total share:", total_share)

    # print day, win, total_cost
    return day, win, total_cost


def find_max_profit(start_date):
    code_list = update.fetch_index()
    days = []
    # code_list = code_list[:500]
    for one_code in code_list:
        chance = get_max_day(one_code, start_date)
        days.append(chance)

    results = [(day, code_list[i]) for i, day in enumerate(days)]
    results.sort(reverse=True)
    for result in results[:1200]:
        print result

    return results

    # for () enumerate(day)


def get_max_day(one_code, start_date):
    data = fetch_data(one_code, start_date)
    if len(data) <= 0:
        # print 'yes', one_code
        return 0
    close = [one[5] for one in data]
    total_day = 0
    total_win = 0
    max_cost = 0
    max_day = 0
    loop = 0
    win_avg = 0
    while True:
        day, win, total_cost = low_get(close, 500, start_index=total_day, sell=0.1, buy=0.1, beta=2)
        win_avg += win / total_cost
        max_day = max(day, max_day)
        max_cost = max(total_cost, max_cost)
        total_day += day + 1
        total_win += win
        # print(total_day)
        loop += 1
        if total_day > len(close) - 2:
            break

    # print 'summarize:'
    # print total_win, max_cost, max_day, loop, win_avg / loop
    return loop


if __name__ == '__main__':
    # code = '601985.ss'
    # # X, Y = fetch_data(code)
    # data = fetch_data(code, '2015-08-01')
    # close = [one[5] for one in data]
    # total_day = 0
    # total_win = 0
    # max_cost = 0
    # max_day = 0
    # loop = 0
    # win_avg = 0
    # while True:
    #     day, win, total_cost = low_get(close, 500, start_index=total_day, sell=0.1, buy=0.1, beta=2)
    #     win_avg += win / total_cost
    #     max_day = max(day, max_day)
    #     max_cost = max(total_cost, max_cost)
    #     total_day += day + 1
    #     total_win += win
    #     # print(total_day)
    #     loop += 1
    #     if total_day > len(close) - 2:
    #         break
    #
    # print 'summarize:'
    # print total_win, max_cost, max_day, loop, win_avg / loop
    # print close
    # for one_day in data:
    #     print one_day
    # print data
    # aa = np.diff(stocks)
    # print stocks
    # print train_data[:0][:-1]
    # print aa / train_data[:0][:-1]

    # for i in range(len(test_data)):
    #     prob = clf.predict(test_data[i])
    #     print(test_labels[i], prob)

    results = find_max_profit('2015-08-01')
    real_result = [result for result in results if result[0] > 0]
    print len(real_result)



