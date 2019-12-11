"""
    HTTP CLIENT

        - send data to server
"""

def send(eventName, data):
        """
        :param eventName: name of variable on website
        :param data: integer data, that will be posted to server
        :return: status code
        """
        jsonData = {'value': data}
        header = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'x-Api-Key': 'qAC9kAwXDBKTc3cS'
        }
        try:
            req = requests.post("https://api.nag-iot.zcu.cz/v1/value/" + eventName, json=jsonData, headers=header)
            return req.status_code
        except:  # time out
            return 500