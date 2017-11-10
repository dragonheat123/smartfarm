# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 12:52:59 2017

@author: lorky
"""

###3https://www.epochconverter.com/ 

import time
import datetime
import http.client 
import json

def deleteValues(id):
    conn = http.client.HTTPConnection("things.ubidots.com", 80, timeout=60)
    conn.request("DELETE", "/api/v1.6/variables/"+str(id)+"/values/0/"+str(round(time.time())*1000)+"/?token=A1E-oBMSdNRG2Z2lkXagXnf16Ho2Hwfond")
    r1 = conn.getresponse()
    print(r1.status, r1.reason)
    
def getVarList():
    conn = http.client.HTTPConnection("things.ubidots.com", 80, timeout=60)
    conn.request("GET", "/api/v1.6/datasources/59ed03a2c03f9757233617d8/variables?token=A1E-oBMSdNRG2Z2lkXagXnf16Ho2Hwfond")
    r1 = conn.getresponse()
    a = json.loads(r1.read().decode())
    print(r1.status, r1.reason)   
    return a

    
a = getVarList()


for i in a["results"]:
    print(i['name'])
    deleteValues(i["id"])
    time.sleep(1)