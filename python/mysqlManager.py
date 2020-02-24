import mysql.connector
from flask import Flask, Response, request
from flask_cors import CORS

import json
import atexit

app = Flask(__name__)
CORS(app)
cnx = mysql.connector.connect(user='GRAFANA_ADMIN', password='abc',
                              host='80.211.204.64', port='3031',
                              database='GRAFANA')
# Test route
@app.route('/')
def hello_world():
    return 'DB api root'


@app.route('/test')
def ret():
    return 'DB api root'


@app.route('/espPld', methods=['POST'])
def espPld():
    try:
        #print('Q', request.data, request.headers, request.json)
        #print('D', request.json)
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

        """ insetQuery = "START TRANSACTION; \
                    INSERT INTO temperature (value) VALUES (%s); \
                    INSERT INTO humidity (value) VALUES (%s); \
                    INSERT INTO light (value) VALUES (%s); \
                    INSERT INTO presure (value) VALUES (%s); \
                    INSERT INTO batteryState (value) VALUES (%s); \
                    COMMIT;"
        insetQueryVal = (temp, pres, hum, light, batteryState)

        cursor = cnx.cursor()
        cursor.execute(insetQuery, insetQueryVal)
        cursor.close() """

        cursor = cnx.cursor()

        insetQuery = "INSERT INTO temperature  (value) VALUES (%s)"
        insetQueryVal = [int(temp)]
        cursor.execute(insetQuery, insetQueryVal)

        insetQuery = "INSERT INTO humidity (value) VALUES (%s);"
        insetQueryVal = [int(hum)]
        cursor.execute(insetQuery, insetQueryVal)

        insetQuery = "INSERT INTO light (value) VALUES (%s);"
        insetQueryVal = [int(light)]
        cursor.execute(insetQuery, insetQueryVal)

        insetQuery = "INSERT INTO presure (value) VALUES (%s);"
        insetQueryVal = [int(pres)]
        cursor.execute(insetQuery, insetQueryVal)

        insetQuery = "INSERT INTO batteryState (value) VALUES (%s);"
        insetQueryVal = [int(batteryState)]
        cursor.execute(insetQuery, insetQueryVal)

        cnx.commit()
        cursor.close()

        resp = Response('Succes')
        resp.status_code = 201
        return resp

    except Exception as e:
        print('[WARN]: Can not auth.', e)
        resp = Response('Internal error')
        resp.status_code = 500
        return resp


@app.route('/homePld', methods=['POST'])
def homePld():
    try:
        if (('temp' not in request.json) or
            ('pres' not in request.json) or
            ('light' not in request.json) or
                ('gateState' not in request.json)):
            resp = Response('Wrong argument')
            resp.status_code = 400
            return resp

        # print(request.json)
        temp = request.json['temp']
        pres = request.json['pres']
        light = request.json['light']
        batteryState = request.json['gateState']

        print(temp, pres, light, batteryState)

        cursor = cnx.cursor()

        insetQuery = "INSERT INTO temperature_home  (value) VALUES (%s)"
        insetQueryVal = [int(temp)]
        cursor.execute(insetQuery, insetQueryVal)

        insetQuery = "INSERT INTO light_home (value) VALUES (%s);"
        insetQueryVal = [int(pres)]
        cursor.execute(insetQuery, insetQueryVal)

        insetQuery = "INSERT INTO presure_home (value) VALUES (%s);"
        insetQueryVal = [int(light)]
        cursor.execute(insetQuery, insetQueryVal)

        insetQuery = "INSERT INTO gateState (value) VALUES (%s);"
        insetQueryVal = [batteryState]
        cursor.execute(insetQuery, insetQueryVal)

        cnx.commit()
        cursor.close()

        resp = Response('Succes')
        resp.status_code = 201
        return resp

    except Exception as e:
        print('[WARN]: Can not auth.', e)
        resp = Response('Internal error')
        resp.status_code = 500
        return resp


@app.route('/addEvent', methods=['POST'])
def addEvent():
    try:
        if (('name' not in request.json) or
            ('type' not in request.json) or
            ('pld' not in request.json) or
            ('timeOfCreation' not in request.json)):
            resp = Response('Wrong argument')
            resp.status_code = 400
            return resp

        # print(request.json)
        name = request.json['name']
        typeObj = request.json['type']
        pld = request.json['pld']
        timeOfCreation = request.json['timeOfCreation']

        cursor = cnx.cursor()

        insetQuery = "INSERT INTO temperature_home  (name, type, pld, timeOfCreation) VALUES (%s, %s, %s, %s)"
        insetQueryVal = [str(name), str(typeObj), str(pld), str(timeOfCreation)]
        cursor.execute(insetQuery, insetQueryVal)

        cnx.commit()
        cursor.close()

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
    # cursor.close()
    cnx.close()
    print("\nEND")


atexit.register(cleanup)
app.run(host='0.0.0.0')
