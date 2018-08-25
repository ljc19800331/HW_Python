import numpy as np
import matplotlib.pyplot as plt
import time
import random
import Robot_setting
from Robot_setting import *

# Fixing random state for reproducibility
np.random.seed(19680801)

N = 50
x = np.random.rand(N)
y = np.random.rand(N)
area = 100
colors = np.random.rand(N)
plt.xlabel('x')         # Set up axes
plt.ylabel('y')
plt.title('ME555 assignment')

# plot the tracking line
r_area = 400                                    # The radius of big environment
r_init = 50                                     # The radius of small circle
cir_init = [-200, 200]                          # The position of the small circle
Init_plot_map(r_area, r_init, cir_init)
x_track = numpy.arange(-200, 200, 1)
y_track = [200] * len(x_track)
y_track_1 = numpy.arange(-200, 200, 1)
x_track_1 = [200] * len(x_track)
target_A = [200, 200]
target_B = [200, -200]
plt.scatter(target_A[0], target_A[1], c='g', marker='o', s=100)
plt.scatter(target_B[0], target_B[1], c='b', marker='o', s=100)
plt.plot(x_track, y_track, 'r')
plt.plot(x_track_1, y_track_1, 'r')

#scat = plt.scatter(x, y, s=area, c=colors, alpha=0.5)
#scat = plt.scatter(x, y, s=area, c=colors, alpha=0.5)

time_start = time.clock()
for i in range(100):
    N = 50
    x = np.random.rand(N)
    y = np.random.rand(N)
    colors = np.random.rand(N)
    area = 100#np.pi * (15 * np.random.rand(N))**2  # 0 to 15 point radii
    scat = plt.scatter(x, y, s=area, c=colors, alpha=0.5)
    plt.pause(0.001)
    plt.show()
    scat.remove()
time_elapsed = (time.clock() - time_start)
print('time_elapsed', time_elapsed)