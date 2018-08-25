import math
import numpy
from scipy.spatial import distance as dist

class robot:
    def __init__(self, pos_x, pos_y, vx, vy, label):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vx = vx
        self.vy = vy
        self.label = label                              #robot ID from 0,1,2 ... others

    def dist_cen(self, pos_cen):
        distance = math.sqrt((self.pos_x - pos_cen[0])**2 + (self.pos_y - pos_cen[1])**2)
        return distance

    def Delta_move(self, force_x, force_y, dt):
        dx = force_x*self.vx*dt
        dy = force_y*self.vy*dt
        return dx,dy

    def dist_rcen(self, pos_centroid):
        pos_r = [self.pos_x,self.pos_y]
        dist_r2cen = dist.euclidean(pos_r,pos_centroid)
        return dist_r2cen

