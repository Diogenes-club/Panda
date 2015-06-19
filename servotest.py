# -*- coding: utf-8 -*-

import os
import serial

while True:
    strdeg = raw_input("degree?")
    if strdeg.isdigit():
        deg = int(strdeg)
    else:
        talkstr = strdeg
        os.system('./aquestalkpi/AquesTalkPi "' + talkstr + '" | aplay&')
        continue

    if deg >= 0 and deg <= 180:
        ser = serial.Serial('/dev/ttyACM0', timeout=5.0)
        ser.write(strdeg)
        ser.close()
