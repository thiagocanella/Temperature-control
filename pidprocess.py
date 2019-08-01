
import PID
import time

targetT = 28
P = 5
I = 3
D = 1


pid = PID.PID(P, I, D)
pid.SetPoint = targetT