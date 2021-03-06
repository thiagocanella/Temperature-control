import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

temperarura = ctrl.Antecedent(np.arange(0,100,1), 'temperatura')
temperarura['muito frio'] = fuzz.trimf(temperarura.universe, [0,0,25])
temperarura['frio'] = fuzz.trimf(temperarura.universe, [0,25,50])
temperarura['bom'] = fuzz.trimf(temperarura.universe, [25,50,75])
temperarura['quente'] = fuzz.trimf(temperarura.universe, [50,75,100])
temperarura['muito quente'] = fuzz.trimf(temperarura.universe, [75,100,100])

lampada = ctrl.Consequent(np.arange(0,100,1), 'lampada')
lampada['desligado'] = fuzz.trimf(lampada.universe, [0,0,25])
lampada['bem fraco'] = fuzz.trimf(lampada.universe, [0,25,50])
lampada['fraco'] = fuzz.trimf(lampada.universe, [25,50,75])
lampada['forte'] = fuzz.trimf(lampada.universe, [50,75,100])
lampada['total'] = fuzz.trimf(lampada.universe, [75,100,100])

ventilador = ctrl.Consequent(np.arange(0,100,1), 'ventilador')
ventilador['desligado'] = fuzz.trimf(ventilador.universe, [0,0,50])
ventilador['fraco'] = fuzz.trimf(ventilador.universe, [0,38,75])
ventilador['forte'] = fuzz.trimf(ventilador.universe, [25,63,100])
ventilador['total'] = fuzz.trimf(ventilador.universe, [50,100,100])

portinhola = ctrl.Consequent(np.arange(0,90,1), 'portinhola')
portinhola['fechada'] = fuzz.trimf(portinhola.universe, [0,0,23])
portinhola['pouco aberta'] = fuzz.trimf(portinhola.universe, [0,23,45])
portinhola['pela metade'] = fuzz.trimf(portinhola.universe, [23,45,68])
portinhola['quase aberta'] = fuzz.trimf(portinhola.universe, [45,68,90])
portinhola['aberta'] = fuzz.trimf(portinhola.universe, [68,90,90])

regra1 = ctrl.Rule(temperarura['muito frio'] , ( lampada['total'] , ventilador['desligado'] , portinhola['fechada']) )
regra2 = ctrl.Rule(temperarura['frio'] , ( lampada['fraco'] , ventilador['fraco'] , portinhola['pouco aberta']) )
regra3 = ctrl.Rule(temperarura['bom'] , ( lampada['bem fraco'] , ventilador['forte'] , portinhola['pela metade']) )
regra4 = ctrl.Rule(temperarura['quente'], ( lampada['desligado'] , ventilador['total'] , portinhola['quase aberta']) )
regra5 = ctrl.Rule(temperarura['muito quente'], ( lampada['desligado'] , ventilador['total'] , portinhola['aberta']) )

controleDeSaida = ctrl.ControlSystem([regra1, regra2, regra3, regra4, regra5])

saida = ctrl.ControlSystemSimulation(controleDeSaida)

def calcularSaida(temp,target, match):
    errorby50 = float( 50 - (target - temp))

    saida.input['temperatura'] = errorby50
    saida.compute()
    if match == 1:
        return saida.output['lampada']
    if match == 2:
        return saida.output['ventilador']
    if match == 3:
        return saida.output['portinhola']
    return
    
