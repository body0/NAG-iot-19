#!/usr/bin/env python3
import devServices as DevServices
import common as Common
import apiComponents as ApiComponents
import settingsService as SettingsService
import eventLog as EventLog
import main as Main

import random
import string
import json
import datetime
from functools import wraps

from flask import Flask, Response, request
from flask_cors import CORS

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
""" systemStatus = ApiComponents.EventSinkAppState() """
settingsServiceInst = SettingsService.SettingsService
lights = DevServices.getLightService()
gate = DevServices.getGateService()

# Test route
@app.route('/api')
def hello_world():
    return 'Api root'

@app.route('/api/ledOn')
def ledOn():
    lights.turnOnForFor(Common.LightsIds.IN_HOUSE)

@app.route('/api/gateOn')
def gateOn():
    gate.openFor(10)


if __name__ == '__main__':
    log = EventLog.getLoginServise()

    """ def newSettigns(_):
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
    update() """
    Main.init()
    # socketio.run(app, port=5000)