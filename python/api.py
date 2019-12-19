import apiComponents as ApiComponents
import json
from flask import Flask

print(__name__)
app = Flask(__name__)
systemStatus = ApiComponents.EventSinkAppState()

@app.route('/api')
def hello_world():
    return 'Api root'

@app.route('/api/state')
def get_status():
     state = systemStatus.getAll()
     return json.dumps(state)






    

