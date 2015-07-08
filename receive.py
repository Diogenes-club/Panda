# -*- coding:utf-8 -*-
import BaseHTTPServer
import os
import cgi 
import serial
import re
import socket
import Queue
import threading

isaimode = 0

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_HEAD(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()

	def do_GET(self):
		if self.path == '/ajax.json': 
			jsoncode = "{"
			while not q.empty():
				line = q.get()
				m1 = re.match(r"^(\w+):(\d*)$", line)
				if m1:
					jsoncode += '"' + m1.group(1) + '": "' + m1.group(2) + '", '
				m2 = re.match(r"^(gyro):(\d+),(\d+),(\d+)$", line)
				if m2:
					jsoncode += '"' + m2.group(1) + '": ["' + m2.group(2) + '", "' + m2.group(3) + '", "' + m2.group(4) + '"], '
			jsoncode += "}"

			jsoncode = '{"sensor1": "1", "sensor2": "0", "gyro": ["33","34","35"]}' #testcode
			self.send_response(200)
			self.end_headers()
			self.wfile.write(jsoncode)

		elif self.path == '/' or self.path == '/index.html':
			self.send_response(200)
			self.end_headers()
			f = open("monitor.html")
			response_body = f.read()
			self.wfile.write(response_body)

		else:
			self.send_response(404)
			self.send_header("Content-type", "text/html")
			self.end_headers()
			self.wfile.write("404 Not found")

	def do_POST(self):
		if self.path == '/post':
			form = cgi.FieldStorage(
			fp=self.rfile, 
			headers=self.headers,
			environ={'REQUEST_METHOD':'POST',
					 'CONTENT_TYPE':self.headers['Content-Type'],
					 })

			if form.has_key('aimode') and (form['aimode'].value).isdigit():
				modevalue = int(form['aimode'].value)
				self.send_response(200)
				self.end_headers()
				self.wfile.write("post ok")
				global isaimode
				if modevalue == 0:
					isaimode = 0
					self.wfile.write("\nWirepuller mode")
				elif modevalue == 1:
					isaimode = 1
					self.wfile.write("\nAI mode")
				else:
					self.wfile.write("\ninvalid value") 
				return
			if isaimode == 1:
				self.send_response(200)
				self.end_headers()
				self.wfile.write("AI mode!\nOperation Locked!")
				return

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
				aquestalk(form['talk'].value)
			if form.has_key('nod') and (form['nod'].value).isdigit():
				tiltdeg = int(form['nod'].value)
				if tiltdeg > 0 and nod < 5:
					ser = serial.Serial('/dev/ttyACM0', timeout=5.0)
					ser.write("nod:" + form['nod'].value)
					ser.close()
			if form.has_key('shake') and (form['shake'].value).isdigit():
				tiltdeg = int(form['shake'].value)
				if tiltdeg > 0 and nod < 5:
					ser = serial.Serial('/dev/ttyACM0', timeout=5.0)
					ser.write("shake:" + form['shake'].value)
					ser.close()
			if form.has_key('detach'):
					ser = serial.Serial('/dev/ttyACM0', timeout=5.0)
					ser.write("detach:0")
					ser.close()
			self.send_response(200)
			self.end_headers()
			self.wfile.write("post ok")

def serialread():
	# 最初の1行は途切れている可能性があるので捨てる
	while True:
	#	str = ser.read(1) #
		if str == "\n":
			break

	while True:
	#	line = ser.readline() #
		line = line[:-2] #改行を削る
		q.put(line)

def juliusread():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect(('127.0.0.1', 10500))
	except socket.error:
		print 'julius connect error'
		return

	while True:
		line = sf.readline().decode('utf-8')
		global isaimode
		if isaimode == 0:
			continue
		if line.find(u'おはよう') != -1:
			aquestalk("おはようございます")
		elif  line.find(u'こんにちわ') != -1:
			aquestalk("こんにちわ")

def aquestalk(line):
	os.system('./aquestalkpi/AquesTalkPi "' + line + '" | aplay&')

if __name__ == '__main__':
	#ser = serial.Serial('/dev/ttyACM0', timeout=5.0) #
	q = Queue.Queue()
	t1 = threading.Thread(target=serialread)
	t1.daemon = True
	t1.start()
	t2 = threading.Thread(target=juliusread)
	t2.daemon = True
	t2.start()

	server_address = ('', 8000)
	httpd = BaseHTTPServer.HTTPServer(server_address, MyHandler)
	httpd.serve_forever()
