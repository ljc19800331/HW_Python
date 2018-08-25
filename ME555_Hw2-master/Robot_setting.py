from __future__ import division
import matplotlib.pyplot as plt
import Robot_class
from Robot_class import *
import Robot_model
from Robot_model import *
import math
import random
import numpy
import time

#def demo_plot(robot_all_x, robot_all_y, ax)

def demo(Robot,r_area,r_init,cir_init):
    # # show the update robot positions
    radius_r = 50
    ax = plt.gca()
    ax.cla()
    #plot the tracking line
    Init_plot_map(r_area, r_init, cir_init)
    x_track = numpy.arange(-200, 200, 1)
    y_track = [200] * len(x_track)
    y_track_1 = numpy.arange(-200, 200, 1)
    x_track_1 = [200] * len(x_track)
    target_A = [200,200]
    target_B = [200,-200]
    plt.scatter(target_A[0], target_A[1], c = 'g', marker='o', s = 100)
    plt.scatter(target_B[0], target_B[1], c='b', marker='o', s=100)
    plt.plot(x_track, y_track, 'r')
    plt.plot(x_track_1, y_track_1, 'r')
    for i in range(len(Robot)):
        pointx = Robot[i].pos_x  # point of x coordinates
        pointy = Robot[i].pos_y  # point of y coordinates
        circle = plt.Circle((pointx, pointy), radius_r, color='r', fill=False)
        ax.add_artist(circle)
        plt.scatter(pointx, pointy, s=5, c='b', marker='o')
    plt.draw()
    plt.pause(0.001)

def Robot_update(Robot, pos_target):
    dt = 1 #time step
    dist_robot2cen = [] #robot to centroid
    pos_centroid = centroid(Robot)
    robot_all_x = []
    robot_all_y = []
    # update the position
    for i in range(len(Robot)):
        x_old = Robot[i].pos_x
        y_old = Robot[i].pos_y
        #append the positions values
        robot_all_x.append(x_old)
        robot_all_y.append(y_old)
        #homing
        r = Robot[i]
        flock = Robot_model.flocking(Robot,r)
        force_home_x, force_home_y = flock.Homing(pos_target, r)
        #aggregation
        force_agg_x, force_agg_y = flock.aggregation()
        #collision model
        force_coll_X, force_coll_Y = flock.Collision()
        #Flocking model with forcevectors
        F_x = force_coll_X + force_home_x + force_agg_x
        F_y = force_coll_Y + force_home_y + force_agg_y
        Robot[i].pos_x = x_old + math.fabs(Robot[i].vx)*dt*F_x
        Robot[i].pos_y = y_old + math.fabs(Robot[i].vy)*dt*F_y
    # update the centroid to the robot positions
        dist_robot2cen.append(r.dist_rcen(pos_centroid))
    return Robot, dist_robot2cen, robot_all_x, robot_all_y

def target_check(Robot, target, pos_target, flag_target):
    pos_cen = centroid(Robot)
    #print('pos_cen =',pos_cen)
    if dist.euclidean(pos_cen, pos_target) < 20:
        pos_target = target[flag_target+1]
        flag_target = flag_target + 1
    return pos_target, flag_target

def Init_robot(r_init,cir_init):
    Robot = []
    m = int(input('The number of robots is '))
    for i in range(m):
        p_init = random_circle(r_init, cir_init)    #define random position within the circle
        px0 = p_init[0]
        py0 = p_init[1]
        vx0 = random.uniform(0.5,0.6)*2    #random velocity
        vy0 = random.uniform(0.5,0.6)*2    #random velocity
        r = robot([],[],[],[],[])        #First, initialize: (self, pos_x, pos_y, vx, vy, label):
        r.vx = vx0
        r.vy = vy0
        r.pos_x = px0
        r.pos_y = py0
        r.label = i
        Robot.append(r)
    return Robot

def Init_plot_map(r_area,r_init,cir_init):
    r_area = 400               #The radius of big environment
    r_init = 50                #The radius of small circle
    cir_init = [-200,200]      #The position of the small circle
    ax = plt.gca()
    ax.cla()
    # draw the environment -- big circle
    circle = plt.Circle((0,0), r_area , color = 'r', fill = False)
    ax = plt.gca()
    ax.cla()                                #clear the current gca figure
    ax.set_xlim((-r_area, r_area))
    ax.set_ylim((-r_area, r_area))
    ax.add_artist(circle)

def Init_plot_robots(Robot,cir_init, r_init):
    radius_r = 50
    # draw the small circle
    circle_init = plt.Circle(cir_init, r_init, color = 'b', fill = False)
    ax = plt.gca()
    ax.add_artist(circle_init)
    # draw the tracking line
    x_track = numpy.arange(-200, 200, 1)
    y_track = [200] * len(x_track)
    #plt.scatter(x_track, y_track)
    #plt.plot(x_track, y_track, '-x')
    for i in range(len(Robot)):
        pointx = Robot[i].pos_x  # point of x coordinates
        pointy = Robot[i].pos_y  # point of y coordinates
        circle = plt.Circle((pointx, pointy), radius_r, color='r', fill=False)
        ax.add_artist(circle)
        plt.scatter(pointx,pointy,s=5,c='b',marker='o')
        #ax.plot(pointx, pointy, 'o', color='black')
        #ax.plot(pointx, pointy, color = 'black')
        plt.show()

def random_circle(r_init,cir_init):
    # Random circle generators
    # radius of the circle
    circle_r = r_init
    # center of the circle (x, y)
    circle_x = cir_init[0]
    circle_y = cir_init[1]
    # random angle
    alpha = 2 * math.pi * random.random()
    # random radius
    r = circle_r * random.random()
    # calculating coordinates
    x = r * math.cos(alpha) + circle_x
    y = r * math.sin(alpha) + circle_y
    p_init = [x,y]
    return p_init

# if __name__ == "__main__":
#     main()