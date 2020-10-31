#!/usr/bin/python
import paho.mqtt.client as paho
import time
from urllib.parse import urlparse
import datetime
from hsyapi import HSYAPI

# HSYAPI
api = HSYAPI()

# Mqtt
mqttc = paho.Client()
url_str = 'mqtt://127.0.0.1:1883'
url = urlparse(url_str)

def sendmqtt(topic, mess):
    try:
        mqttc.connect(url.hostname, url.port)
        mqttc.publish("hsypy/" + topic, mess)
        print(topic, mess)
        sleep(5)
    except:
        pass

sendmqtt("debug", "HSYmqtt started")

raw_response = api.update()
data = api.parse(raw_response.text)
for line in data:
    sendmqtt(line, data[line])

sendmqtt("updated", datetime.datetime.now().strftime("%H:%M %d.%m.%Y"))

sendmqtt("debug", "HSYmqtt done")
