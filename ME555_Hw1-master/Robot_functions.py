import importlib as imp
import matplotlib.pyplot as plt
from scipy.spatial import distance as dist
from Robot_setting import *
import numpy as np
import math
import random
import time
import numpy

def Weight(Robot, Target, i_losttarget, i_lostrobot, dprr):
    #For lost targets
    if len(i_losttarget) != 0:
        for i in range(len(i_losttarget)):
            #For each target, find the k nearest robots
            target_spec = i_losttarget[i]
            #calculate the distances between all the robots
            dist_t2r = []
            dist_sort_list = []
            for j in range(len(Robot)):
                dist_t2r.append(Robot[j].drt[target_spec-1])    #robot label
            dist_sort = sorted(range(len(dist_t2r)), key=lambda k: dist_t2r[k])
            dist_sort_list = [x+1 for x in dist_sort]   #robot list with the correct label
    #For the near robot, calculate the weight coefficients, N_t is the number of targets
            for a in range(len(dist_sort_list)):
                # Initialize the robot weights
                Robot[dist_sort_list[a]-1].w_rt = [1] * len(Target)
                if Robot[dist_sort_list[a]-1].N_t == 0:
                    Robot[dist_sort_list[a]-1].w_rt[target_spec-1] = 1.5
                if Robot[dist_sort_list[a]-1].N_t == 1:
                    Robot[dist_sort_list[a]-1].w_rt[target_spec-1] = 1.4
                if Robot[dist_sort_list[a]-1].N_t == 2:
                    Robot[dist_sort_list[a]-1].w_rt[target_spec-1] = 1.3
                if Robot[dist_sort_list[a]-1].N_t == 3:
                    Robot[dist_sort_list[a]-1].w_rt[target_spec-1] = 1.2
                if Robot[dist_sort_list[a] - 1].N_t == 4:
                    Robot[dist_sort_list[a] - 1].w_rt[target_spec - 1] = 1.1
    if len(i_losttarget) == 0:
        for i in range(len(Robot)):
            Robot[i].w_rt = [1]*len(Target)

    #For lost robot, find the lost targets respectively
    if len(i_lostrobot) != 0:
        for i in range(len(i_lostrobot)):
            robot_spec = i_lostrobot[i]
            dist_r2t = []
            dist_sort_list = []
            for j in range(len(i_losttarget)): #lost targets
                tar_spec = i_losttarget[j]
                dist_r2t.append(Robot[robot_spec-1].drt[tar_spec-1])    #robot label
            dist_sort = sorted(range(len(dist_r2t)), key=lambda k: dist_r2t[k])
            dist_sort_list = [x+1 for x in dist_sort]   #target list with the correct label
    #For the nearest targets, add the weights for that problem
            wrt_robot = Robot[i].w_rt
            #wrt_robot = [(x - 0.5) for x in wrt_robot]                  #First lower the weights
            for a in range(len(dist_sort_list)):
                if Robot[i].drt[dist_sort_list[a]-1] < dprr:            #within predicted range
                    wrt_robot[dist_sort_list[a]-1] = 1.5
                    Robot[i].w_rt = wrt_robot
    return Robot,Target

def Find_lost(Robot,Target,radius_r):
    coeff_matrix, sum = coff_matrix(Robot,Target,radius_r)
    i_catchtarget = []
    i_losttarget = []
    i_catchrobot = []
    i_lostrobot = []
    #Find the column that is 0, and label the target
    for j in range(len(Target)):
        i_catchtarget = len([k for k in range(len(coeff_matrix[:,j])) if coeff_matrix[:,j][k] == 1]) # catch target
        if i_catchtarget == 0:
            i_losttarget.append(j+1) # The label of the lost targets
    #Find the lost robots
    for j in range(len(Robot)):
        i_catchrobot = len([k for k in range(len(coeff_matrix[j,:])) if coeff_matrix[j,:][k] == 1]) # catch target
        if i_catchrobot == 0:
            i_lostrobot.append(j+1) # The label of the lost robots
    N_catch = i_catchtarget
    return i_losttarget, i_lostrobot, N_catch

def coff_matrix(Robot,Target,radius_r):
    matrix = numpy.zeros((len(Robot),len(Target)))
    sum = 0
    N_catch = 0
    for i in range(len(Robot)):
        index_rt = [j for j in range(len(Robot[i].drt)) if Robot[i].drt[j] < radius_r]
        sum += len(index_rt)  #The number of 1 in the matrix
        for k in range(len(index_rt)):
            matrix[i][index_rt[k]] = 1
    return matrix, sum

def All_forcevector(Robot,Target):
    #calculate the overall force vector projected into both x and y coordinates
    #robot to target
    fsum_rt_x = fsum_rt_y = fsum_rr_x = fsum_rr_y = 0
    for i in range(len(Robot)):
        for j in range(len(Target)):
            sign_x, sign_y = p_direction(Robot[i].Pr[0], Robot[i].Pr[1], Target[j].Pt[0], Target[j].Pt[1], Robot[i].frt[2*j])
            fsum_rt_x = fsum_rt_x + sign_x*math.fabs(Robot[i].frt[2*j])*math.fabs(math.cos(Robot[i].frt[2*j+1]))*Robot[i].w_rt[j]
            fsum_rt_y = fsum_rt_y + sign_y*math.fabs(Robot[i].frt[2*j])*math.fabs(math.sin(Robot[i].frt[2*j+1]))*Robot[i].w_rt[j]
        Robot[i].Frt.append(fsum_rt_x)
        Robot[i].Frt.append(fsum_rt_y)
        #robot to robot
        for j in range(len(Robot)-1):
            flag_robot = Robot[i].drr[2 * j + 1]  # This is the label of other robot
            sign_x, sign_y = p_direction(Robot[i].Pr[0], Robot[i].Pr[1], Robot[flag_robot-1].Pr[0], Robot[flag_robot-1].Pr[1], Robot[i].frr[3*j])
            fsum_rr_x = fsum_rr_x + sign_x*math.fabs(Robot[i].frr[3*j])*math.fabs(math.cos(Robot[i].frr[3*j+1]))*Robot[i].w_rr[j]
            fsum_rr_y = fsum_rr_y + sign_y*math.fabs(Robot[i].frr[3*j])*math.fabs(math.sin(Robot[i].frr[3*j+1]))*Robot[i].w_rr[j]
        Robot[i].Frr.append(fsum_rr_x)
        Robot[i].Frr.append(fsum_rr_y)
    return Robot,Target

