# -*- coding: utf-8 -*-

import os
import serial
import time

ser = serial.Serial('/dev/ttyACM0', timeout=5.0)
while True:
    str = ser.read(1)
    if str == "\n":
        break
    
while True:
    line = ser.readline()
    line = line[:-2] #改行を削る
    
    print line +"debug"
    if line.isdigit():
        value = int(line)
        if value < 200:
            talkstr = "暗いー"
            os.system('./aquestalkpi/AquesTalkPi "' + talkstr + '" | aplay&')

            ser.write("120")
            time.sleep(1)
            ser.write("60")
            time.sleep(1)
            ser.write("120")
            time.sleep(1)
            ser.write("60")
            time.sleep(1)
