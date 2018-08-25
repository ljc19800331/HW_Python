import time
import matplotlib.pyplot as plt
import matplotlib
import Robot_class
from Robot_class import *
import random
import numpy as np
import Robot_update
from Robot_update import *
import numpy as np

def plot_init():
    radius = 200
    d_half = 30
    fig, ax = plt.subplots()
    ax.set_title('ME555 Hw3')
    ax.set_xlim([-180, 180])
    ax.set_ylim([-180, 180])
    circle = plt.Circle((0, 0), 50, color='r', fill=False)
    l_1 = matplotlib.lines.Line2D([-radius, radius], [d_half, d_half])
    l_2 = matplotlib.lines.Line2D([-200, 200], [-d_half, -d_half])
    l_3 = matplotlib.lines.Line2D([-d_half, -d_half], [200, -200])
    l_4 = matplotlib.lines.Line2D([d_half, d_half], [200, -200])
    ax.add_artist(circle)
    ax.add_artist(l_1)
    ax.add_artist(l_2)
    ax.add_artist(l_3)
    ax.add_artist(l_4)
    return ax

def plot(Robots,ax):
    Pos_all_x = []
    Pos_all_y = []
    for i in range(len(Robots)):
        for j in range(len(Robots[i])):
            robot = Robots[i][j]
            Pos_all_x.append(robot.pos[0])
            Pos_all_y.append(robot.pos[1])
    paths = ax.scatter(Pos_all_x,Pos_all_y)         # ax scatter
    plt.pause(0.000000001)
    paths.remove()

def robots_init(v_max):
    Robots = []
    for i in range(4):
        robots = []
        v_max = 20
        r = []
        ID = 0                  # The first robot
        if i == 0:              # lane A
            x_init = -200
            y_init = -3.5
            pos_init = [x_init, y_init]
            r = robot(pos_init,v_max,ID)
            robots.append(r)
        if i == 1:  #lane B
            x_init = -3.5
            y_init = -200
            pos_init = [x_init, y_init]
            r = robot(pos_init, v_max, ID)
            robots.append(r)
        if i == 2:  #lane C
            x_init = 200
            y_init = 3.5
            pos_init = [x_init, y_init]
            r = robot(pos_init, v_max, ID)
            robots.append(r)
        if i == 3:  #lane D
            x_init = 3.5
            y_init = 200
            pos_init = [x_init, y_init]
            r = robot(pos_init, v_max, ID)
            robots.append(r)
        Robots.append(robots)
    return Robots

