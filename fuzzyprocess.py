import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class FuzzyProcessor:
    def __init__(self):
        temperarura = ctrl.Antecedent(np.arange(0,100,1), 'temperatura')
        temperarura['frio'] = fuzz.trapmf(temperarura.universe, [0,0,10,30])
        temperarura['bom'] = fuzz.trimf(temperarura.universe, [10,30,50])
        temperarura['quente'] = fuzz.trapmf(temperarura.universe, [30,50,100,100])

        temperarura.view()