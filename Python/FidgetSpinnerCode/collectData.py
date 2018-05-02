import serial
import time
import msvcrt
import argparse
from collections import deque

def collectData(filename, port, baudRate): 
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
    parser = argparse.ArgumentParser(description='Reading in filename for data.')
    parser.add_argument('--port', action='store', dest='port')
    #NOTE: this baud rate must match that which is set by the Arduino code and running on the board
    parser.add_argument('--baudRate', action='store', dest='baudRate', type=int, default=74880)
    parser.add_argument('filename', action="store")
    namespace = parser.parse_args()
    print('Writing data to ' + namespace.filename)
    collectData(namespace.filename, namespace.port, namespace.baudRate)

