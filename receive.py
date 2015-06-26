# -*- coding:utf-8 -*-
import BaseHTTPServer
import os
#import serial
import time

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        
        # faviconのリクエストは無視
        if self.path.endswith('favicon.ico'):
            return;

        elif self.path.endswith('/'):        
            self.send_response(200)
            self.end_headers()
            f = open("monitor.html")
            response_body = f.read()
            self.wfile.write(response_body)
        elif self.path.endswith('ajax.json'): 
            html = """
{"sensor1": "1", "sensor2": "0"}
"""
            self.wfile.write(html)

server_address = ('', 8000)
httpd = BaseHTTPServer.HTTPServer(server_address, MyHandler)
httpd.serve_forever()
