import serial
import time
import datetime 
import platform

ts = time.time()
stamp = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
logFileName = stamp + '.txt'

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
if platform.system() == "Linux":
    ser = serial.Serial('/dev/ttyUSB0', 9600)

fileLog = open (logFileName, 'at') 
fileLog.write("TEMP DECISION SECONDS\n")

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