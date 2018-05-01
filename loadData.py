import numpy as np

def load(filename):
    data = []
    with open(filename) as f:
        data.append(int(f.readline()))

    return np.array(data)
