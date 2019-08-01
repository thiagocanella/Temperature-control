import time
import datetime 
import platform
import os
import math
from shutil import copyfile
import fuzzyprocess as fuzzyproc 

tgt = 50

ts = time.time()
stamp = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H-%M-%S')


logFileName = 'simulado ' + stamp + '.log'
fileLog = open (logFileName, 'at') 
fileLog.write("TEMPERATURA TRIAC COOLER WINDOW\n")

iteration = 0
while iteration < 1000:
    triac = fuzzyproc.calcularSaida(float(iteration/10), tgt , 1)
    cooler = fuzzyproc.calcularSaida(float(iteration/10), tgt , 2)
    portinhola = fuzzyproc.calcularSaida(float(iteration/10), tgt , 3)
    textOut = str( str(triac) + " " + str(cooler) + " " + str(portinhola) )
    texto = str(float(iteration /10)) + " "+ str(textOut)
    fileLog.write(texto + '\n')

    iteration = iteration + 1