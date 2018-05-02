'''
Code by Cody Ethan Jordan, script to collect data from Arduino for introductory lab about friction and data analysis
Lab activities and details at http://codyethanjordan.com/physics/fidgetSpinnerLab/
Code hosted at https://github.com/CodyEthanJordan/FidgetSpinnerLab
'''

import serial
import time
import msvcrt
import sys
import argparse
import serial.tools.list_ports
import matplotlib.pyplot as plt
from collections import deque

defaultBaudrate = 74880
#NOTE: this baud rate must match that which is set by the Arduino code and running on the board

def collectData(filename, port, baudRate, livePlot):
    # attempt automatic detection of connected arduino device
    if port == None:
        print('No port specified, attempting to locate port automatically')
        connectedDevices = list(serial.tools.list_ports.comports())
        arduinosConnected = [portInfo for portInfo in connectedDevices 
                             if 'Arduino' in portInfo[1] ] #TODO: improve detection scheme via regex and VID matching for offbrand Arduinos
        if len(arduinosConnected) == 0:
            print('Cannot automatically detect connected Arduino, check connections and specify port via --port option')
            print('The following devices are connected')
            for portInfo in connectedDevices:
                print(portInfo[0] + '   ' + portInfo[1])
            sys.exit(1)
        elif len(arduinosConnected) > 1:
            print('Multiple Arduinos connected, specify one via --port option')
            sys.exit(1)
        else:
            port = arduinosConnected[0][0]
            print('Arduino detected on ' + port)


    samples = deque([])

    done = False
    with serial.Serial("COM4", baudRate) as ser:
        print('Starting data recording - press any key to end')

        if livePlot:
            plt.ion()
            fig = plt.figure()
            ax = fig.add_subplot(111)
            line1, = ax.plot([], 'r-') # Returns a tuple of line objects, thus the comma

        while not done:
            if msvcrt.kbhit():
                done = True
            while ser.inWaiting() > 0:
                input = ser.readline()
                try:
                    nextValue = int(input)
                    samples.append(nextValue)
                except ValueError:
                    nextValue = None

            if livePlot:
                line1.set_xdata(range(len(samples)))
                line1.set_ydata(samples)
                ax.relim()
                ax.autoscale_view()
                fig.canvas.draw()
                fig.canvas.flush_events()


    print("Done, writing to " + filename)

    with open(filename, 'w') as outFile:
        for d in samples:
            outFile.write(str(d) + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Reading in filename for data.')
    parser.add_argument('--port', action='store', dest='port',
                        help='Specify what port to pull serial data from, if unset attempts to automatically locate an Arduino')
    parser.add_argument('--baudRate', action='store', dest='baudRate', type=int, default=defaultBaudrate,
                        help='Baud rate to read data at, set by Arduino script running on the board')
    parser.add_argument('--livePlot', action="store_true", default=False,
                        help='If set will plot data as it comes in')
    parser.add_argument('filename', action="store",
                        help='File to store data in')
    namespace = parser.parse_args()
    print('Writing data to ' + namespace.filename)
    collectData(namespace.filename, namespace.port, namespace.baudRate, namespace.livePlot)

