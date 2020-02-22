import mysql.connector
from flask import Flask, Response, request
from flask_cors import CORS

import json
import atexit

app = Flask(__name__)

cnx = mysql.connector.connect(user='GRAFANA_ADMIN', password='abc',
                              host='80.211.204.64', port='3031',
                              database='GRAFANA')
cursor = cnx.cursor()

# Test route
@app.route('/')
def hello_world():
    return 'DB api root'

@app.route('/espPld', methods=['POST'])
def login():
    try:
        if (('temp' not in request.json) or
            ('pres' not in request.json) or
            ('hum' not in request.json) or
            ('light' not in request.json) or
            ('batteryState' not in request.json)):
            resp = Response('Wrong argument')
            resp.status_code = 400
            return resp

        temp = request.json['temp']
        pres = request.json['pres']
        hum = request.json['hum']
        light = request.json['light']
        batteryState = request.json['batteryState']

        insetQuery = "INSERT INTO temperature (value) VALUES (%s); \
                    INSERT INTO humidity (value) VALUES (%s); \
                    INSERT INTO light (value) VALUES (%s); \
                    INSERT INTO presure (value) VALUES (%s); \
                    INSERT INTO batteryState (value) VALUES (%s);"
        insetQueryVal = (temp, pres, hum, light, batteryState)

        cursor.execute(insetQuery, insetQueryVal)
        resp = Response('Succes')
        resp.status_code = 201
        return resp

    except Exception as e:
        print('[WARN]: Can not auth.', e)
        resp = Response('Internal error')
        resp.status_code = 500
        return resp


@app.route('/homePld', methods=['POST'])
def login():
    try:
        if (('temp' not in request.json) or
            ('pres' not in request.json) or
            ('light' not in request.json) or
            ('gateState' not in request.json)):
            resp = Response('Wrong argument')
            resp.status_code = 400
            return resp

        temp = request.json['temp']
        pres = request.json['pres']
        light = request.json['light']
        batteryState = request.json['gateState']

        insetQuery = "INSERT INTO temperature (value) VALUES (%s); \
                    INSERT INTO light (value) VALUES (%s); \
                    INSERT INTO presure (value) VALUES (%s); \
                    INSERT INTO gateState (value) VALUES (%s);"
        insetQueryVal = (temp, pres, hum, light, batteryState)

        cursor.execute(insetQuery, insetQueryVal)
        resp = Response('Succes')
        resp.status_code = 201
        return resp

    except Exception as e:
        print('[WARN]: Can not auth.', e)
        resp = Response('Internal error')
        resp.status_code = 500
        return resp

def cleanup():
    cnx.commit()
    cursor.close()
    cnx.close()
    print("\nEND")

    
atexit.register(cleanup)