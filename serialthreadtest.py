# -*- coding: utf-8 -*-

import serial
import re

ser = serial.Serial('/dev/ttyACM0', timeout=5.0)
q = Queue()

t = Thread(target=worker)
     t.daemon = True
     t.start()


# シリアル通信を読むスレッド
def worker():
	# 最初の1行は途切れている可能性があるので捨てる
	while True:
    	str = ser.read(1)
    	if str == "\n":
        	break

	while True:
    	line = ser.readline()
    	line = line[:-2] #改行を削る
    	q.put(line) #キューに追加


# JSONコードの生成
jsoncode = "{"
while not q.empty():
    line = q.get() #キューから取り出す
	if m = re.match(r"(\w+):(\d*)", line):
		jsoncode += '"' + m.group(1) + '": "' + m.group(2) + '", '
	elif  m = re.match(r"(gyro):(\d+),(\d+),(\d+)", line):
		jsoncode += '"' + m.group(1) + '": ["' + m.group(2) + '", "' + m.group(3) + '", "' + m.group(4) + '"], '
jsoncode += "}"

