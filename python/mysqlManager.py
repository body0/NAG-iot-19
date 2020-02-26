import mysql.connector
from flask import Flask, Response, request
from flask_cors import CORS

import json
import atexit
import os
import requests

# Safely load api key from env
ApiKey = ''
if 'KEYAPI' in os.environ:
    ApiKey = os.environ['KEYAPI']

DbApiAccesToken = ''
if 'DB_API_ACCES_TOKEN' in os.environ:
    DbApiAccesToken = os.environ['DB_API_ACCES_TOKEN']

CleanExit = False


app = Flask(__name__)
CORS(app)
cnx = mysql.connector.connect(user='GRAFANA_ADMIN', password='abc',
                              host='80.211.204.64', port='3031',
                              database='GRAFANA')


# Test route
@app.route('/nagDbIntf')
def hello_world():
    return 'DB api root'

@app.route('/nagDbIntf/espPld', methods=['POST'])
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

        """ if (not request.json['accesToken'] == DbApiAccesToken):
            resp = Response('Wrong acces token')
            resp.status_code = 401
            return resp """
 

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
        insetQueryVal = [float(temp)]
        cursor.execute(insetQuery, insetQueryVal)

        insetQuery = "INSERT INTO humidity (value) VALUES (%s);"
        insetQueryVal = [int(hum)]
        cursor.execute(insetQuery, insetQueryVal)

        insetQuery = "INSERT INTO light (value) VALUES (%s);"
        insetQueryVal = [float(light)]
        cursor.execute(insetQuery, insetQueryVal)

        insetQuery = "INSERT INTO presure (value) VALUES (%s);"
        insetQueryVal = [int(pres)]
        cursor.execute(insetQuery, insetQueryVal)

        insetQuery = "INSERT INTO batteryState (value) VALUES (%s);"
        insetQueryVal = [float(batteryState)]
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


@app.route('/nagDbIntf/homePld', methods=['POST'])
def homePld():
    try:
        # print(request.json['temp'])
        if (('temp' not in request.json) or
            ('pres' not in request.json) or
            ('light' not in request.json) or
                ('gateState' not in request.json)):
            resp = Response('Wrong argument')
            resp.status_code = 400
            return resp

        """ if (not request.json['accesToken'] == DbApiAccesToken):
            resp = Response('Wrong acces token')
            resp.status_code = 401
            return resp """

        # print(request.json)
        temp = request.json['temp']
        pres = request.json['pres']
        light = request.json['light']
        batteryState = request.json['gateState']

        print(temp, pres, light, batteryState)

        cursor = cnx.cursor()

        insetQuery = "INSERT INTO temperature_home  (value) VALUES (%s)"
        insetQueryVal = [float(temp)]
        cursor.execute(insetQuery, insetQueryVal)

        insetQuery = "INSERT INTO light_home (value) VALUES (%s);"
        insetQueryVal = [float(light)]
        cursor.execute(insetQuery, insetQueryVal)

        insetQuery = "INSERT INTO presure_home (value) VALUES (%s);"
        insetQueryVal = [int(pres)]
        cursor.execute(insetQuery, insetQueryVal)

        insetQuery = "INSERT INTO gateState (value) VALUES (%s);"
        insetQueryVal = [float(batteryState)]
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


@app.route('/nagDbIntf/addEvent', methods=['POST'])
def addEvent():
    try:
        if (('arr' not in request.json)):
            resp = Response('Wrong argument')
            resp.status_code = 400
            return resp

        """ if (not request.json['accesToken'] == DbApiAccesToken):
            resp = Response('Wrong acces token')
            resp.status_code = 401
            return resp """

        # print(request.json)
        name = request.json['name']
        typeObj = request.json['type']
        pld = request.json['pld']
        timeOfCreation = request.json['timeOfCreation']

        for event in parsedEventList:

        insetQuery = "INSERT INTO event (name, type, pld, timeOfCreation) VALUES (%s, %s, %s, %s)"
        insetQueryVal = [str(name), str(typeObj), str(pld), str(timeOfCreation)]
        cursor.execute(insetQuery, insetQueryVal)

            cursor = cnx.cursor()

            insetQuery = "INSERT INTO event  (name, type, pld) VALUES (%s, %s, %s)"
            insetQueryVal = [str(name), str(typeObj), str(pld)]
            cursor.execute(insetQuery, insetQueryVal)

            cnx.commit()
            cursor.close()

        resp = Response('Succes')
        resp.status_code = 201
        return resp

    except Exception as e:
        print('[WARN]: Can not auth.', e)
        #raise e
        resp = Response('Internal error')
        resp.status_code = 500
        return resp



"""
    HTTP CLIENT
        - send data to server
        - auth to server
"""
def sendToUpstream(eventName, data):
    jsonData = {'value': data}
    header = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Api-Key': ApiKey
    }
    print("https://api.nag-iot.zcu.cz/v2/value/" + eventName, header, jsonData)
    try:
        req = requests.post("https://api.nag-iot.zcu.cz/v2/value/" + eventName, json=jsonData, headers=header)
        return req.status_code
    except Exception as e:  # time out
        print(e)
        return 500


def cleanup():
    global CleanExit
    CleanExit = True
    cnx.commit()
    # cursor.close()
    cnx.close()
    print("\nEND")


atexit.register(cleanup)
app.run(host='0.0.0.0', port=3005)
