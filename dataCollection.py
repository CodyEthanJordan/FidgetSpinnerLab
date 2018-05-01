import serial
import time
import msvcrt
from collections import deque

def collectData(filename, baudRate = 1000000):
    samples = deque([])

    done = False
    with serial.Serial("COM4", baudRate) as ser:
        print('Starting data recording - press any key to end')
        while not done:
            if msvcrt.kbhit():
                done = True
            while ser.inWaiting() > 0:
                samples.append(ser.readline())

    print("Done, writing to " + filename)

    with open(filename, 'w') as outFile:
        for d in samples:
            outFile.write(str(d) + '\n')

if __name__ == "__main__":
    collectData("data3")
