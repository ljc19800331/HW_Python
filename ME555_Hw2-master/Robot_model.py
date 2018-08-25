#This script is used to define the model class
import math
from scipy.spatial import distance as dist
import numpy as np

#1.flocking class
class flocking:
    #Most of the functions return the forcevectors and weights
    def __init__(self, Robot, robot):
        self.Robot = Robot
        self.robot = robot

    def Homing(self, pos_target, robot):
    #point to the target point A
        dist_rt = dist.euclidean([self.robot.pos_x, self.robot.pos_y], pos_target)
        angle = theta_sign(robot.pos_x,robot.pos_y,pos_target[0],pos_target[1])
        force_home_x = 0
        force_home_y = 0
        w_home = 0.6
        if dist_rt > 10: #not close enough to the target
            force_home_x = w_home*math.cos(angle)                                     #some weights bigger than 1
            force_home_y = w_home*math.sin(angle)
        return force_home_x, force_home_y                                          #The homing force vectors for 100 robots

    def aggregation(self):
        #stay with the determined distances and stay close to the centroid
        pos_cen = centroid(self.Robot)
        #pos_cen = [-200,200]
        w_agg = 1.2
        for i in range(len(self.Robot)):
            #blob = Blobfinder(Robot, robot)
            angle = theta_sign(self.robot.pos_x, self.robot.pos_y, pos_cen[0], pos_cen[1])
            dist_rc = dist.euclidean([self.robot.pos_x, self.robot.pos_y], pos_cen)
            force_agg_x = 0
            force_agg_y = 0
            if dist_rc > 10:                #move the robot close to the centroid
                force_agg_x = w_agg*math.cos(angle)
                force_agg_y = w_agg*math.sin(angle)
            if dist_rc < 5:                #move the robot away to the centroid
                force_agg_x = -w_agg*math.cos(angle)
                force_agg_y = -w_agg*math.sin(angle)
        return force_agg_x, force_agg_y

    def Collision(self):
        w_coll = 1.4
        for i in range(len(self.Robot)):
            blob = Blobfinder(self.Robot, self.robot)
            r_sense = 50 #The sensing range of the robots
            distances, labels, directions = blob.robot_dists(r_sense)  #All the robots parameters are within blobfinder
            force_coll_x = []
            force_coll_y = []
            for j in range(len(distances)):
                dist = distances[j]
                label = labels[j]
                angle = directions[j]
                if dist < 5:                       #The collision, move the robots away
                    force_coll_x.append(-w_coll*math.cos(angle))
                    force_coll_y.append(-w_coll*math.sin(angle))
                if dist > 5 and dist == 5:        #The determined distances, flocking effect
                    force_coll_x.append(w_coll*math.cos(angle))
                    force_coll_y.append(w_coll*math.sin(angle))
            force_coll_X = sum(force_coll_x)
            force_coll_Y = sum(force_coll_y)
        return force_coll_X, force_coll_Y

#2.Blobfinder
class Blobfinder:
#The goal of Blobfinder is to find the relative positions between all the robots
    def __init__(self, Robot, robot):
        self.Robot = Robot
        self.robot = robot

    def robot_dists(self,r_sense):
        distances = []                          #The distances between agent robot and other robots
        labels = []                             #The labels corresponding to the distances
        directions = []                         #The directions measure by the theta [-pi,pi]
        for i in range(len(self.Robot)):
            if self.robot.label != i:
                dist = math.sqrt( (self.robot.pos_x - self.Robot[i].pos_x)**2 + (self.robot.pos_y - self.Robot[i].pos_y)**2 )
                if dist < r_sense:              #The robot within the sensing range
                    distances.append(dist)
                    labels.append(self.Robot[i].label)    #theta(x1,y1,x2,y2):
                    angle = theta_sign(self.robot.pos_x, self.robot.pos_y, self.Robot[i].pos_x, self.Robot[i].pos_y)
                    directions.append(angle)
        return distances, labels, directions

#Find the direction based on the theta
def theta_sign(x1,y1,x2,y2):
    #x1: robot.pos_x
    #x2: target.pos_y
    #y1: robot.pos_x
    #y2: target.pos_y
    #sign_x = 1
    #sign_y = 1
    if x1 == x2 and y1 != y2:
        theta = math.pi/2  # measure in radians
    if x1 != x2 and y1 == y2:
        theta = 0
    if x1 != x2 and y1 != y2:
        theta = math.atan2( (y2-y1), (x2-x1) )
        # sign_x = np.sign(x2 - x1)
        # sign_y = np.sign(y2 - y1)
    return theta

def centroid(Robot):
    #Return the centroid of the robots
    sum_x = 0
    sum_y = 0
    for i in range(len(Robot)):
        sum_x += Robot[i].pos_x
        sum_y += Robot[i].pos_y
    centroid_x = sum_x/len(Robot)
    centroid_y = sum_y/len(Robot)
    return centroid_x, centroid_y

