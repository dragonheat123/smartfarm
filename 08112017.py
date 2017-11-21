# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 11:08:48 2017

@author: Brian
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 23:47:24 2017

@author: Brian
"""
import time
import datetime
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008 
import RPi.GPIO as GPIO
import numpy as np
import smbus
import sys
from hx711 import HX711
import Adafruit_DHT
import http.client 
import json
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError
import sys
import picamera

###INITIALIZE VARIABLES FOR DATA UPLOAD
d = {}
dbx = dropbox.Dropbox("-maRW30I7sAAAAAAAAAAC6tQJp7TB2pp7-qZQ9mijGMPqhE4F48G3eMslstwzbZo")
imagepath = '/home/pi/Desktop/now.jpg'
dbpath1 = '/'+str(round(time.time()))+'.jpg'
dbpath2 = '/now.jpg'

def getData():
    conn = http.client.HTTPConnection("things.ubidots.com", 80, timeout=60)
    
    conn.request("GET", "/api/v1.6/devices/smart-farm-1/on-cycle/lv?token=A1E-oBMSdNRG2Z2lkXagXnf16Ho2Hwfond")
    r1 = conn.getresponse()
    print('oncycle ', r1.status, r1.reason)
    on_cycle = float(str(r1.read(),'utf-8'))
    
    conn.request("GET", "/api/v1.6/devices/smart-farm-1/cycle-period/lv?token=A1E-oBMSdNRG2Z2lkXagXnf16Ho2Hwfond")
    r1 = conn.getresponse()
    print('cycle-period ', r1.status, r1.reason)
    cycle_period = float(str(r1.read(),'utf-8'))

    conn.request("GET", "/api/v1.6/devices/smart-farm-1/blue-led-level/lv?token=A1E-oBMSdNRG2Z2lkXagXnf16Ho2Hwfond")
    r1 = conn.getresponse()
    print('blue-led-level ', r1.status, r1.reason)
    blue_led_level = float(str(r1.read(),'utf-8'))

    conn.request("GET", "/api/v1.6/devices/smart-farm-1/red-led-level/lv?token=A1E-oBMSdNRG2Z2lkXagXnf16Ho2Hwfond")
    r1 = conn.getresponse()
    print('red-led-level ', r1.status, r1.reason)
    red_led_level = float(str(r1.read(),'utf-8'))
    
    conn.request("GET", "/api/v1.6/devices/smart-farm-1/manual-overide/lv?token=A1E-oBMSdNRG2Z2lkXagXnf16Ho2Hwfond")
    r1 = conn.getresponse()
    print('manual-overide ', r1.status, r1.reason)
    manual_overide = float(str(r1.read(),'utf-8'))    

    conn.request("GET", "/api/v1.6/devices/smart-farm-1/t_hr/lv?token=A1E-oBMSdNRG2Z2lkXagXnf16Ho2Hwfond")
    r1 = conn.getresponse()
    print('t_hr ', r1.status, r1.reason)
    t_hr = float(str(r1.read(),'utf-8'))     
    
    conn.request("GET", "/api/v1.6/devices/smart-farm-1/t-min/lv?token=A1E-oBMSdNRG2Z2lkXagXnf16Ho2Hwfond")
    r1 = conn.getresponse()
    print('t_min ', r1.status, r1.reason)
    t_min = float(str(r1.read(),'utf-8'))     
    
    conn.close()
    return on_cycle, cycle_period, blue_led_level, red_led_level, manual_overide, t_hr, t_min

def sendData():
    conn = http.client.HTTPConnection("things.ubidots.com", 80, timeout=60)
    headers = {'Content-type': 'application/json',"Connection": "close"}
    json_foo = json.dumps(d)
    conn.request("POST", "/api/v1.6/devices/smart-farm-1/?token=A1E-oBMSdNRG2Z2lkXagXnf16Ho2Hwfond",json_foo,headers)
    r1 = conn.getresponse()
    print('sending data ', r1.status, r1.reason)
    conn.close()
    
def sendUpdateConfirmation():
    conn = http.client.HTTPConnection("things.ubidots.com", 80, timeout=60)
    headers = {'Content-type': 'application/json',"Connection": "close"}
    foo = {'manual-overide': 0}
    json_foo1 = json.dumps(foo)
    conn.request("POST", "/api/v1.6/devices/smart-farm-1/?token=A1E-oBMSdNRG2Z2lkXagXnf16Ho2Hwfond",json_foo1,headers)
    r1= conn.getresponse()
    print('sending update ', r1.status, r1.reason)
    conn.close()

def uploading(dbpath):
    with open(imagepath, 'rb') as f:
        print("Uploading to Dropbox...")
        try:
            dbx.files_upload(f.read(), dbpath, mode=WriteMode('overwrite'))
        except ApiError as err:
            # This checks for the specific error where a user doesn't have
            # enough Dropbox space quota to upload this file
            if (err.error.is_path() and
                    err.error.get_path().error.is_insufficient_space()):
                sys.exit("ERROR: Cannot back up; insufficient space.")
            elif err.user_message_text:
                print(err.user_message_text)
                sys.exit()
            else:
                print(err)
                sys.exit()
#    
#def deleteValues(id):
#    conn = http.client.HTTPConnection("things.ubidots.com", 80, timeout=60)
#    conn.request("DELETE", "/api/v1.6/variables/"+str(id)+"/values/0/1510124400000/?token=A1E-oBMSdNRG2Z2lkXagXnf16Ho2Hwfond")
#    r1 = conn.getresponse()
#    print(r1.status, r1.reason)
#    
#def getVarList():
#    conn = http.client.HTTPConnection("things.ubidots.com", 80, timeout=60)
#    conn.request("GET", "/api/v1.6/datasources/59ed03a2c03f9757233617d8/variables?token=A1E-oBMSdNRG2Z2lkXagXnf16Ho2Hwfond")
#    r1 = conn.getresponse()
#    a = json.loads(r1.read())
#    print(r1.status, r1.reason)   
#    return a
#
#for i in a["results"]:
#    deleteValues(i["id"])
#    time.sleep(1)

# Software SPI configuration:
##CLK  = 18     #Vdd and Vref to 3.3V
##MISO = 23     #AGND & DGND to GND
##MOSI = 24      #MISO and MOSI of RPi respectively to Dout and Din
##CS   = 25      #CLK to RPi Pin 23(CLK) and CS to RPi 24 (CE0)
##mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)


##-------Load Cell--------##
###DT - P05(on the cobbler)
###SCK - P06(on the cobbler)
###Red = E+
###black =E-
###Green = a-
###white = a+
import csv
#####write header for csv
with open('/home/pi/Desktop/data.csv', "w", newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    header = 'time','ms0','ms1','ms2','ms3','ms4','ms5','avg_basin1','avg_basin2','avg_basin3',\
    'ppfdred0','ppfdblue0','ppfd0',\
    'ppfdred1','ppfdblue1','ppfd1',\
    'ppfdred2','ppfdblue2','ppfd2',\
    'ppfdred3','ppfdblue3','ppfd3',\
    'ppfdred4','ppfdblue4','ppfd4',\
    'ppfdred5','ppfdblue5','ppfd5',\
    'temp','humd'
    writer.writerow(header)

def writecsv(data):
    with open('C:/Users/Brian/Desktop/25102017/try.csv', "a", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=' ')
        writer.writerow(data)

####function definition for load cell
def cleanAndExit():
    print("Cleaning...")
    GPIO.cleanup()
    print("Bye!")
    sys.exit()

def getWeight():
    # I've found out that, for some reason, the order of the bytes is not always the same between versions of python, numpy and the hx711 itself.
    # Still need to figure out why does it change.
    # If you're experiencing super random values, change these values to MSB or LSB until to get more stable values.
    # There is some code below to debug and log the order of the bits and the bytes.
    # The first parameter is the order in which the bytes are used to build the "int" value.
    # The second paramter is the order of the bits inside each byte.
    # According to the HX711 Datasheet, the second parameter is MSB so you shouldn't need to modify it.
    hx1.set_reading_format("LSB", "MSB")
    hx2.set_reading_format("LSB", "MSB")
    # HOW TO CALCULATE THE REFFERENCE UNIT
    # To set the reference unit to 1. Put 1kg on your sensor or anything you have and know exactly how much it weights.
    # In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
    # and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
    # If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.
    #hx.set_reference_unit(113)
    hx1.set_reference_unit(103.475)
    hx2.set_reference_unit(105.125)
#    hx1.reset()
#    hx1.tare()
#    hx2.reset()
#    hx2.tare()

    while True:
        try:
            # These three lines are usefull to debug wether to use MSB or LSB in the reading formats
            # for the first parameter of "hx.set_reading_format("LSB", "MSB")".
            # Comment the two lines "val = hx.get_weight(5)" and "print val" and uncomment the three lines to see what it prints.
            #np_arr8_string = hx.get_np_arr8_string()
            #binary_string = hx.get_binary_string()
            #print binary_string + " " + np_arr8_string
            
            # Prints the weight. Comment if you're debbuging the MSB and LSB issue.
            val1 = hx1.get_weight(5)
            val2 = hx2.get_weight(5)
            print('val1:',val1, ' ','val2:',val2)
            
            hx1.power_down()
            hx1.power_up()
            hx2.power_down()
            hx2.power_up()
            time.sleep(0.5)
            
            return val1,val2
            
        except (KeyboardInterrupt, SystemExit):
                print('failed')
                cleanAndExit()


#### function definition for moisture sensor
def monitoring():
    GPIO.setup(29, GPIO.OUT)   #BCM no. to connect to Pump   

    #moisturevalues is the list of moisture from 0-1023
    
    moistsensor0=mcp.read_adc(0)#Check which 2 moisture are together, and find the average
    moistsensor1=mcp.read_adc(1)
    moistsensor2=mcp.read_adc(2)
    moistsensor3=mcp.read_adc(3)
    moistsensor4=mcp.read_adc(4)
    moistsensor5=mcp.read_adc(5)
#    moistsensor6=mcp.read_adc(6)
#    moistsensor7=mcp.read_adc(7)
    avg_moist_basin1 = (moistsensor2+moistsensor5)/2
    avg_moist_basin2 = (moistsensor0+moistsensor4)/2
    avg_moist_basin3 = (moistsensor1+moistsensor3)/2
    
    print (moistsensor0," | ",moistsensor1," | ",moistsensor2," | ",moistsensor3," | ",moistsensor4," | ",moistsensor5," | ")

    return moistsensor0,moistsensor1,moistsensor2,moistsensor3,moistsensor4,moistsensor5,avg_moist_basin1,avg_moist_basin2,avg_moist_basin3        

#######function definition for rgb sensor
def checkid():
    if bus.read_byte_data(address,0x00)==125:     #device indentiy is 0x7D == 125 in decimal
        print('Device Indentified')
    

def reset():
    bus.write_byte_data(address,0,0x46)      ##write 0x46 to 0x00 to reset
    time.sleep(0.1)
    reset_value= bus.read_byte_data(address,0x01)
    reset_value|=bus.read_byte_data(address,0x02)
    reset_value|=bus.read_byte_data(address,0x03)
    reset_value|=bus.read_byte_data(address,0x08)
    if reset_value== 0:
        print('reset successful')
    else:
        print('resetting')
        return reset()

def reconfig():
    bus.write_byte_data(address,1,0x0D)         ##config for rgb mode and high luxoutput (1101) 
    time.sleep(0.1)
    bus.write_byte_data(address,2,0x3F)         ##config for IR rejection
    time.sleep(0.1)
    bus.write_byte_data(address,3,0x00)         #config for threshold interupts
    time.sleep(0.1)
    config_value_1 = bus.read_byte_data(address,0x01)
    config_value_2 = bus.read_byte_data(address,0x02)
    config_value_3 = bus.read_byte_data(address,0x03)
    print(config_value_1,config_value_2,config_value_3)
    if (config_value_1== 13) and (config_value_2==63) and (config_value_3==0):
        print('config successful')
    else:
        print('reconfig')
        return reconfig()

###s0,s1,s2,s3 --> (0000) --> 0, (0001) --> 1, 0100 – 2, 1100 – 3  
def sel_light(d,c,b,a):    
    GPIO.setmode(GPIO.BCM) #follow the numbering on the T-cobbler
    GPIO.setup(s3, GPIO.OUT)   #S3
    GPIO.setup(s2, GPIO.OUT)    #S2
    GPIO.setup(s1, GPIO.OUT)    #S1
    GPIO.setup(s0, GPIO.OUT)
    GPIO.output(s0,a)
    GPIO.output(s1,b)
    GPIO.output(s2,c)
    GPIO.output(s3,d)
    time.sleep(0.1)
    green_long_1 = bus.read_byte_data(address,0x09)   #low
    green_long_2 = bus.read_byte_data(address,0x0A)   #high
    red_long_1 = bus.read_byte_data(address,0x0B)     #low
    red_long_2 = bus.read_byte_data(address,0x0C)     #high
    blue_long_1 = bus.read_byte_data(address,0x0D)    #low
    blue_long_2 = bus.read_byte_data(address,0x0E)    #high
    red0 = red_long_2*256+red_long_1
    blue0 = blue_long_2*256+blue_long_1
    green0 = green_long_2*256+green_long_1
    PPFD_total0 = max(0,int((0.0038*(float(red0)-5.6364)) + (0.0059*float(((green0) - (0.1065*(red0)-87.339))) -5.8711))) #PPFD1 + PPFD2
    PPFD_Red0 = max(0,int((0.0038*(float(red0)-5.6364))))
    PPFD_Blue0 = max(0,int(0.0059*float(((green0) - (0.1065*(red0)-87.339))) -5.8711))
    print ("RGB 1 - Red:",red0," | ","Blue:",blue0," | ","Green:"," | ",green0,"\n","PPFD:"," | ",PPFD_total0)
    return PPFD_Red0, PPFD_Blue0, PPFD_total0
    
######function defination for DHT
pin = 26 ## Pin for DHT Sensor
sensor = Adafruit_DHT.DHT22
def getDHTreading():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        return temperature, humidity
    else:
        print('Failed to get reading. Try again!')


######initialization 

s3=5   ###for light define multiplexer pins
s2=6
s1=13
s0=19

GPIO.setmode(GPIO.BCM) #GPIO setup
GPIO.setup(s3, GPIO.OUT)   #S3
GPIO.setup(s2, GPIO.OUT)    #S2
GPIO.setup(s1, GPIO.OUT)    #S1
GPIO.setup(s0, GPIO.OUT)    #S0

bus=smbus.SMBus(1) #for i2c RBG Sensor, to read 1st ic2 bus
address = 0x44   # For i2c Light Sensor
try:          
    sel_light(0,0,0,0)             
    checkid()    
    reset()
    reconfig()
    sel_light(0,0,0,1)
    checkid()    
    reset()
    reconfig()
    sel_light(0,0,1,0)
    checkid()
    reset()
    reconfig()
    sel_light(0,0,1,1)
    checkid()    
    reset()
    reconfig()
    sel_light(0,1,0,0)
    checkid()    
    reset()
    reconfig()
    sel_light(0,1,0,1)
    checkid()    
    reset()
    reconfig()
    CYR = -0.08819218
    CYG = -0.135497
    CYB = 0.6051979

except OSError:
    print ("Identified OSError")
    pass

hx1 = HX711(5, 6)                   ####for weight
print('s1 done')
hx2 = HX711(13, 6)
print('s2 done')

# Hardware SPI configuration:       ###for soil moisuture
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

pin = 26                                 ## Pin for DHT Sensor   
sensor = Adafruit_DHT.DHT22

#######define working functions
GPIO.setup(20,GPIO.OUT)  #for Red
lightingb = GPIO.PWM(20,120)

GPIO.setup(21,GPIO.OUT)  #for Red
lightingr = GPIO.PWM(21,120)

lightingr.start(100) #Duty Cycle turn down light
lightingb.start(100)

GPIO.setup(16,GPIO.OUT)
GPIO.output(16,0)              
    

############################# define variables
tlastread=0
tlastcheck=0
tlastpic = 0
tlastsend = 0
ppfdred0, ppfdblue0, ppfd0 = 0,0,0
ppfdred1, ppfdblue1, ppfd1 = 0,0,0
ppfdred2, ppfdblue2, ppfd2 = 0,0,0
ppfdred3, ppfdblue3, ppfd3 = 0,0,0
ppfdred4, ppfdblue4, ppfd4 = 0,0,0
ppfdred5, ppfdblue5, ppfd5 = 0,0,0
ms0,ms1,ms2,ms3,ms4,ms5,avg_basin1,avg_basin2,avg_basin3 = 0,0,0,0,0,0,0,0,0
temp, humd = 0,0
on_time = datetime.datetime(2017,11,5,8,0).timestamp()
off_time = 0
oncycle = 12
period = 24
cycle_state = 0
watering_state = 0
blue_led_level = 0
red_led_level = 0
manual_overide = 0
t_hr = 0
t_min =0


####start of loop
while 1:
    now = datetime.datetime.now()
    if time.time()-tlastcheck> 1* 60:   ## check server for settings every 5mins 
        try:
            oncycle, period, blue_led_level, red_led_level, manual_overide, t_hr, t_min = getData()
        except:
            pass
        tlastcheck = time.time()
        
    if manual_overide == 1 and period>=oncycle:
        cycle_state = 1                 ####start on cycle immediately
        on_time = datetime.datetime(now.year,now.month,now.day,int(t_hr),int(t_min)).timestamp()
        off_time = (on_time + oncycle*60*60)   ###find next off time by converting seconds
        sendUpdateConfirmation()
        manual_overide = 0
    
    if time.time()-tlastread > 5*60:
        try:
            ms0,ms1,ms2,ms3,ms4,ms5,avg_basin1,avg_basin2,avg_basin3 = monitoring()    #Returns 8 values, moistsensor0,moistsensor1,moistsensor2,.....
            try:
                ppfdred0, ppfdblue0, ppfd0 = sel_light(0,0,0,0)  #~Returns 4 output each red0,blue0,green0,PPFD0  -->need to map from out data from excel
            except:
                ppfdred0, ppfdblue0, ppfd0 = None, None, None
            try:    
                ppfdred1, ppfdblue1, ppfd1 = sel_light(0,0,0,1)  
            except:
                ppfdred1, ppfdblue1, ppfd1 = None, None, None
            try:
                ppfdred2, ppfdblue2, ppfd2 = sel_light(0,0,1,0)
            except:
                ppfdred2, ppfdblue2, ppfd2 = None, None, None
            try:    
                ppfdred3, ppfdblue3, ppfd3 = sel_light(0,0,1,1)
            except:
                ppfdred3, ppfdblue3, ppfd3 = None, None, None
            try:
                ppfdred4, ppfdblue4, ppfd4 = sel_light(0,1,0,0)
            except:
                ppfdred4, ppfdblue4, ppfd4 = None, None, None
            try:
                ppfdred5, ppfdblue5, ppfd5 = sel_light(0,1,0,1)
            except:
                ppfdred5, ppfdblue5, ppfd5 = None, None, None

            now = datetime.datetime.now()
            temp,humd = getDHTreading() #returns temperature and humidity
#           getweight()   #returns val1 and val2 for 2 load cell
            data = str(now.strftime("%d-%m-%y %H:%M"))+','+\
            str(ms0)+','+str(ms1)+','+str(ms2)+','+str(ms3)+','+str(ms4)+','+str(ms5)+','+str(avg_basin1)+','+str(avg_basin2)+','+str(avg_basin3)+','+\
            str(ppfdred0)+','+str(ppfdblue0)+','+ str(ppfd0)+','+\
            str(ppfdred1)+','+str(ppfdblue1)+','+ str(ppfd1)+','+\
            str(ppfdred2)+','+str(ppfdblue2)+','+ str(ppfd2)+','+\
            str(ppfdred3)+','+str(ppfdblue3)+','+ str(ppfd3)+','+\
            str(ppfdred4)+','+str(ppfdblue4)+','+ str(ppfd4)+','+\
            str(ppfdred5)+','+str(ppfdblue5)+','+ str(ppfd5)+','+\
            str(temp)+','+str(humd)+','+'\n'
    
            with open('/home/pi/Desktop/data.csv','a',newline = '') as file:
                file.write(data)
                file.close()
                
                print ("file written")
                tlastread = time.time()
        except OSError:
            print ("OSError Occurred")
            tlastread = time.time()
            pass
            
    
    if now.hour==8 and now.minute==1 and watering_state == 0:
        #print('go time')
        watering_state = 1
    if watering_state == 1 and (avg_basin1>700 or avg_basin2>700 or avg_basin3>700):   
        GPIO.output(16,1)
        ms0,ms1,ms2,ms3,ms4,ms5,avg_basin1,avg_basin2,avg_basin3 = monitoring()
        
    if watering_state == 1 and avg_basin1<=700 and avg_basin2<=700 and avg_basin3<=700:
        #print('stop')
        GPIO.output(16,0)
        watering_state = 0
    
    if cycle_state == 0 and time.time()>=on_time and on_time!=off_time:
        #print('switch on')
        cycle_state =1
        off_time = (on_time + oncycle*60*60) 

    if cycle_state == 1 and time.time()<off_time and time.time()>on_time:  ###on stage
        #print('set pwm high')
        lightingr.start(100-red_led_level) #Duty Cycle
        lightingb.start(100-blue_led_level) #Duty 
    
    if cycle_state == 1 and time.time()>=off_time:
        #print('switch off')
        cycle_state = 0
        on_time = off_time + (period-oncycle)*60*60
     
    if cycle_state == 0 and time.time()<on_time and time.time()>off_time:
        #rint('set pwm low')
        lightingr.start(100) #Duty Cycle turn down light
        lightingb.start(100)     
    
    if cycle_state ==1  and time.time()<on_time and time.time()<off_time:
        lightingr.start(100) #Duty Cycle turn down light
        lightingb.start(100) 
    
    if time.time() - tlastsend > 5*60:   
        ### insert measurements
        
        ##fill in data dictionary
        if ppfdblue0 != None and ppfdblue1 != None and ppfdblue2 != None and ppfdblue3 != None and ppfdblue4 != None and ppfdblue5!= None:
            d["avg-blue-ppfd"] = np.mean([ppfdblue0,ppfdblue1,ppfdblue2,ppfdblue3,ppfdblue4,ppfdblue5])
        if ppfdred0 != None and ppfdred1 != None and ppfdred2 != None and ppfdred3 != None and ppfdred4 != None and ppfdred5!= None:
            d["avg-red-ppfd"] = np.mean([ppfdred0,ppfdred1,ppfdred2,ppfdred3,ppfdred4,ppfdred5])
        d["humidity"] = humd
        d["temperature"] = temp
        if ppfd4 != None:
            d["light-sensor-1"] = ppfd4                 ##sensor position not decided --> planned to draw a colored html table to show light intensity
        if ppfd1 != None:
            d["light-sensor-2"] = ppfd1
        if ppfd3 != None:
            d["light-sensor-3"] = ppfd3
        if ppfd5 != None:
            d["light-sensor-4"] = ppfd5
        if ppfd2 != None:
            d["light-sensor-5"] = ppfd2
        if ppfd0 != None:
            d["light-sensor-6"] = ppfd0
        d["soil-moisture-1"] = avg_basin1
        d["soil-moisture-2"] = avg_basin2
        d["soil-moisture-3"] = avg_basin3
        try:
            sendData()
        except:
            print("senddata failed")
            pass
        print('data sent')
        tlastsend = time.time()

    if time.time()- tlastpic >5*60 :
        cam = picamera.PiCamera()
        cam.resolution = (640,480)
        cam.capture("/home/pi/Desktop/now.jpg")
        cam.close()
        dbpath1 = '/'+str(round(time.time()))+'.jpg'
        try:
            uploading(dbpath1)
            uploading(dbpath2)
        except:
            print("upload failed")
            pass
        print("upload done")
        tlastpic = time.time()
        
        

        

            
    
    
