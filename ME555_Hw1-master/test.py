import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()

x = [1, 2, 3, 4]
y = [5, 6, 7, 8]

for t in range(10):
    if t == 0:
        points, = ax.plot(x, y, marker='o', linestyle='None')
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
    else:
        new_rx = np.random.randint(10, size=5)
        new_ry = np.random.randint(10, size=5)
        new_tx = new_rx+1
        new_ty = new_ry+1
        points.set_data(new_rx, new_ry)
        points.set_data(new_tx, new_ty)
        #circle2 = plt.Circle((new_rx, new_ry), 2, color='b', fill=False)
        #ax.add_artist(circle2)
        #ax.add_patch(circle2)
    plt.pause(0.5)