# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 19:08:16 2017

@author: lorky
"""

import smbus
import time

tlastread=0
bus=smbus.SMBus(1)

def readtemp():
    data = bus.read_i2c_block_data(0x48, 0)
    msb = data[0]
    lsb = data[1]
    print (((msb << 8) | lsb) >> 4) * 0.0625 
    
def reset():
    bus.write_byte_data(0x48,0)
    time.sleep(0.1)
    reset_value= bus.read_byte_data(0x48,0x00)
    if reset_value== 0:
        print('reset successful')
    else:
        print('resetting')
        return reset()