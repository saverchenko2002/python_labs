import numpy as np

if __name__ != "__main__":
    size = 15
    matrix = np.zeros((size, size), dtype='int64')
    matrix[0, 1] = 1
    matrix[0, 5] = 1
    matrix[0, 8] = 1
    matrix[0, 12] = 1
    matrix[0, 14] = 1

    matrix[3, 1] = 1
    matrix[3, 5] = 1
    matrix[3, 8] = 1
    matrix[3, 10] = 1
    matrix[3, 12] = 1
    matrix[3, 14] = 1

    matrix[7, 3] = 1
    matrix[7, 5] = 1
    matrix[7, 10] = 1
    matrix[7, 14] = 1

    matrix[8, 5] = 1

    matrix[10, 1] = 1
    matrix[10, 3] = 1
    matrix[10, 5] = 1
    matrix[10, 14] = 1

    matrix[11, 2] = 1
    matrix[11, 10] = 1
    matrix[11, 12] = 1

    matrix[12, 1] = 1
    matrix[12, 5] = 1
    matrix[12, 8] = 1

    matrix[14, 8] = 1
    matrix[14, 12] = 1
