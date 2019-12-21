import apiComponents as ApiComponents
import json
from flask import Flask, Response
from flask_socketio import SocketIO

app = Flask(__name__)
systemStatus = ApiComponents.EventSinkAppState()

@app.route('/api')
def hello_world():
    return 'Api root'

@app.route('/api/state')
def get_status():
    state = systemStatus.getAll()
    resp = Response(json.dumps(state))
    resp.headers['Access-Control-Allow-Origin'] = '*'
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