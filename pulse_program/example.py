from pulsesensor import Pulsesensor
import time
import matplotlib.pyplot as plt
import numpy as np

pulse = Pulsesensor()
pulse.startAsyncBPM()
passtime = []
bpm_list = []
x=0
try:
    while True:
        bpm = pulse.BPM
        if bpm > 0:
            print("BPM: %d" % bpm)
        else:
            print("No Heartbeat found")
        x += 1
        passtime.append(x)
        bpm_list.append(bpm)
        x_value = passtime
        y_value = bpm_list
        ax = plt.subplot()
        plt.plot(x_value,y_value,marker="o")
        plt.axis([x-10,x,0,150])
        plt.title("BPM Value")
        plt.xlabel("time /s")
        plt.ylabel("BPM")
        plt.pause(.01) 
        time.sleep(1)
except:
    pulse.stopAsyncBPM()
