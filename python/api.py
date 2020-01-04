import apiComponents as ApiComponents
import settingsService as SettingsService
import eventLog as EventLog

import random
import string
import json
import datetime
from functools import wraps

from flask import Flask, Response, request
from flask_cors import CORS
from flask_socketio import SocketIO
import jwt


def generateRandomString():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))

app = Flask(__name__)
app.config['SECRET_KEY'] = generateRandomString()
CORS(app)
loger = EventLog.getLoginServise()
systemStatus = ApiComponents.EventSinkAppState()
settingsServiceInst = SettingsService.SettingsService


@app.route('/api')
def hello_world():
    return 'Api root'

def tokenRequired(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        try:
            authHeader = request.headers.get('Authorization', '').split()[1]
            jwt.decode(authHeader.encode('utf-8'), app.config['SECRET_KEY'])
            return f(*args, **kwargs)
        except Exception:
            resp = Response('Can not auth.')
            resp.status_code = 401
            return resp
    return _verify

@app.route('/api/login', methods=['POST'])
def login():
    try:
        if not settingsServiceInst.matchAccesPassword(request.json['password']):
            raise Exception('Wrong password')
        print('OK',bool(settingsServiceInst.matchAccesPassword(request.json['password'])))
        token = jwt.encode({
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
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
def settingsGet():
    settings = settingsServiceInst.getFrontEndSettings()
    serializedSettings = json.dumps(settings)
    resp = Response(serializedSettings)
    return resp

@app.route('/api/events')
def eventGet():
    events = loger.getLastAny()
    eventsDir = map(lambda event: event.getDictionary(), events)
    #print('Events', list(eventsDir))
    list(eventsDir)
    serializedEvents = json.dumps(list(eventsDir))
    resp = Response(serializedEvents)
    return resp

@app.route('/api/settingsUpdate', methods=['POST'])
def settingsUpdate(): 
    try:
        print(request.json)
        newSettings = request.json
        settingsServiceInst.saveNewSettings(newSettings)
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

""" @socketio.on('connect')
def test_connect():
    print('Client connected')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

def onNewData():
    socketio.emit('NEW_STATE_AVAILIBLE', json)

def onNewLog():
    socketio.emit('EVENT_EMITED', json) """

if __name__ == '__main__':
    socketio.run(app, port=5000)
    #app.run(app, port=5000)

    login = EventLog.getLoginServise()

    def newSettigns():
        socketio.emit('NEW_STATE_AVAILIBLE')
    login.subscribeByName('Settings Change', newSettigns)

    def newEvent():
        socketio.emit('EVENT_EMITED')
    login.subscribeAny(newEvent)