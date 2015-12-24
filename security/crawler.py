__author__ = 'roger'

import urllib2
# import csv
import sys
import MySQLdb as mdb


def fetch_data(code):

    try:
        con = mdb.connect('127.0.0.1', 'root', '', 'test_algorithm')

        with con:

            cursor = con.cursor()
            cursor.execute("SELECT * FROM history_data WHERE code in ('%s');" % code)
            rows = cursor.fetchall()

            data = [row for row in rows]
            for attribute in data:
                print attribute

        # print "MySql version: %s" % result.fetch_row()[0]
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
    finally:
        if con:
            con.close()


def parse_data(raw):
    raw_string = str(raw)
    lines = raw_string.split('\n')
    for line in lines:
        print line

    return lines


def insert_data(lines, code):
    try:
        con = mdb.connect('127.0.0.1', 'root', '', 'test_algorithm')

        header_skipper = False
        with con:
            for line in lines:
                data = str(line).split(',')
                cur = con.cursor()

                if not header_skipper:
                    header_skipper = True
                    continue
                print data

                if len(data) == 7:
                    sql = "INSERT IGNORE INTO  history_data VALUES ('%s', '%s', %s, %s, %s, %s, %s, %s); " % (code, data[0], data[1], data[2], data[3], data[4], data[5], data[6])
                    cur.execute(sql)
                print sql
                # cur.execute(sql)

        #con.query("SELECT VERSION()")
        #result = con.use_result()


        # print "MySql version: %s" % result.fetch_row()[0]
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
    finally:
        if con:
            con.close()


def crawler(code):
    request_url = 'http://table.finance.yahoo.com/table.csv?s=%s' % code
    print request_url
    req = urllib2.Request(request_url)
    response = urllib2.urlopen(req)
    the_page = response.read()
    # reader = csv.reader(the_page)
    # for line in reader:
    #     print line
    # print the_page
    lines = parse_data(the_page)
    insert_data(lines, code)


if __name__ == '__main__':
    code = "600036.ss"
    # fetch_data(code)
    # crawler(code)
