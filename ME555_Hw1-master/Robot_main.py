import importlib as imp
import Robot_functions
import Robot_setting
import Robot_update
import Robot_class
from Robot_setting import *
from Robot_functions import *
from Robot_class import *
from Robot_update import *

def main():
    #def __init__(self, Vrx, Vry, Pr, drr, drt, drb, Wrt, label, frt, frr, Frt, Frr)
    #def __init__(self, Vtx, Vty, Pt, dtb, label):
    radius_r = 30
    dt = 1  #time interval
    Robot, Target, origin, dr1, dr2, do1, do2, do3, dprr = setting_init()
    Robot, Target = init_distances(Robot, Target, origin, radius_r)
    Robot, Target = forcevector(Robot, Target, dr1, dr2, do1, do2, do3, dprr)
    Robot, Target = All_forcevector(Robot, Target)
    Init_plot(Robot, Target, radius_r)
    ###############################
    t_old = time.process_time()
    for i in range(30):
        robot_target_update(Robot,Target,dt,origin)
        Result_show(Robot, Target)
    t_new = time.process_time()
    print ('The overall run time is %5.3f. ' % (t_new-t_old) )

if __name__ == '__main__':
    main()