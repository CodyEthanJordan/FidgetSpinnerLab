import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import scipy as sy
import scipy.fftpack as syft
from collections import deque
import scipy.optimize as opt
# %% Read in data

def analyzeData(filename):

    inData = deque([])
    with open("data4") as dataFile:
        for d in dataFile:
            try:
                inData.append(int(d[2:5]))
            except:
                pass
    data = np.array(inData)
    plt.plot(data)
    plt.show()

    # %% Find zero crossings
    crossings = []
    zeroPoint = 700
    lastPoint = data[0]
    lastPositive = lastPoint > zeroPoint
    i = 0
    for d in data[1:]:
        if lastPositive and d < zeroPoint:
            x = (lastPoint - zeroPoint)/(d - lastPoint) + i
            crossings.append(x) #update to lerp
        lastPoint = d
        lastPositive = lastPoint >= zeroPoint
        i = i + 1

    crossings = np.array(crossings)
    crossings2 = np.where(np.diff(np.sign(data-zeroPoint)))[0]
    t = np.diff(crossings)
    plt.plot(crossings, zeroPoint + 0*crossings, 'ro', crossings2, zeroPoint + 10+0*crossings2, 'bo', data)
    plt.show()

    # %%
    newT = t[np.append(np.diff(t) < 4000, True)]
    linear = lambda x, a, b: a*x + b
    x = np.array(list(range(len(newT))))
    popt, r = opt.curve_fit(linear, x, 1/newT)
    plt.plot(x,linear(x, *popt))

    plt.plot(1/newT)
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Reading in filename for data.')
    parser.add_argument('filename', action="store")
    namespace = parser.parse_args()

    analyzeData(namespace.filename)
