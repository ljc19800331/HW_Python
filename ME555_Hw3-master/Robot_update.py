# This is the update class structure based on Robot_class

import numpy as np
import Robot_class
from Robot_class import *
import matplotlib.pyplot as plt
import matplotlib

class update:
    def __init__(self, Robots, flag_policy):
        self.Robots = Robots
        self.flag_policy = flag_policy

    def update_newrobot(self, Robots, v_max, p_enter):
        #p_enter = 0.04                               # probability of generating robots
        flag_enter = np.random.choice(np.arange(1, 3), p=[p_enter, 1 - p_enter])
        r = []
        if flag_enter == 1:                          # generate a new robot
            p_sec = np.random.random_integers(0, 3)  # generate a new robot
            #print('p_sec', p_sec)
            if p_sec == 0:  # lane A
                x_init = -200
                y_init = -3.5
                ID = Robots[p_sec][-1].ID + 1
                pos_init = [x_init, y_init]
                r = robot(pos_init, v_max, ID)
                if dist.euclidean(r.pos, Robots[p_sec][-1].pos) > v_max:
                    Robots[p_sec].append(r)
            if p_sec == 1:  # lane B
                x_init = -3.5
                y_init = -200
                ID = Robots[p_sec][-1].ID + 1
                pos_init = [x_init, y_init]
                r = robot(pos_init, v_max, ID)
                if dist.euclidean(r.pos, Robots[p_sec][-1].pos) > v_max:
                    Robots[p_sec].append(r)
            if p_sec == 2:  # lane C
                x_init = 200
                y_init = 3.5
                ID = Robots[p_sec][-1].ID + 1
                pos_init = [x_init, y_init]
                r = robot(pos_init, v_max, ID)
                if dist.euclidean(r.pos, Robots[p_sec][-1].pos) > v_max:
                    Robots[p_sec].append(r)
            if p_sec == 3:  # lane D
                x_init = 3.5
                y_init = 200
                ID = Robots[p_sec][-1].ID + 1
                pos_init = [x_init, y_init]
                r = robot(pos_init, v_max, ID)
                if dist.euclidean(r.pos, Robots[p_sec][-1].pos) > v_max:
                    Robots[p_sec].append(r)
        return Robots

    def traffic_viz(self, time_clock, flag_light, ax):
        if flag_light == 1:
            l_1 = matplotlib.lines.Line2D([-7, -7], [-7, 7], linewidth=3, Color='g')
            ax.add_artist(l_1)
            l_2 = matplotlib.lines.Line2D([7, 7], [-7, 7], linewidth=3, Color='g')
            ax.add_artist(l_2)
            l_3 = matplotlib.lines.Line2D([-7, 7], [7, 7], linewidth=3, Color='r')
            ax.add_artist(l_3)
            l_4 = matplotlib.lines.Line2D([-7, 7], [-7, -7], linewidth=3, Color='r')
            ax.add_artist(l_4)
        if flag_light == 0:
            l_1 = matplotlib.lines.Line2D([-7, 7], [7, 7], linewidth = 3, Color='g')
            ax.add_artist(l_1)
            l_2 = matplotlib.lines.Line2D([-7, 7], [-7, -7], linewidth = 3, Color='g')
            ax.add_artist(l_2)
            l_1 = matplotlib.lines.Line2D([-7, -7], [-7, 7], linewidth=3, Color='r')
            ax.add_artist(l_1)
            l_2 = matplotlib.lines.Line2D([7, 7], [-7, 7], linewidth=3, Color='r')
            ax.add_artist(l_2)

    def update_position(self, Robots, T, T_spent, T_expected, sum_robots, flag_policy, flag_light, time_clock, ax):

        dt = 0.2

        #viz the traffic light
        timeclock = 35
        time_inter = 20

        if flag_policy == 2:
            if time_clock >= timeclock and flag_light == 1:
                flag_light = 0
                time_clock = 0
            if time_clock >= timeclock and flag_light == 0:
                flag_light = 1
                time_clock = 0
            time_clock += 1
            self.traffic_viz(time_clock, flag_light, ax)

        for i in range(len(Robots)):
            flag_lane = i
            for j in range(len(Robots[flag_lane])):
                flag_robot = j
                r = Robots[flag_lane][flag_robot]
                if r.flag_appear == 0 and r.flag_stat == 1:          # when the robot disappear and not be calculate
                    T_spent = T_spent + (r.t_spent - dt)
                    T_expected = T_expected + (r.t_expected)
                    sum_robots = sum_robots + 1
                    #del Robots[flag_lane][flag_robot]
                    #print('The current sum of robot is ', sum_robots)
                    r.flag_stat = 0
                if r.dist_spent <= 400 and r.flag_appear == 1:      # The robot doesn't disappear
                    r = Robots[flag_lane][flag_robot]
                    # update dist between front and back
                    r.dist_frontback(Robots, flag_lane, flag_robot)
                    # update velocity
                    r.velocity(self.flag_policy, flag_lane, flag_robot, Robots)
                    # update traffic behavior
                    if flag_policy == 2:
                        r.traffic_behavior(flag_light, time_clock, flag_lane, time_inter, timeclock)
                    # update spent time
                    r.spend_time(T)
                    # update spent distance
                    r.spend_dist()
                    # update position
                    r.position(flag_lane)

        return Robots, T_spent, T_expected, sum_robots, flag_light, time_clock