def forcevector(Robot,Target,dr1,dr2,do1,do2,do3,dprr):
    #robot to target
    for i in range(len(Robot)):
        for j in range(len(Target)):
            force_rt = F_r2t(Robot[i].drt[j], do1, do2, do3, dprr)
            theta_rt = theta(Robot[i].Pr[0],Robot[i].Pr[1],Target[j].Pt[0],Target[j].Pt[1]) #measure in radians
            Robot[i].frt.append(force_rt)
            Robot[i].frt.append(theta_rt)
    #robot to robot
    for i in range(len(Robot)):
        for j in range(len(Robot)-1):
            force_rr = F_r2r(Robot[i].drr[2*j], dr1, dr2)
            flag_robot = Robot[i].drr[2*j+1] #This is the label of other robot
            theta_rr = theta(Robot[i].Pr[0], Robot[i].Pr[1], Robot[flag_robot-1].Pr[0], Robot[flag_robot-1].Pr[1]) # measure in radians
            Robot[i].frr.append(force_rr)   #force value
            Robot[i].frr.append(theta_rr) #theta
            Robot[i].frr.append(Robot[i].drr[2*j+1])  #label
    return Robot, Target

def init_distances(Robot,Target,origin,radius_r):
    ##Distances -- should be init_distances
    # robot and target
    for i in range(len(Robot)):
        Nt = 0
        for j in range(len(Target)):
            Robot[i].drt.append(dist.euclidean(Robot[i].Pr, Target[j].Pt))
            if dist.euclidean(Robot[i].Pr, Target[j].Pt) < radius_r: #within range
                Nt += 1
        Robot[i].N_t = Nt
    # robot and robot
    for i in range(len(Robot)):
        for j in range(len(Robot)):
            if Robot[i].label == Robot[j].label:
                continue
            if Robot[i].label != Robot[j].label:
                Robot[i].drr.append(dist.euclidean(Robot[i].Pr, Robot[j].Pr))  # odd number
                Robot[i].drr.append(Robot[j].label)  # even number
    # target and target
    for i in range(len(Target)):
        for j in range(len(Target)):
            if Target[i].label == Target[j].label:
                continue
            if Target[i].label != Target[j].label:
                Target[i].dtt.append(dist.euclidean(Target[i].Pt, Target[j].Pt))  # odd number
                Target[i].dtt.append(Target[j].label)  # even number
    # robot/target and boundary
    for i in range(len(Target)):
        if i < len(Robot):
            Robot[i].drb = dist.euclidean(Robot[i].Pr, origin)
        Target[i].dtb = dist.euclidean(Target[i].Pt, origin)
    return Robot,Target

def p_direction(x1, y1, x2, y2, frt_rr):
    #This function defines the direction sign of force vectors
    #x1 and y1:coordinate of the robot  -- robot
    #x2 and y2:coordinate of the target -- target
    #frt_rr:force vector between robot and target/robot and robot -- consider them as the similar sign problems
    sign_x = 1
    sign_y = 1
    dx = x2 - x1
    if dx > 0:
        sign_x = 1
    if dx < 0:
        sign_x = -1
    dy = y2 - y1
    if dy > 0:
        sign_y = 1
    if dy < 0:
        sign_y = -1
    if frt_rr < 0:
        sign_x = -sign_x
        sign_y = -sign_y
    return sign_x, sign_y

def theta(x1,y1,x2,y2):
    if x1 == x2 and y1 != y2:
        theta = math.pi/2  # measure in radians
    if x1 != x2 and y1 == y2:
        theta = 0
    if x1 != x2 and y1 != y2:
        theta = math.atan( (y1-y2)/(x1-x2) )
    return theta

def line(x,x1,y1,x2,y2):
    d = 0
    d = ((y2-y1)/(x2-x1))*x + ((y1*x2-x1*y2)/(x2-x1))
    return d

def F_r2t(drt, do1, do2, do3, dprr):
    #This function defines the force vector between robot and target
    d = 0
    if drt < do1:
        d = line(drt,0,-1,do1,0)
    if drt >= do1 and drt < do2:
        d = line(drt,do1,0,do2,1)
    if drt >= do2 and drt < do3:
        d = 1
    if drt >= do3 and drt < dprr:
        d = line(drt,do3,1,dprr,0)
    if drt >= dprr:
        d = 0
    return d

def F_r2r(drr, dr1, dr2):
    #This function defines the vector between robot and robot
    #drr: distance between robot and robot
    #dr1: parameter 1:self define
    #dr2; parameter 2 self define
    d = 0
    if drr < dr1:
        return -1
    if drr >= dr1 and drr < dr2:
        d = (1/(dr2-dr1))*drr - (dr2/(dr2-dr1))
        return d
    if drr >= dr2:
        return 0
