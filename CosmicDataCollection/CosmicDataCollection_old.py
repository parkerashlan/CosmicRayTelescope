#!/usr/bin/env python3
import os
import sys

import RPi.GPIO as GPIO
import time
import datetime

#Detect signals on GPIO on pin 11.
GPIO.setmode(GPIO.BOARD)
GPIO.setup(13,GPIO.IN)
GPIO.setup(11, GPIO.IN)

#Make text file for data
file = 'CosmicRayData.txt'

def checkfile(file):
    i = 0
    while os.path.isfile(file) == True:
        file = 'CosmicRayData'+str(i)+'.txt'
        i = i+1
        os.path.isfile(file)
    data = open(file, 'w+')
    return data

data = checkfile(file)

#Loop forever checking for a high signal on pin 11
NCount = 0
deadtime = 0
starttime = datetime.datetime.now()

try:
    while True:
        #print('Time Elapsed:',starttime - datetime.datetime.now(), end='\r')
        if GPIO.input(11)==1 and GPIO.input(14)==1:
            NCount = NCount + 1
            date = datetime.datetime.now()
            deadtime = deadtime + 0.1
            print('NCounts:',NCount, end='\r')
            data.write('1 cosmicpi1 %s %s \n'% (NCount,date))
            time.sleep(0.1)

finally:
    endtime = datetime.datetime.now()
    timedifference = endtime - starttime
    nSeconds = timedifference.total_seconds()
    livetime = nSeconds - deadtime
    data.write('Live Time:'+str(livetime)+'\n')
    data.write('Total Time:'+str(nSeconds)+'\n')
    data.write('Dead Time:'+str(NCount/livetime))
    nSeconds = nSeconds - NCount/10
    print('')
    print('Total count=', NCount)
    print('Count rate =', NCount/nSeconds, 'Hz')
    GPIO.cleanup()
