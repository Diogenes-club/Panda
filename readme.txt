Execute Julius(module mode) and receive.py and access http://127.0.0.1:8000/

Panda System

   pin write                               aquestalk
     ↑                 →downlink            ↑                   →GET
arduino(pantilt.ino) =====serial===== raspberry pi(receive.py) =====http===== web browser
     ↑                 ←uplink              ||                   ←POST         ||
   pin read                                  http ↑GET                    Voice streaming server
                                              ||
                                      Julius module mode
example:

downlink
-----------------------
sensor1:1
sensor2:0
gyro:100,150,200
comment:ok


uplink
-----------------------
pan:90
tilt:120
talk:Hello, I am Panda.



GET 127.0.0.1:8000/ajax.json
-----------------------
{"sensor1": "1", "sensor2": "0", "gyro": ["100","150","200"]}


POST 127.0.0.1:8000/post
-----------------------
pan=90&tilt=120&talk=Hello,+I+am+Panda.


Necessary module:
・pySerial
・Chainer
・numpy
