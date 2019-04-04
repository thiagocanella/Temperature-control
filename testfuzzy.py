
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import time

temperarura = ctrl.Antecedent(np.arange(0,100,1), 'temperatura')
temperarura['frio'] = fuzz.trapmf(temperarura.universe, [0,0,25,48])
temperarura['bom'] = fuzz.trimf(temperarura.universe, [38,46,50])
temperarura['quente'] = fuzz.trapmf(temperarura.universe, [46,50,100,100])

temperarura.view()


while 1:
    time.sleep(20)