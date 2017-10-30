# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 00:03:44 2017

@author: lorky
"""

from ubidots import ApiClient
import random
import time
from datetime import datetime

tlastsend = 0

#Ubidots variable list
print('linking variables')

#temperature = api.get_variable("59ed0454c03f97569e7986ee")
#humidity = api.get_variable("59ed71ffc03f974402f76f01")
#leaf_area1 = api.get_variable("59f20787c03f9759434fbb8b")
#leaf_area2 = api.get_variable("59f207a5c03f975981b96312")
#light_sen1 = api.get_variable("59ed7173c03f97431c4e0c1e")
#light_sen2 = api.get_variable("59ed718bc03f97427e01d1d3")
#light_sen3 = api.get_variable("59ed7192c03f9743363bd39d")
#light_sen4 = api.get_variable("59ed71bac03f9743363bd3a2")
#light_sen5 = api.get_variable("59f20110c03f974e52341e0d")
#light_sen6 = api.get_variable("59f20122c03f974e3922f7f1")
#weight1 = api.get_variable("59ed7309c03f97446655eee1")
#weight2 = api.get_variable("59ed731ec03f9744bda90073")
#weight3 = api.get_variable("59ed732cc03f97444993ce21")
#s_moist1 = api.get_variable("59ed70fbc03f97431c4e0c14")
#s_moist2 = api.get_variable("59ed7112c03f97429b5fba37")
#s_moist3 = api.get_variable("59ed711fc03f9743363bd387")
#avg_red_ppfd = api.get_variable("59f2101fc03f97671b61efac")
#avg_blue_ppfd = api.get_variable("59f21035c03f97667e977ef0")
#        
#blue_level = api.get_variable("59ed72b1c03f974402f76f19")
#red_level = api.get_variable("59ed72a3c03f97446655eed3")
#on_cycle = api.get_variable("59ed575ac03f972b1414fb30")
#period = api.get_variable("59ed6fb0c03f9740d1c3e48d")
#
#m_override = api.get_variable("59ed72c4c03f97446655eed6")
#
#red_level_setting = 0
#blue_level_setting = 0
#on_cycle_setting = 0
#period_setting = 0
#
#print('variables link done')
#
red_level_setting = 0 
blue_level_setting = 0
on_cycle_setting = 0
period_setting = 0

#blue_level = api.get_variable("59ed72b1c03f974402f76f19")
#time.sleep(0.1)
#red_level = api.get_variable("59ed72a3c03f97446655eed3")
#time.sleep(0.1)
#on_cycle = api.get_variable("59ed575ac03f972b1414fb30")
#time.sleep(0.1)
#period = api.get_variable("59ed6fb0c03f9740d1c3e48d")
#time.sleep(0.1)


def getsettings():
    print('start')
    api = ApiClient(token="A1E-oBMSdNRG2Z2lkXagXnf16Ho2Hwfond")
    red_level=api.get_variable("59ed72b1c03f974402f76f19")
    time.sleep(0.1)
    blue_level=api.get_variable("59ed72a3c03f97446655eed3")
    time.sleep(0.1)
    on_cycle=api.get_variable("59ed575ac03f972b1414fb30")
    time.sleep(0.1)
    period=api.get_variable("59ed6fb0c03f9740d1c3e48d")
    time.sleep(0.1)
    red_level_setting = red_level.get_values(1)[0]['value']
    blue_level_setting = blue_level.get_values(1)[0]['value']
    on_cycle_setting = on_cycle.get_values(1)[0]['value']
    period_setting = period.get_values(1)[0]['value']
    print('red:',red_level_setting,'blue:',blue_level_setting,'on:',on_cycle_setting)
    return(red_level_setting,blue_level_setting,on_cycle_setting,period_setting)

while 1:
    if time.time()-tlastsend > 20:
        print('into')
        red_level_setting,blue_level_setting,on_cycle_setting,period_setting = getsettings()
        print('cred:',red_level_setting,'blue:',blue_level_setting,'on:',on_cycle_setting)
        tlastsend = time.time()
        
        #Here is where you usually put the code to capture the data, either through your GPIO pins or as a calculation.We'll simply put a random value here:
        
#        #Write the value to your variable in Ubidots
#        temperature.save_value({'value':25+(0.1*random.randint(-10,10))})
#        humidity.save_value({'value':95})
#        leaf_area1.save_value({'value':100+(0.1*random.randint(-10,10))})
#        leaf_area2.save_value({'value':90+(0.1*random.randint(-10,10))})
#        avg_red_ppfd.save_value({'value':120+(0.1*random.randint(-10,10))})
#        avg_blue_ppfd.save_value({'value':100+(0.1*random.randint(-10,10))})
#        weight1.save_value({'value':2+(0.01*random.randint(-100,100))})
#        weight2.save_value({'value':2.1+(0.01*random.randint(-100,100))})
#        weight3.save_value({'value':2.5+(0.01*random.randint(-100,100))})
#        s_moist1.save_value({'value':60+(0.01*random.randint(-100,100))})
#        s_moist2.save_value({'value':60+(0.01*random.randint(-100,100))})
#        s_moist3.save_value({'value':60+(0.01*random.randint(-100,100))})
#        
#        tlastsend = time.time()
#        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) 
        






