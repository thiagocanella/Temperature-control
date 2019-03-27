import serial
import time
import datetime 
import platform
import os
from shutil import copyfile

ts = time.time()

def decisaoParaNumero(decisao):
    if decisao == "Alta":
        return 2
    if decisao == "Baixa":
        return 1
    if decisao == "Nula":
        return 0
    return 0


if platform.system() == "Windows":
    ser = serial.Serial('COM15', 9600, timeout=0)
    stamp = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H-%M-%S')


if platform.system() == "Linux":
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    stamp = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')

try:
    os.remove('lastplot.plt')
except FileNotFoundError:
    print('')

copyfile('plot.dol','lastplot.plt')
logFileName = stamp + '.log'
fileLog = open (logFileName, 'at') 
fileLog.write("TEMP DECISION SECONDS\n")
plotfileInjectLogfile = open ('lastplot.plt','at')
plotfileInjectLogfile.write("plot '"+ logFileName +"' using 3:1, '' using 3:2 \n" + "pause -1" )

minima = 29.60
maxima = 31.00

iterationCounter = 1

while 1:  

    try:
        temp = ser.readline()
        leitura = str(temp)[2:7] 
        temperatura = float(temp)
     
        if temperatura <= minima:
            decisao = "Alta"
            ser.write(b'H')
     
        if temperatura  > minima :
            if  temperatura  <= maxima:
                decisao = "Baixa"
                ser.write(b'L')
                             
        if temperatura > maxima:
            decisao = "Nula"
            ser.write(b'N') 

        decisaoOut = decisaoParaNumero(decisao)
        texto = str(leitura) + " " + str(decisaoOut) + " " + str(iterationCounter)  
        print (texto)
        fileLog.write(texto + '\n')
     
    except:
        print("erro")
          
    iterationCounter = iterationCounter + 1
    time.sleep(1)
