import serial
import time
import datetime 
import platform
import os
import math
from shutil import copyfile
import atuadores
import PID

ts = time.time()



#DEFINIÇÕES DO EXPERIMENTO
horasDeExperimento = 4
minutosDeExperimento = 0
#----------------------------
alvo = 28




#PIDSETUP
P = 5
I = 3
D = 1
pid = PID.PID(P, I, D)
pid.SetPoint = alvo


#MONTA ARQUIVO DE LOG
try:
    os.remove('lastplot.plt')
except FileNotFoundError:
    print('')
copyfile('plot.dol','lastplot.plt')
logFileName = atuadores.stamp + '.log'
fileLog = open (logFileName, 'at') 
fileLog.write("TEMP TRIAC COOLER WINDOW SECONDS\n")
plotfileInjectLogfile = open ('lastplot.plt','at')
plotfileInjectLogfile.write("plot '"+ logFileName +"' using 5:1 \n" + "pause -1" )

def tempoTotalEmSegundos(hora,minuto):
    return (hora * 3600) + (minuto * 60)




iterationCounter = 1

while 1:  

    try:
        #LÊ PORTA SERIAL E CONVERTE A STRING PRA FLOAT
        temp = atuadores.ser.readline()
        leitura = str(temp)[2:7] 
        temperatura = float(leitura)
        #pid.update(temperatura)
        #print ("Decisao do PID " + str(pid.output))
        #decisaoOut = atuadores.processorFuncion( int(pid.output) )

        decisaoOut = atuadores.processorFuzzyFuncion(temperatura, alvo)


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
