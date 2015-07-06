# -*- coding:utf-8 -*-
import BaseHTTPServer
import os
import cgi 
import serial
import time
import re
import socket

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_GET(self):
		
		# faviconのリクエストは無視
		if self.path.endswith('favicon.ico'):
			return

		elif self.path.endswith('ajax.json'): 
			jsoncode = "{"
			while not q.empty():
				line = q.get() #キューから取り出す
				if m == re.match(r"(\w+):(\d*)", line):
					jsoncode += '"' + m.group(1) + '": "' + m.group(2) + '", '
				elif  m == re.match(r"(gyro):(\d+),(\d+),(\d+)", line):
					jsoncode += '"' + m.group(1) + '": ["' + m.group(2) + '", "' + m.group(3) + '", "' + m.group(4) + '"], '
			jsoncode += "}"

			#jsoncode = """
#{"sensor1": 1, "sensor2": "0", "gyro": ["33","34","35"]}
#"""
			self.send_response(200)
			self.end_headers()
			self.wfile.write(html)
			return

		elif self.path.endswith('/') or self.path.endswith('index.html'):		
			self.send_response(200)
			self.end_headers()
			f = open("monitor.html")
			response_body = f.read()
			self.wfile.write(response_body)
			return

	def do_POST(self):
		if self.path.endswith('post'):
			form = cgi.FieldStorage(
			fp=self.rfile, 
			headers=self.headers,
			environ={'REQUEST_METHOD':'POST',
					 'CONTENT_TYPE':self.headers['Content-Type'],
					 })
			
			if form.has_key('pan') and (form['pan'].value).isdigit():
				pandeg = int(form['pan'].value)
				if pandeg >= 0 and pandeg <= 180:
					ser = serial.Serial('/dev/ttyACM0', timeout=5.0)
					ser.write('pan:' + form['pan'].value)
					ser.close()
			if form.has_key('tilt') and (form['tilt'].value).isdigit():
				tiltdeg = int(form['tilt'].value)
				if tiltdeg >= 0 and tiltdeg <= 180:
					ser = serial.Serial('/dev/ttyACM0', timeout=5.0)
					ser.write("tilt:" + form['tilt'].value)
					ser.close()
			if form.has_key('talk'):
				os.system('./aquestalkpi/AquesTalkPi "' + form['talk'].value + '" | aplay&')
			self.send_response(200)
			self.end_headers()
			self.wfile.write("ok")

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

def worker2():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('127.0.0.1', 10500))
	while True:
		line = sf.readline().decode('utf-8')
		if line.find(u'おはよう') != -1:
			os.system('./aquestalkpi/AquesTalkPi "おはようございます" | aplay&')

if __name__ == '__main__':
	ser = serial.Serial('/dev/ttyACM0', timeout=5.0)
	q = Queue()
	t = Thread(target=worker)
	t.daemon = True
	t.start()

	server_address = ('', 8000)
	httpd = BaseHTTPServer.HTTPServer(server_address, MyHandler)
	httpd.serve_forever()
