#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") == "check.price":
    result = req.get("result")
    parameters = result.get("parameters")
    zone = parameters.get("Item-Cost")
    cost = {'milk':10, 'bread':8, 'eggs':20, 'sugar':11,'yoghurt':13}
    speech = "The cost of  " + zone + " is K" + str(cost[zone]) + "."
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-pricechecker"
    }
    elif req.get("result").get("action")=="make.order":
    result = req.get("result")
    parameters = result.get("parameters")
    zone = []
    zone = parameters.get("Item-Cost")
    cost = {'milk':10, 'bread':8, 'eggs':20, 'sugar':11,'yoghurt':13}
    total = 0
    for x in zone:
     total += cost[x]
    speech = "The cost of your goods is K"+ str(total)
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-pricechecker"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
