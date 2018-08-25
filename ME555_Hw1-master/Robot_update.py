from scipy.spatial import distance as dist
import importlib as imp
import Robot_functions
from Robot_functions import *

def update_collision(Robot, Target, r_area):
    #robot to target // robot to robot
    db1 = 5
    dbb = 5
    #robot
    for i in range(len(Robot)):
        #vrx_old = Robot[i].Vrx
        #vry_old = Robot[i].Vry
        #Robot[i].Pr = Pr_old
        if Robot[i].Frb == 1:
            if Robot[i].drb >= (r_area - db1):  # close to the boundary
                Robot[i].Frb = [-1]
                #Robot[i].Pr = Pr_old
                #Robot[i].Vrx = -vrx_old
                #Robot[i].Vry = -vry_old
            if Robot[i].drb < (r_area - db1):  # not close to the boundary
                Robot[i].Frb = [1]
                for j in range(len(Target)):
                    #vtx_old = Target[j].Vtx
                    #vty_old = Target[j].Vty
                    if Robot[i].drt[j] < dbb:   #close to target
                        Robot[i].Frb = [0]
                        #Robot[i].Vrx = -vrx_old
                        #Robot[i].Vry = -vry_old
                        #Robot[i].Frb = [-1.1]
                        Target[j].Ftb = -1
            for j in range(len(Robot)-1):
                if Robot[i].drr[2*j] < dbb:
                    Robot[i].Frb = [-1]
                    #Robot[i].Vrx = -vrx_old
                    #Robot[i].Vry = -vry_old
    #target
    for j in range(len(Target)):
        #boundary problem
        if Target[j].Ftb == 1:
            if Target[j].dtb >= (r_area - db1): #close to boundary
                Target[j].Ftb = -1
            if Target[j].dtb < (r_area - db1):
                Target[j].Ftb = 1
                for a in range(len(Target) - 1):
                    # target to target
                    if Target[j].dtt[2 * a] < dbb:
                        Target[j].Ftb = -1
                    if Target[j].dtt[2 * a] >= dbb:
                        Target[j].Ftb = 1

def Result_show(Robot,Target,radius_r, r_area,radius_p):
    #Second plot the coordinate points of robots and targets
    #robot
    #for i in range(30):  #time interval
    #calcualte the coefficient matrix
    ax = plt.gca()
    ax.cla()
    map(r_area)
    for i in range(len(Robot)):
        pointx = Robot[i].Pr[0] # point of x coordinates
        pointy = Robot[i].Pr[1] # point of y coordinates
        ax.plot(pointx, pointy, 'o', color='black')
        circle2 = plt.Circle((pointx, pointy), radius_r, color='b', fill=False)
        circle3 = plt.Circle((pointx, pointy), radius_p, color='y', fill=False)
        ax.add_artist(circle2)
        ax.add_artist(circle3)
        plt.show()
    #target
    for i in range(len(Target)):
        pointx = Target[i].Pt[0]
        pointy = Target[i].Pt[1]
        ax.plot(pointx, pointy, 'x', color='red')
        plt.show()
    plt.pause(0.5)

def robot_target_update(Robot,Target,dt,origin,radius_r,dr1,dr2,do1,do2,do3,dprr, r_area):
    i_losttarget, i_lostrobot, N_catch = Find_lost(Robot, Target,radius_r)
    g_ij = [] #The number of all the catched targets
    #update the drt -- robot and target and boundary
    Robot,Target = update_distances(Robot,Target,origin,radius_r)
    #update weight
    Robot,Target = Weight(Robot, Target, i_losttarget, i_lostrobot, dprr)
    # update the force vector considering the boundary problem
    Robot, Target = update_forcevector(Robot, Target, dt, dr1, dr2, do1, do2, do3, dprr)
    #update All_forcevector
    Robot,Target = update_Allforcevector(Robot, Target)
    #update collision model
    update_collision(Robot, Target, r_area)
    #update all positions
    Robot, Target = update_position(Robot,Target, dt)
    #update the number of lost target
    N_catch = len(Target) - len(i_losttarget)
    return N_catch

def update_forcevector(Robot,Target,dt, dr1, dr2, do1, do2, do3, dprr):
    # robot to target
    for i in range(len(Robot)):
        for j in range(len(Target)):
            force_rt = F_r2t(Robot[i].drt[j], do1, do2, do3, dprr)
            theta_rt = theta(Robot[i].Pr[0], Robot[i].Pr[1], Target[j].Pt[0], Target[j].Pt[1])  # measure in radians
            Robot[i].frt[2*j] = force_rt*Robot[i].w_rt[j]
            Robot[i].frt[2*j+1] = theta_rt
    # robot to robot
    for i in range(len(Robot)):
        for j in range(len(Robot) - 1):
            force_rr = F_r2r(Robot[i].drr[2 * j], dr1, dr2)
            flag_robot = Robot[i].drr[2 * j + 1]  # This is the label of other robot
            theta_rr = theta(Robot[i].Pr[0], Robot[i].Pr[1], Robot[flag_robot - 1].Pr[0],
                             Robot[flag_robot - 1].Pr[1])  # measure in radians
            Robot[i].frr[3*j] = force_rr*Robot[i].w_rr[j]  # force value
            Robot[i].frr[3*j+1] = theta_rr  # theta
            Robot[i].frr[3*j+2] = Robot[i].drr[2 * j + 1]  # label
    return Robot, Target

