from constants_task_2 import *
import matplotlib.pyplot as plt


def location(field):
    position = np.random.randint(0, size - 1), np.random.randint(0, size - 1)
    for i in range(5):
        while field[position] != 0:
            position = np.random.randint(0, size - 1), np.random.randint(0, size - 1)
        towers_field[position] = p1
        towers[i] = position
    for i in range(3):
        while field[position] != 0:
            position = np.random.randint(0, size - 1), np.random.randint(0, size - 1)
        towers_field[position] = p2
        towers[5 + i] = position
    for i in range(2):
        while field[position] != 0:
            position = np.random.randint(0, size - 1), np.random.randint(0, size - 1)
        towers_field[position] = p3
        towers[8 + i] = position


def signal(signal_field, population):
    good_connection = 0
    all_people = 0
    signal_current_point = np.zeros(10)
    for i in range(size):
        for j in range(size):
            all_people += population[i, j]
            for k in range(10):
                if i == towers[k, 0] and j == towers[k, 1]:
                    signal_current_point[k] = towers_field[i, j]
                    continue
                elif k <= 4:
                    signal_current_point[k] = p1 / ((i - towers[k, 0]) ** 2 + (j - towers[k, 1]) ** 2)
                elif 5 <= k <= 7:
                    signal_current_point[k] = p2 / ((i - towers[k, 0]) ** 2 + (j - towers[k, 1]) ** 2)
                elif 8 <= k <= 9:
                    signal_current_point[k] = p3 / ((i - towers[k, 0]) ** 2 + (j - towers[k, 1]) ** 2)
            signal_field[i, j] = max(signal_current_point)
            if signal_field[i][j] >= 1:
                good_connection += population[i, j]
                x.append(j)
                y.append(i)
    return good_connection, all_people


if __name__ == "__main__":
    location(towers_field)
    a = signal(signal_level, density)
    print('Людей с сигналом >=1 {}, всего людей {}'.format(a[0], a[1]))

    figure, ax = plt.subplots(2)
    figure.set_size_inches(6, 12)

    ax[0].scatter(x, y, size, marker='s', color=point_color)

    ax[1].imshow(signal_level, cmap=gradient_color, interpolation='nearest', origin='lower',
                 vmin=0, vmax=p3)
    plt.show()
