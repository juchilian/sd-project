#ラズパイ側で動かすコード
from pulsesensor import Pulsesensor
import time
import socket

pulse = Pulsesensor()
pulse.startAsyncBPM()
passtime = []
bpm_list = []
PORT = 50000
BUFFER_SIZE = 1024
x=0

try:
    while True:
        bpm = pulse.BPM
        if bpm > 0:
#             assign socket as TCP/IP
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#                 connect to IP adress
                s.connect(('192.168.11.7', PORT))
#                 define data as bpm
                data =  str(bpm)
                # send data 
                s.send(data.encode())
                print("BPM: %d" % bpm)

        else:
            print("No Heartbeat found")
            
        time.sleep(1)

except:
    pulse.stopAsyncBPM()