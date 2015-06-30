import datetime as dt
import os
import socket
import time

import picamera

client_socket = socket.socket()
client_socket.connect((os.environ['PICAMERA_SERVER'], 3141))

connection = client_socket.makefile('wb')
try:
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)
        camera.hflip = True
        camera.vflip = True
        camera.framerate = 5
        camera.annotate_text_size = 16
        camera.start_preview()
        time.sleep(2)
        camera.annotate_background = picamera.Color('black')
        camera.start_recording(connection, format='h264')
        while True:
            camera.annotate_text = (dt.datetime
                                    .now()
                                    .strftime('%Y-%m-%d %H:%M:%S'))
            camera.wait_recording(0.2)
finally:
    connection.close()
    client_socket.close()