if __name__== "__main__":

    # Initial plot
    # ax = plot_init()

    # Initial robots
    v_max = 20

    # update Big loop
    t = 0
    sum_robots = 0
    T_spent = 0
    T_expected = 0
    flag_light = 1
    time_clock = 0
    flag_policy = int(input('The flag_policy is (1:crosspass 2:traffic light '))  # control policy
    p_enter = 0
    delay_values = []

    if flag_policy == 1:
        ax = plot_init()
        Robots = robots_init(v_max)
        p_enter = 0.5
        while t < 500: # 100 time step
            t += 1
            update_status = update(Robots,flag_policy)
            # update new robot
            Robots = update_status.update_newrobot(Robots, v_max, p_enter)
            # update positions
            Robots, T_spent, T_expected, sum_robots, flag_light, time_clock = update_status.update_position(Robots,t, T_spent, \
                                            T_expected, sum_robots, flag_policy, flag_light, time_clock, ax)
            # viz the update
            plot(Robots,ax)
        delay_all = (T_spent - T_expected)/sum_robots
        print('The delay', delay_all)
        print('The sum of robots', sum_robots)

    if flag_policy == 2:
        while p_enter < 0.21:
            #print('p_enter is', p_enter)
            p_enter += 0.01
            #p_enter = 0.2
            # if p_enter != 0.2:
            #     print('The p_enter is ', p_enter)
            #     continue
            #print('The p_enter is ', p_enter)
            t = 0
            Robots = robots_init(v_max)
            T_spent = 0
            T_expected = 0
            sum_robots = 0
            ax = plot_init()
            while t < 250:  # 100 time step
                t += 1
                #print('The time t is ', p_enter)
                # update staus
                update_status = update(Robots, flag_policy)
                # update new robot
                Robots = update_status.update_newrobot(Robots, v_max, p_enter)
                # update positions
                Robots, T_spent, T_expected, sum_robots, flag_light, time_clock = update_status.update_position(Robots, t, T_spent, \
                                                T_expected, sum_robots, flag_policy, flag_light, time_clock, ax)
                # viz the update
                plot(Robots, ax)

            # clear all plot
            plt.close()
            delay_all = (T_spent - T_expected) / sum_robots
            SUM_all = 0
            for i in range(len(Robots)):
                SUM_all += len(Robots[i])
            print('The delay', delay_all)
            print('The sum of robots being calculated', sum_robots)
            print('The sum of all robots', SUM_all)
            print('The time of all the T_spent', T_spent)
            print('The time expected', T_expected)
            delay_values.append(delay_all)
            print('The delay_values are ', delay_values)



















            # pos_x = np.linspace(0, 0.21, num=21)
            # pos_y = [2.67999999999995, 3.7499999999999467, 5.524999999999938, 4.499999999999947, 4.927272727272669,
            #  2.690909090909044, 6.119999999999951, 3.699999999999948, 5.279999999999953, 4.927272727272674, 5.476923076923015, 5.914285714285654, 2.985714285714234, 4.799999999999941, 5.333333333333281,
            #  2.1142857142856712, 7.524999999999949, 6.711111111111048, 8.466666666666615, 5.764705882352888
            #     , 5.849999999999941]
            #
            # plt.scatter(pos_x, pos_y)
            # plt.plot(pos_x, pos_y)
            # plt.xlabel('The probability of spawning robot')
            # plt.ylabel('The average delay time')
            # plt.title('ME555 Hw3')
            # plt.show()









            # plot the result xaxis: probability of spawning model; yaxis: average delay time

 #        pos_x_1 = np.linspace(0, 0.21, num=21)
 #        pos_y_1 = [1.7749999999999524, 4.259999999999946, 3.999999999999943, 4.494736842105208, 3.624999999999943,
 #         2.495652173912993, 2.686956521739079, 3.8615384615384083, 4.3939393939393385, 5.446153846153787,
 #         4.83414634146336, 5.459090909090853, 3.766666666666611, 7.154166666666616, 4.408695652173858, 5.23529411764701,
 #         4.550943396226365, 9.625925925925888, 5.091228070175387, 5.862295081967155, 7.1399999999999375]
 #
 #        pos_x_2 = np.linspace(0, 0.21, num=21)
 #        pos_y_2 = [1.5999999999999563, 4.16666666666661, 2.584615384615338, 3.8272727272726725, 4.055999999999944,
 #         4.690909090909036, 4.471794871794816, 3.6666666666666137, 5.681081081081027, 3.6166666666666205, 3.8434782608695146, 4.545454545454489, 4.9499999999999424, 5.277551020408105, 5.02857142857137,
 #         5.4318181818181195, 7.250909090909045, 4.942857142857092, 8.934545454545415, 6.413333333333275, 7.071428571428527]
 #
 #        pos_x_3 = np.linspace(0, 0.21, num=21)
 #        pos_y_3 = [4.974999999999945, 4.016666666666613, 4.374999999999947, 4.249999999999943, 3.9133333333332834, 3.949999999999951, 3.278260869565172, 4.510526315789423, 5.399999999999946,
 #                 3.99069767441855, 5.2133333333332805, 4.513513513513468, 5.567999999999952, 6.069565217391251, 5.4615384615384, 4.399999999999941, 4.979999999999941, 5.303999999999946, 6.473333333333286, 12.176271186440676,
 # 9.816129032258011]
 #
 #        pos_x = []
 #        pos_y = []
 #        for i in range(len(pos_x_1)):
 #            x_a = pos_x_1[i]
 #            x_b = pos_x_2[i]
 #            x_c = pos_x_3[i]
 #            pos_x.append((x_a+x_b+x_c)/3)
 #            y_a = pos_y_1[i]
 #            y_b = pos_y_2[i]
 #            y_c = pos_y_3[i]
 #            pos_y.append((y_a+y_b+y_c)/3)
 #
 #        plt.scatter(pos_x, pos_y)
 #        plt.plot(pos_x, pos_y)
 #        plt.xlabel('The probability of spawning robot')
 #        plt.ylabel('The average delay time')
 #        plt.title('ME555 Hw3')
 #        plt.show()

