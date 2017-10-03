#adapted from https://github.com/sparkfun/SparkFun_ISL29125_Breakout_Arduino_Library for raspberry pi

import smbus
import time

tlastread=0
bus=smbus.SMBus(1)
address = 0x44

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

checkid()    
reset()
reconfig()

while 1:
    if time.time()-tlastread > 2:
        green_long_1 = bus.read_byte_data(address,0x09)   #low
        green_long_2 = bus.read_byte_data(address,0x0A)   #high
        red_long_1 = bus.read_byte_data(address,0x0B)     #low
        red_long_2 = bus.read_byte_data(address,0x0C)     #high
        blue_long_1 = bus.read_byte_data(address,0x0D)    #low
        blue_long_2 = bus.read_byte_data(address,0x0E)    #high
        print('red: ',red_long_2*256+red_long_1,' ','blue: ',blue_long_2*256+blue_long_1,' ','green: ',green_long_2*256+green_long_1)
        tlastread = time.time()
        
        