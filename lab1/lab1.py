import sqlite3
import requests
import pandas as pd
from pymongo import MongoClient


def read_csv(filename):
    """
    :param filename: the filename which need to read
    """
    return pd.read_csv(filename)


def store_scv(data_frame, filename):
    """
    :param data_frame: the pandas data frame
    :param filename: the filename which need to be stored
    :return:
    """
    data_frame.to_csv(filename, sep=',', encoding='utf-8')


def show_col_row(data_frame, show_col=True, show_row=True):
    """
    :param data_frame: the pandas data frame
    :param show_col: whether show col
    :param show_row: whether show row
    :return:
    """
    if show_col:
        print(", ".join([col for col in data_frame]))

    if show_row:
        for index, row in data_frame.iterrows():
            print(", ".join([str(row[col]) for col in data_frame]))


def store_sqlite(data_frame, table_name, conn):
    """
    :param conn: sqlite3 con
    :param data_frame: the pandas data frame
    :param table_name: the tables name in sql
    :return:
    """
    data_frame.to_sql(table_name, conn)


def read_db(query, conn):
    """
    :param query: query language
    :param conn: connect sqlite3
    :return: the data frame after reading database
    """
    return pd.read_sql_query(query, conn)


def connect_mongo(database_name, collection, host='127.0.0.1', port='27017'):
    """

    :param collection: the database collection
    :param database_name: which database need to connect
    :param host: the host of mongodb
    :param port: the port of mongodb
    :return: cursor
    """
    client = MongoClient('mongodb://%s:%s/' % (host, port))
    return client[database_name][collection]


def read_mongo(db, query={}):
    """
    :param db: the mongo db database
    :param query: query language
    :return:
    """
    cursor = db.find(query)
    df = pd.DataFrame(list(cursor))
    del df['_id']
    return df


def store_mongo(db, data_frame):
    """

    :param db: database
    :param data_frame: the data frame
    :return:
    """
    data = []
    for index, row in data_frame.iterrows():
        t = {}
        for col in data_frame:
            t[col] = str(row[col])
        data.append(t)
    db.insert_many(data)


def get_web_json(url):
    """
    get the json file from an url
    :param url: the json url
    :return:
    """
    res = requests.get(url)
    return res.json()


def pd_read_json(json_data):
    """
    read json from an url through pandas
    :param json_data: json files
    :return:
    """
    col = []
    data = json_data['data']
    for c in json_data['meta']['view']['columns']:
        col.append(c['name'])

    df = pd.DataFrame(data=data, columns=col)
    return df


def conn_db(filename):
    """

    :param filename: the filename of db
    :return: return the cursor
    """
    return sqlite3.connect(filename)


if __name__ == '__main__':
    # df = read_csv('Demographic_Statistics_By_Zip_Code.csv')
    # show_col_row(df, show_row=False)
    # show_col_row(df, show_col=False)
    # store_scv(df, 'test.csv')
    con = sqlite3.connect('test.db')
    # # store_sqlite(df, 'test', con)
    # df = read_db("SELECT * FROM test", con)
    # show_col_row(df)
    # conn = connect_mongo('comp9321', 'Demographic_Statistics')
    # store_mongo(conn, df)
    # df = read_mongo(conn, query={})
    # show_col_row(df)
    json = get_web_json('https://data.cityofnewyork.us/api/views/kku6-nxdu/rows.json')
    df = pd_read_json(json)
    show_col_row(df)
    store_sqlite(df, 'online', con)

