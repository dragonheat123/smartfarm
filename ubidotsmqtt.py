# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 00:03:44 2017

@author: lorky
"""

import paho.mqtt.client as mqtt
import time


payload = []
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    connectval = rc
    return(connectval)
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("A1E-oBMSdNRG2Z2lkXagXnf16Ho2Hwfond",password=None)
client.connect("things.ubidots.com", 1883, 60)
client.loop_forever()
client.subscribe([("/v1.6/devices/smart-farm-1/manual-overide/lv",0),("/v1.6/devices/smart-farm-1/blue-led-level/lv",0)])


http://things.ubidots.com/api/v1.6/devices/smart-farm-1/manual-overide/values?token=A1E-oBMSdNRG2Z2lkXagXnf16Ho2Hwfond
