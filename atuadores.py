import time
import serial
import time
import datetime 
import platform
import os
import math
import fuzzyprocess as fuzzyproc 


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

#START PID COMPUTING AREA
def triacPidCalc(pidIn):
    saidainteira = 0
    power = int((255/100)*pidIn)
    if power > 255:
        power = 255

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
    if power > 100:
        power = 100

    if power <= 100 and power > 74:
        saidainteira = 79
    elif power <= 74 and power >49:
        saidainteira = 59
    elif power <= 49 and power >24:
        saidainteira = 39
    else:
        saidainteira = 19
    power = power * 2
    return saidainteira 

def portinholaPidCalc(pidIn):
    saidainteira = 0
    power = 0
    if pidIn > 0:
        return saidainteira
    else:
        power = pidIn - 2*pidIn
    if power > 100:
        power = 100
        
    power = power * 2

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

#END PID COMPUTING ARE


# START FUZZY COMPUTING AREA
def processorFuzzyFuncion(temp, tgt):

    triac = triacFuzzyCalc(fuzzyproc.calcularSaida(temp, tgt , 1))
    cooler = coolerFuzzyCalc(fuzzyproc.calcularSaida(temp, tgt , 2))
    portinhola = portinholaFuzzyCalc(fuzzyproc.calcularSaida(temp, tgt , 3))
    serialOut = encoder(triac, cooler , portinhola)
    arduinoSerialWrite(serialOut)
    textOut = str( str(decodeData(serialOut, 1)) + " " + str(decodeData(serialOut, 2)) + " " + str(decodeData(serialOut, 3)) )
    return textOut

def triacFuzzyCalc(fuzzin):
    power = 0
    power = int((255/100)*fuzzin)
    return power

def coolerFuzzyCalc(fuzzin):
    power = 0
    if fuzzin <= 100 and fuzzin > 74:
        power = 79
    elif fuzzin <= 74 and fuzzin >49:
        power = 59
    elif fuzzin <= 49 and fuzzin >24:
        power = 39
    else:
        power = 19
    return power

def portinholaFuzzyCalc(fuzzin):
    power = 0
    power = int(fuzzin)
    return power

#END FUZZY COMPUTING AREA


def arduinoSerialWrite(dataIn):
    byteout = bytes(dataIn,  encoding="ascii")
    ser.write(byteout)

