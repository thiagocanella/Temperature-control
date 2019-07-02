import serial
import time
import datetime 
import platform
import os
import math
from shutil import copyfile
import pidprocess
import atuadores
ts = time.time()



#DEFINIÇÕES DO EXPERIMENTO
horasDeExperimento = 4
minutosDeExperimento = 0
#----------------------------






#MONTA ARQUIVO DE LOG
try:
    os.remove('lastplot.plt')
except FileNotFoundError:
    print('')
copyfile('plot.dol','lastplot.plt')
logFileName = atuadores.stamp + '.log'
fileLog = open (logFileName, 'at') 
fileLog.write("TEMP DECISION SECONDS\n")
plotfileInjectLogfile = open ('lastplot.plt','at')
plotfileInjectLogfile.write("plot '"+ logFileName +"' using 3:1, '' using 3:2 \n" + "pause -1" )

def tempoTotalEmSegundos(hora,minuto):
    return (hora * 3600) + (minuto * 60)




iterationCounter = 1

while 1:  

    try:
        #LÊ PORTA SERIAL E CONVERTE A STRING PRA FLOAT
        temp = atuadores.ser.readline()
        leitura = str(temp)[2:7] 
        temperatura = float(leitura)
        pidprocess.pid.update(temperatura)
        print (str(pidprocess.pid.output))
        decisaoOut = atuadores.processorFuncion( int(pidprocess.pid.output) )

        texto = str(leitura) + " "+ str(decisaoOut) +" "+ str(iterationCounter)  
        print (texto)
        fileLog.write(texto + '\n')
        #TOMA DECISÃO ENTRE TEMPERATURAS ESTABELECIDAS E MANDA RESPOSTA SERIAL
       # if temperatura <= minima:
          #  decisao = "Alta"
          #  ser.write(b'H')
        #if temperatura  > minima :
         #   if  temperatura  <= maxima:
        #        decisao = "Baixa"
        #        ser.write(b'L')
        #CRIA TEXTO QUE IMPRIME NO CONSOLE E SALVA NO LOG
        

     
    except:
        print("erro")
          
    iterationCounter = iterationCounter + 1
    time.sleep(1)

    #LIMITADOR DE TEMPO DE EXECUÇÃO DO EXPERIMENTO
    if iterationCounter > tempoTotalEmSegundos(horasDeExperimento,minutosDeExperimento):
        break
