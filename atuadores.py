import time
import serial
import time
import datetime 
import platform
import os
import math

ts = time.time()
#CONFIGURAÇÕES DE PORTA COM E FORMATO DE DATA/HORA PELO SISTEMA OPERACIONAL
if platform.system() == "Windows":
    ser = serial.Serial('COM15', 9600, timeout=0)
    stamp = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H-%M-%S')
if platform.system() == "Linux":
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    stamp = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')



#FUNÇÕES CONVERSORAS

def encoder(triac, cooler, portinhola):
    outputEncoded = str((triac * 1000000) + ( cooler * 1000) + portinhola)
    return outputEncoded

def decodeData(encodedInt , match):
    encodedInt = int(encodedInt)
    triacValue = int(encodedInt / 1000000)
    coolerValue = int((encodedInt - (triacValue * 1000000) ) / 1000)
    portinholaValue = (encodedInt - ( (triacValue * 1000000) + (coolerValue * 1000) )   )
    if match == 1: 
        return triacValue
    if match == 2: 
        return coolerValue
    if match == 3: 
        return portinholaValue
    return 0


def triacPidCalc(pidIn):
    saidainteira = 0
    power = int((255/100)*pidIn)
    if power < 0:
        saidainteira = 0
    else:
        saidainteira = power
    return saidainteira

def coolerPidCalc(pidIn):
    saidainteira = 0
    power = 0
    if pidIn > 0:
        return saidainteira
    else:
        power = pidIn - 2*pidIn

    if power <= 100 and power > 74:
        saidainteira = 79
    elif power <= 74 and power >49:
        saidainteira = 59
    elif power <= 49 and power >24:
        saidainteira = 39
    else:
        saidainteira = 19

    return saidainteira 

def portinholaPidCalc(pidIn):
    saidainteira = 0
    power = 0
    if pidIn > 0:
        return saidainteira
    else:
        power = pidIn - 2*pidIn
    
    saidainteira = int(float(power /100) * 45)

    return saidainteira


def processorFuncion(pidResult):
   
    triac = triacPidCalc(pidResult)
    cooler = coolerPidCalc(pidResult)
    portinhola = portinholaPidCalc(pidResult)
    serialOut = encoder(triac, cooler , portinhola)
    arduinoSerialWrite(serialOut)
    textOut = str( str(decodeData(serialOut, 1)) + " " + str(decodeData(serialOut, 2)) + " " + str(decodeData(serialOut, 3)) )
    return textOut

def arduinoSerialWrite(dataIn):
    byteout = bytes(dataIn,  encoding="ascii")
    ser.write(byteout)