def update_position(Robot,Target,dt):
    for i in range(len(Robot)):
        fx_rt = Robot[i].Frt[0]
        fy_rt = Robot[i].Frt[1]
        fx_rr = Robot[i].Frr[0]
        fy_rr = Robot[i].Frr[1]
        if (fx_rt + fx_rr) == 0 or (fy_rt + fy_rr) == 0:
            Dx_r = Robot[i].Vrx
            Dy_r = Robot[i].Vry
        if (fx_rt + fx_rr) != 0 or (fy_rt + fy_rr) != 0:
            Dx_r = (fx_rt + fx_rr)*dt*Robot[i].Vrx*Robot[i].Frb[0]
            Dy_r = (fy_rt + fy_rr)*dt*Robot[i].Vry*Robot[i].Frb[0]
        Pr_old_x = Robot[i].Pr[0]
        Pr_old_y = Robot[i].Pr[1]
        Robot[i].Pr = ((Pr_old_x+Dx_r),(Pr_old_y+Dy_r))
    for j in range(len(Target)):
        Pt_old_x = Target[j].Pt[0]
        Pt_old_y = Target[j].Pt[1]
        Dx_t = Target[j].Vtx*dt*Target[j].Ftb
        Dy_t = Target[j].Vty*dt*Target[j].Ftb
        Target[j].Pt = ((Pt_old_x+Dx_t),(Pt_old_y+Dy_t))
    return Robot, Target

def update_distances(Robot,Target,origin,radius_r):
    for i in range(len(Robot)):
        Nt = 0
        for j in range(len(Target)):
            Robot[i].drt[j] = (dist.euclidean(Robot[i].Pr, Target[j].Pt))
            if dist.euclidean(Robot[i].Pr, Target[j].Pt) < radius_r: #within range
                Nt += 1
        Robot[i].N_t = Nt
    # robot and robot
    for i in range(len(Robot)):
        for j in range(len(Robot)-1):
            #if Robot[i].label == Robot[j].label:
            #    continue
            #if Robot[i].label != Robot[j].label:
            label_r = Robot[i].drr[2*j+1] - 1
            Robot[i].drr[2*j] = (dist.euclidean(Robot[i].Pr, Robot[label_r].Pr))  # odd number
                #Robot[i].drr[2*j+1] = (Robot[2*j+1].label)  # even number
    # target and target
    for i in range(len(Target)):
        for j in range(len(Target)-1):
            # if Target[i].label == Target[j].label:
            #     continue
            #if Target[i].label != Target[j].label:
            label_t = Target[i].dtt[2*j+1] - 1
            Target[i].dtt[2*j] = (dist.euclidean(Target[i].Pt, Target[label_t].Pt))  # odd number
                #Target[i].dtt.append(Target[j].label)  # even number
    # robot/target and boundary
    for i in range(len(Target)):
        if i < len(Robot):
            Robot[i].drb = dist.euclidean(Robot[i].Pr, origin)
        Target[i].dtb = dist.euclidean(Target[i].Pt, origin)
    return Robot,Target

def update_Allforcevector(Robot,Target):
    #calculate the overall force vector projected into both x and y coordinates
    #robot to target
    for i in range(len(Robot)):
        fsum_rt_x = fsum_rt_y = fsum_rr_x = fsum_rr_y = 0
        for j in range(len(Target)):
            sign_x, sign_y = p_direction(Robot[i].Pr[0], Robot[i].Pr[1], Target[j].Pt[0], Target[j].Pt[1], Robot[i].frt[2*j])
            fsum_rt_x = fsum_rt_x + sign_x*math.fabs(Robot[i].frt[2*j])*math.fabs(math.cos(Robot[i].frt[2*j+1]))#*Robot[i].w_rt[j]
            fsum_rt_y = fsum_rt_y + sign_y*math.fabs(Robot[i].frt[2*j])*math.fabs(math.sin(Robot[i].frt[2*j+1]))#*Robot[i].w_rt[j]
        Robot[i].Frt[0] = (fsum_rt_x)
        Robot[i].Frt[1] = (fsum_rt_y)
        #robot to robot
        for j in range(len(Robot)-1):
            flag_robot = Robot[i].drr[2 * j + 1]  # This is the label of other robot
            sign_x, sign_y = p_direction(Robot[i].Pr[0], Robot[i].Pr[1], Robot[flag_robot-1].Pr[0], Robot[flag_robot-1].Pr[1], Robot[i].frr[3*j])
            fsum_rr_x = fsum_rr_x + sign_x*math.fabs(Robot[i].frr[3*j])*math.fabs(math.cos(Robot[i].frr[3*j+1]))#*Robot[i].w_rr[j]
            fsum_rr_y = fsum_rr_y + sign_y*math.fabs(Robot[i].frr[3*j])*math.fabs(math.sin(Robot[i].frr[3*j+1]))#*Robot[i].w_rr[j]
        Robot[i].Frr[0] = (fsum_rr_x)
        Robot[i].Frr[1] = (fsum_rr_y)
    return Robot,Target