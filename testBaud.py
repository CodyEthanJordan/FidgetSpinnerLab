import numpy as np
import time
import serial
import matplotlib.pyplot as plt

samples = np.array([b'0'])
samples = np.resize(samples, 10000)
deltaT = np.zeros(10000)

with serial.Serial("COM4", 9600) as ser:
    print('Starting test')

    print('Reading out buffer')
    while ser.inWaiting() > 0:
        ser.readline()

    startTime = time.clock()
    t1 = time.clock()
    i = 0
    j = 0
    while time.clock() - startTime < 5:
            deltaT[j] = time.clock() - t1
            j = j + 1
            while ser.inWaiting() < 1:
                pass
            t1 = time.clock()
            while ser.inWaiting() > 0:
                samples[i] = ser.readline()
                i = i + 1

samples = samples[:i]
deltaT = deltaT[:j]
print(len(samples))
print(len(deltaT))
deltaT[0] = deltaT[10]
1/np.mean(deltaT)
np.std(deltaT)

np.max(deltaT)
np.min(deltaT)
np.argmax(deltaT)
np.std(deltaT)
len(deltaT[deltaT > 1e-1])
deltaT[:10]
deltaT
