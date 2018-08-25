import matplotlib.pyplot as plt
import Robot_class
from Robot_class import *
import math
import random

def setting_init(r_area):
    Robot = []
    Target = []
    #Generate robot and target class
    #m = int(input("Enter the number of robots: "))  #robot
    #n = int(input("Enter the number of targets: "))  #target
    m = 30
    n = 3
    ratio = n/m
    value_rxy = 2 / math.sqrt(2)    #robot from 0~2m/s
    value_txy = 1.5 / math.sqrt(2)  #target from 0~1.5m/s
    #Generate the random coordinates for both robot and targets
    #list_x = [-40,-30,-20,0,0,20,30,40]
    #list_y = [0,25,35,40,-40,-35,-25,0]
    #list_robot = random.sample(range(len(list_x)-1), m)
    #list_target = random.sample(range(20),n)
    for i in range(m):
        # def __init__(self, Vrx, Vry, Pr, drr, drt, drb, Wrt, label, frt, frr, Frt, Frr, Frb, w_rt, w_rr, N_t)
        # def __init__(self, Vtx, Vty, Pt, dtb, label, Ftb):
        #Prx0 = list_x[list_robot[i]]
        #Pry0 = list_y[list_robot[i]]
        Prx0 = random.randrange(-int(r_area/math.sqrt(2)) , int(r_area/math.sqrt(2)))
        Pry0 = random.randrange(-int(r_area/math.sqrt(2)), int(r_area/math.sqrt(2)))
        v_rx0 = random.uniform(0,value_rxy)
        v_ry0 = random.uniform(0, value_rxy)
        r = robot(v_rx0, v_ry0, (Prx0, Pry0), [], [], 1, [], i+1, [], [], [], [], 1, [], [], 0)
        #r = robot(1, 1, (Prx0, Pry0), [], [], 1, [], i+1, [], [], [], [], 1, [], [], 0)
        r.w_rt = [1]*n #target
        r.w_rr = [1]*m #robot
        Robot.append(r)
    for j in range(n):
        Ptx0 = random.randrange(-int(r_area/math.sqrt(2)), int(r_area/math.sqrt(2)))
        Pty0 = random.randrange(-int(r_area/math.sqrt(2)), int(r_area/math.sqrt(2)))
        v_tx0 = random.uniform(-value_txy, value_txy)
        v_ty0 = random.uniform(-value_txy, value_txy)
        #(Vtx, Vty, Pt, dtb, label, Ftb, dtt)
        t = target(v_tx0, v_ty0, (Ptx0,Pty0), 1, j+1, 1, [])
        #t = target(0, 0, (Ptx0, Pty0), 1, j + 1, 1, [])
        Target.append(t)
    origin = (0, 0)
    dr1 = 12.5
    dr2 = 20
    do1 = 4
    do2 = 8
    do3 = 30
    dprr = 50
    return Robot,Target,origin,dr1,dr2,do1,do2,do3,dprr

def map(r_area):
    #r_area = 200
    circle = plt.Circle((0,0), r_area , color = 'r', fill = False)
    ax = plt.gca()
    ax.cla()  #clear the current gca figure
    ax.set_xlim((-r_area, r_area))
    ax.set_ylim((-r_area, r_area))
    ax.add_artist(circle)

def Init_plot(Robot,Target,radius_r,r_area, radius_p):
    ax = plt.gca()
    ax.cla()
    map(r_area)
    for i in range(len(Robot)):
        pointx = Robot[i].Pr[0]  # point of x coordinates
        pointy = Robot[i].Pr[1]  # point of y coordinates
        ax.plot(pointx, pointy, 'o', color='black')
        circle2 = plt.Circle((pointx, pointy), radius_r, color='b', fill=False)
        circle3 = plt.Circle((pointx, pointy), radius_p, color='y', fill=False)
        ax.add_artist(circle2)
        ax.add_artist(circle3)
        plt.show()
    # target
    for i in range(len(Target)):
        pointx = Target[i].Pt[0]
        pointy = Target[i].Pt[1]
        ax.plot(pointx, pointy, 'x', color='red')
        # ax.add_artist(circle)
        plt.show()
