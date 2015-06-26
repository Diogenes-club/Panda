# -*- coding:utf-8 -*-
import BaseHTTPServer
import os
import cgi 
import serial
import time

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        
        # faviconのリクエストは無視
        if self.path.endswith('favicon.ico'):
            return

        elif self.path.endswith('/'):        
            self.send_response(200)
            self.end_headers()
            f = open("monitor.html")
            response_body = f.read()
            self.wfile.write(response_body)
            return

        elif self.path.endswith('ajax.json'): 
            html = """
{"sensor1": "1", "sensor2": "0"}
"""
            self.wfile.write(html)
        elif self.path.endswith('post'):
            if os.environ['REQUEST_METHOD'] == 'POST':
                data = cgi.FieldStorage()
                if data['pan'].value.isdigit():
                    pandeg = int(data['pan'].value)
                    if pandeg >= 0 and pandeg <= 180:
                        ser = serial.Serial('/dev/ttyACM0', timeout=5.0)
                        ser.write("pan:" + pandeg)
                        ser.close()
                if data['tilt'].value.isdigit():
                    tiltdeg = int(data['tilt'].value)
                    if tiltdeg >= 0 and tiltdeg <= 180:
                        ser = serial.Serial('/dev/ttyACM0', timeout=5.0)
                        ser.write("tilt:" + tiltdeg)
                        ser.close()
                if data['talk'].value
                    os.system('./aquestalkpi/AquesTalkPi "' + data['talk'].value + '" | aplay&')
            self.wfile.write("ok")
            return
server_address = ('', 8000)
httpd = BaseHTTPServer.HTTPServer(server_address, MyHandler)
httpd.serve_forever()
