import serial
import time
import datetime 
import platform
import os
import math
from shutil import copyfile
ts = time.time()

ser = serial.Serial('COM15', 9600, timeout=2)
dados = 11111111

while 1:  

    try:
        send  = bytes(str(dados),  encoding="ascii")
        ser.write(send) 
        time.sleep(1)
        temp = ser.readline()
        recebido = str(temp)
        print(recebido[2:][:-5])

    except:
        print("erro")

    time.sleep(1)
