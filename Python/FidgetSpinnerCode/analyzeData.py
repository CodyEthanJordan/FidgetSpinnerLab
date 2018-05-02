import numpy as np
import matplotlib.pyplot as plt
from collections import deque
import scipy.optimize as opt
import argparse

def findVelocity(data):
    crossings = []
    zeroPoint = np.mean(data)
    crossings = np.where(np.diff(np.sign(data-zeroPoint)))[0]
    period = np.diff(crossings)
    filteredPeriod = period[np.append(np.diff(period) < 4000, True)]
    velocity = 1 / filteredPeriod
    filteredVelocity = velocity[velocity < np.mean(velocity)]
    return filteredVelocity


def analyzeData(filename):
    data = np.loadtxt(filename)

    plt.ion()

    plt.plot(data)
    plt.draw()
    plt.pause(.001)
    
    startData = input("Where does data start? ")
    startData = int(startData)
    data = data[startData:]

    plt.close()
    plt.ioff()
    
    velocity = findVelocity(data[startData:])

    plt.plot(velocity)
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Reading in filename for data.')
    parser.add_argument('filename', action="store",
                        help='Name of file where data is stored')
    namespace = parser.parse_args()

    analyzeData(namespace.filename)
