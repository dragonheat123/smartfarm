# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 13:31:03 2017
@author: lorky
"""

import http.client 
import json
import time

###LIGHTING STATE VARIABLES
cycle_state = 0
on_time = 0
off_time = 0


####TIMING VARIABLES
tlastcheck = 0
tlastsend

###INITIALIZE VARIABLES FOR DATA UPLOAD
d = {}
d["avg-blue-ppfd"] = 0
d["avg-red-ppdf"] = 0
d["blue-led-level"] = 0                 ###send the calculated value for blue avg ppfd
d["red-led-level"] = 0                      ###send the calculated value for avg red ppfd
d["humidity"] = 0
d["temperature"] = 0
d["leaf-area-1"] = 0
d["leaf-area-2"] = 0
d["light-sensor-1"] = 0                 ##sensor position not decided --> planned to draw a colored html table to show light intensity
d["light-sensor-2"] = 0
d["light-sensor-3"] = 0
d["light-sensor-4"] = 0
d["light-sensor-5"] = 0
d["light-sensor-6"] = 0
d["manual-overide"] = 0                 ##update this back to zero after manual overide is triggered and changes to led level and cycle implemented
d["pot-1-weight"] = 0                   ###averaged pot weight
d["pot-2-weight"] = 0
d["pot-3-weight"] = 0
d["soil-moisture-1"] = 0
d["soil-moisture-2"] = 0
d["soil-moisture-3"] = 0 
 
############defining httpclient functions

def getData():
    conn = http.client.HTTPConnection("things.ubidots.com", 80, timeout=60)
    
    conn.request("GET", "/api/v1.6/devices/smart-farm-1/on-cycle/lv?token=A1E-oBMSdNRG2Z2lkXagXnf16Ho2Hwfond")
    r1 = conn.getresponse()
    print('oncycle ', r1.getresponse().status, r1.getresponse().reason)
    on_cycle = float(str(r1.read(),'utf-8'))
    
    conn.request("GET", "/api/v1.6/devices/smart-farm-1/cycle-period/lv?token=A1E-oBMSdNRG2Z2lkXagXnf16Ho2Hwfond")
    r1 = conn.getresponse()
    print('cycle-period ', r1.getresponse().status, r1.getresponse().reason)
    cycle_period = float(str(r1.read(),'utf-8'))

    conn.request("GET", "/api/v1.6/devices/smart-farm-1/blue-led-level/lv?token=A1E-oBMSdNRG2Z2lkXagXnf16Ho2Hwfond")
    r1 = conn.getresponse()
    print('blue-led-level ', r1.getresponse().status, r1.getresponse().reason)
    blue_led_level = float(str(r1.read(),'utf-8'))

    conn.request("GET", "/api/v1.6/devices/smart-farm-1/red-led-level/lv?token=A1E-oBMSdNRG2Z2lkXagXnf16Ho2Hwfond")
    r1 = conn.getresponse()
    print('red-led-level ', r1.getresponse().status, r1.getresponse().reason)
    red_led_level = float(str(r1.read(),'utf-8'))
    
    conn.request("GET", "/api/v1.6/devices/smart-farm-1/manual-overide/lv?token=A1E-oBMSdNRG2Z2lkXagXnf16Ho2Hwfond")
    r1 = conn.getresponse()
    print('manual-overide ', r1.getresponse().status, r1.getresponse().reason)
    manual_overide = float(str(r1.read(),'utf-8'))    
    
    conn.close()
    return on_cycle, cycle_period, blue_led_level, red_led_level, manual_overide


def sendData():
    conn = http.client.HTTPConnection("things.ubidots.com", 80, timeout=60)
    headers = {'Content-type': 'application/json',"Connection": "close"}
    json_foo = json.dumps(d)
    conn.request("POST", "/api/v1.6/devices/smart-farm-1/?token=A1E-oBMSdNRG2Z2lkXagXnf16Ho2Hwfond",json_foo,headers)
    print('sending data ', conn.getresponse().status, con.getresponse().reason)
    conn.close()
    
def sendUpdateConfirmation():
    conn = http.client.HTTPConnection("things.ubidots.com", 80, timeout=60)
    headers = {'Content-type': 'application/json',"Connection": "close"}
    foo = {'manual-overide': 0}
    json_foo1 = json.dumps(foo)
    conn.request("POST", "/api/v1.6/devices/smart-farm-1/?token=A1E-oBMSdNRG2Z2lkXagXnf16Ho2Hwfond",json_foo,headers)
    print('sending update ', conn.getresponse().status, con.getresponse().reason)
    conn.close()


##########LIGHT OPERATING FUNCTIONS
def set_pwm_red(x):
    ###GPIOxxxx.pwm(freq,x)

def set_pwm_blue(x):
    ####GPIOxxxx.pwm(freq,x)
        
    

##################start of actual code

while 1: 
    if time.time()-tlastcheck>300:   ## check server for settings every 5mins 
        u_on_cycle, u_cycle_period, u_blue_led_level, u_red_led_level, u_manual_overide = getData()
        tlastcheck = time.time()
        
    if u_manual_overide == 1 & u_cycle_period>=u_on_cycle:
        cycle_state = 1                 ####start on cycle immediately
        on_time = time.time()
        off_time = (on_time + u_on_cycle*60*60)   ###find next off time by converting seconds
        sendUpdateConfirmation()
    
    if cycle_state == 1 & time.time()<off_time & time.time()>on_time:  ###on stage
        #set_pwm_red(u_red_led_level)
        #set_pwm_blue(u_blue_led_level)
    
    if cycle_state == 1 & time.time()>=off_time:
        cycle_state = 0
        on_time = off_time + (u_cycle_period-u_on_cycle)*60*60
     
    if cycle_state == 0 & time.time()<on_time & time.time()>off_time:
        #set_pwm_red(0)
        #set_pwm_blue(0)
        
    if cycle_state == 0 & time.time()>on_time & on_time!=off_time:
        cycle_state =1
        off_time = (on_time + u_on_cycle*60*60)      
    

    if time.time() - tlastsend > 0:   
        ### insert measurements
        
        ##fill in data dictionary
        
        d["avg-blue-ppfd"] = blah
        d["avg-red-ppdf"] = blah
        d["blue-led-level"] = blah                 ###send the calculated value for blue avg ppfd
        d["red-led-level"] = blah                     ###send the calculated value for avg red ppfd
        d["humidity"] = blah
        d["temperature"] = blah
        d["leaf-area-1"] = blah
        d["leaf-area-2"] = blah
        d["light-sensor-1"] = blah                 ##sensor position not decided --> planned to draw a colored html table to show light intensity
        d["light-sensor-2"] = blah
        d["light-sensor-3"] = blah
        d["light-sensor-4"] = blah
        d["light-sensor-5"] = blah
        d["light-sensor-6"] = blah
        d["manual-overide"] = blah                 ##update this back to zero after manual overide is triggered and changes to led level and cycle implemented
        d["pot-1-weight"] = blah                   ###averaged pot weight
        d["pot-2-weight"] = blah
        d["pot-3-weight"] = blah
        d["soil-moisture-1"] = blah
        d["soil-moisture-2"] = blah
        d["soil-moisture-3"] = blah      
        
        
        sendData()
        
        tlastsend = time.time()
    
    
        ###record data in a csv file
    
    




      