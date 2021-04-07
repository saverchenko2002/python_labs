import numpy as np
import matplotlib.pyplot as plt

if __name__ != "__main__":
    p1 = 100
    p2 = 300
    p3 = 500
    size = 100
    towers = np.zeros((10, 2), dtype='int64')
    towers_field = np.zeros((size, size), dtype='int64')
    signal_level = np.zeros((size, size))
    density = np.random.randint(100, size=(size, size))
    point_color = 'green'
    gradient_color = 'Greys'
    x = list()
    y = list()
