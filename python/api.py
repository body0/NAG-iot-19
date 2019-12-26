import apiComponents as ApiComponents
import settingsService as SettingsService

import json
from flask import Flask, Response
from flask_socketio import SocketIO

app = Flask(__name__)
systemStatus = ApiComponents.EventSinkAppState()
settingsServiceInst = SettingsService.SettingsService

@app.route('/api')
def hello_world():
    return 'Api root'

@app.route('/api/state')
def get_status():
    state = systemStatus.getAll()
    resp = Response(json.dumps(state))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/api/settingsGet')
def settingsGet():
    settings = settingsServiceInst.getSettings()
    serializedSettings = json.dumps(settings)
    return serializedSettings

@app.route('/api/settingsUpdate',  methods=['POST'])
def settingsUpdate(): 
    try:
        newSettings = json.loads()
        settingsServiceInst.saveNewSettings(newSettings)
        return 'Succes'
    except 
        return 'Cannot Parse', 400
    except:
        return 'Wrong Json Format', 400

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