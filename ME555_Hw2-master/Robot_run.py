from __future__ import division
import matplotlib.pyplot as plt
import Robot_class
from Robot_class import *
import math
import random
import numpy
import time
import Robot_setting
from Robot_setting import *

#The main function
r_area = 400                                    # The radius of big environment
r_init = 50                                     # The radius of small circle
cir_init = [-200, 200]                          # The position of the small circle
T = 100
Init_plot_map(r_area, r_init, cir_init)         # plot the environment and all the robots
Robot = Init_robot(r_init, cir_init)            # Initialize robots
#Init_plot_robots(Robot, cir_init, r_init)       # plot all the robots
target = [[200, 200], [200, -200], [-200,-200], [-200,200]]
flag_target = 0
pos_target = target[0]
dist_cen2line = []
dist_average = []
plt.xlim((-400, 400))
plt.ylim((-400, 400))

for t in range(T):
    pos_target, flag_target = target_check(Robot, target, pos_target, flag_target)
    #time_start = time.clock()
    Robot, dist_robot2cen, robot_all_x, robot_all_y = Robot_setting.Robot_update(Robot, pos_target)                               #update positions
    #time_elapsed = (time.clock() - time_start)
    #print('All the robotic positions are x', robot_all_x)
    #print('All the robotic positions are y', robot_all_y)
    area = 5  # np.pi * (15 * np.random.rand(N))**2  # 0 to 15 point radii
    #N = 50
    #colors = np.random.rand(N)
    time_start = time.clock()
    scat = plt.scatter(robot_all_x, robot_all_y, s=area, alpha=0.5)
    time_elapsed = (time.clock() - time_start)
    print('The time is', time_elapsed)
    plt.pause(0.001)
    plt.show()
    scat.remove()

    #demo(Robot, r_area, r_init, cir_init)                                                           #show the new positions
