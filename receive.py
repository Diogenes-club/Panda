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

        elif self.path.endswith('ajax.json'): 
            html = """
{"sensor1": "1", "sensor2": "0"}
"""
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

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = BaseHTTPServer.HTTPServer(server_address, MyHandler)
    httpd.serve_forever()
