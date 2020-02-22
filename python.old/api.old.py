#!/usr/bin/env python3

import apiComponents as ApiComponents
import settingsService as SettingsService
import eventLog as EventLog
# import main as Main

import random
import string
import json
import datetime
from functools import wraps

from flask import Flask, Response, request
from flask_cors import CORS
from flask_socketio import SocketIO
import jwt

import threading


def generateRandomString():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))


app = Flask(__name__)
# JWT KEY
app.config['SECRET_KEY'] = generateRandomString()
# app.config['SECRET_KEY'] = 'SECRET'
CORS(app)
loger = EventLog.getLoginServise()
systemStatus = ApiComponents.EventSinkAppState()
settingsServiceInst = SettingsService.SettingsService

# Test route
@app.route('/api')
def hello_world():
    return 'Api root'

# Auth midleware


def tokenRequired(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        try:
            authHeader = request.headers.get('Authorization', '').split()[1]
            jwt.decode(authHeader.encode('utf-8'), app.config['SECRET_KEY'])
            return f(*args, **kwargs)
        except Exception as e:
            print('e', e)
            resp = Response('Can not auth.')
            resp.status_code = 401
            return resp
    return _verify


@app.route('/api/login', methods=['POST'])
def login():
    try:
        if not settingsServiceInst.matchAccesPassword(request.json['password']):
            raise Exception('Wrong password')
        print('OK', bool(settingsServiceInst.matchAccesPassword(
            request.json['password'])))
        token = jwt.encode({
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
        }, app.config['SECRET_KEY'])
        jsonResp = {
            'token': token.decode('utf-8')
        }
        resp = Response(json.dumps(jsonResp))
        return resp

    except Exception as e:
        print('[WARN]: Can not auth.', e)
        resp = Response('Can not auth.')
        resp.status_code = 401
        return resp


@app.route('/api/state')
@tokenRequired
def statusGet():
    state = systemStatus.getAll()
    serializedState = json.dumps(state)
    resp = Response(serializedState)
    return resp


@app.route('/api/settings')
@tokenRequired
def settingsGet():
    settings = settingsServiceInst.getFrontEndSettings()
    serializedSettings = json.dumps(settings)
    resp = Response(serializedSettings)
    return resp


@app.route('/api/events')
@tokenRequired
def eventGet():
    events = loger.getAll()
    # eventsDir = map(lambda event: event.__dict__, events)
    eventsDir = []
    for event in events:
        eventsDir.append(event.__dict__)
    print('Events', list(eventsDir), eventsDir)
    list(eventsDir)
    serializedEvents = json.dumps(eventsDir)
    # serializedEvents = json.dumps(events.__dict__)
    print('Events', serializedEvents)
    resp = Response(serializedEvents)
    return resp


@app.route('/api/settingsUpdate', methods=['POST'])
@tokenRequired
def settingsUpdate():
    try:
        print(request.json)
        newSettings = request.json
        settingsServiceInst.saveNewBasicSettings(newSettings)
        resp = Response('Succes')
        return resp
    except ValueError as e:
        print('[WARN]:', e)
        resp = Response('Cannot Parse')
        resp.status_code = 400
        return resp
    except Exception as e:
        print('[WARN]:', e)
        resp = Response('Wrong Json Format')
        resp.status_code = 400
        return resp


socketio = SocketIO(app, cors_allowed_origins="*")

if __name__ == '__main__':
    log = EventLog.getLoginServise()

    def newSettigns(_):
        socketio.emit('NEW_STATE_AVAILIBLE')
    log.subscribeByName('Settings Change', newSettigns)

    def newEvent(_):
        socketio.emit('EVENT_EMITED')
    log.subscribeAny(newEvent)

    def update():
        log.emit('DEBUG', EventLog.EventType.DEBUG)
        t = threading.Timer(10, update)
        t.setDaemon(True)
        t.start()
    update()
    # Main.init()
    socketio.run(app, port=5000)
