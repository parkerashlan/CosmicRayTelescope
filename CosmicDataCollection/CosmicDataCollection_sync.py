#!/usr/bin/env python3
import os
import sys

import RPi.GPIO as GPIO
import time
import datetime

import getch

#Detect signals on GPIO on pin 11.
GPIO.setmode(GPIO.BOARD)
GPIO.setup(13, GPIO.IN)
GPIO.setup(11, GPIO.IN)
GPIO.setup(12, GPIO.OUT)

#Make text file for data
file = 'CosmicRayData0.txt'

def checkfile(file):
    i = 1
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
        if GPIO.input(13)==1: #and GPIO.input(14)==1:
            NCount = NCount + 1
            date = datetime.datetime.now()
            deadtime = deadtime + 0.1
            print('NCounts:',NCount, end='\r')
            data.write('1 cosmicpi11 %s %s \n'% (NCount,date))
            GPIO.output(12, 1)
            time.sleep(0.1)
            GPIO.output(12, 0)

        if GPIO.input(11)==1:
            data.write('SYNC cosmicpi11 %s %s \n'% (NCount, date))

        if  getch.kbhit():
            if (getch.getch() == True):
                break

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
