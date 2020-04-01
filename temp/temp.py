"""
zxxx.db
"""
import uuid
import requests
import sqlite3
from flask import Flask
from flask_restplus import Api
from flask_restful import reqparse

UUID = uuid.uuid1()

app = Flask(__name__)
api = Api(app)


response = requests.get('http://api.worldbank.org/v2/countries/all/indicators/NY.GDP.MKTP.CD?date=2012:2017&format=json&per_page=1000')

data = response.json()

for d in data[1]:
    index = 1
    indicator = d['indicator']['id']
    indicator_value = d['indicator']['value']
    country = d['country']['value']
    country_id = d['country']['id']
    countryiso3code = d['countryiso3code']
    date = int(d['date'])
    value = d['value']
    unit = d['unit']
    obs_status = d['obs_status']
    decimal = d['decimal']

    conn = sqlite3.connect('zxxxxx.db')
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO test(id, indicator, indicator_id, country, country_id, countryiso3code, date, unit, obs_status, decimal, value)
        values (?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,?)
        """, (index, indicator, indicator_value, country, country_id, country_id, date, unit, obs_status, decimal, value)
    )
    conn.commit()
    conn.close()



def test():
    conn = sqlite3.connect('zxxxxx.db')
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS test (
            id int ,
            indicator text,
            indicator_id text,
            country text,
            country_id text,
            countryiso3code text,
            date int,
            unit text,
            obs_status text,
            decimal text,
            value real
        );""")
    conn.commit()
    conn.close()


if __name__ == '__main__':
    test()
