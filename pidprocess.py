
import PID
import time

targetT = 28
P = 10
I = 1
D = 1

pid = PID.PID(P, I, D)
pid.SetPoint = targetT