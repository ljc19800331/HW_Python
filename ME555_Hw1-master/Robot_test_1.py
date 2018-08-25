import importlib as imp
import Robot_functions
import Robot_setting
import Robot_update
from Robot_functions import *
from Robot_setting import *
from Robot_update import *

r_area = 0
radius_r = 30
radius_p = 35
T = 60
A = []
for t in range(10):
    dt = 1
    g_ij = []
    r_area += 100
    Robot, Target, origin, dr1, dr2, do1, do2, do3, dprr = setting_init(r_area)
    Robot, Target = init_distances(Robot, Target, origin, radius_r)
    update_collision(Robot, Target, r_area)
    Robot, Target = forcevector(Robot, Target, dr1, dr2, do1, do2, do3, dprr)
    Robot, Target = All_forcevector(Robot, Target)
    Init_plot(Robot, Target, radius_r, r_area, radius_p)
    print('Robot_initpos',Robot[0].Pr)
    for i in range(T):
        N_catch = robot_target_update(Robot, Target, dt, origin, radius_r, dr1, dr2, do1, do2, do3, dprr, r_area)
        g_ij.append(N_catch)
        Result_show(Robot,Target,radius_r, r_area,radius_p)
        # print('vrx',Robot[0].Vrx)
        # print('vry',Robot[0].Vry)
        # print('drt',Robot[0].drt)
        # print('drr', Robot[0].drr)
        # print('wrt', Robot[0].w_rt)
        # print('frt', Robot[0].frt)
        # print('frr', Robot[0].frr)
        # print('Frt', Robot[0].Frt)
        # print('Frb', Robot[0].Frb)
    A.append(sum(g_ij)/T)
    print('g_ij is ', g_ij)
print('The average over time is ', A)

