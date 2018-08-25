
from scipy.spatial import distance as dist
import math
import numpy as np

class robot:
    def __init__(self, pos, v_max, ID):
        self.ID = ID  # ID name: measured with ordered number
        self.pos = pos                      # realtime position measured with [x,y]
        self.v_max = v_max                  # maximum velocity: 20 m/s default
        self.v = v_max                      # realtime velocity
        self.dis_front = 0                  # distance between front robot i-1
        self.dis_back = 0                   # distance between back robot i+1
        self.dist_spent = 0                 # distance spent on the simulator dist_spent = T*v
        self.dist_origin = 0                # distance between the robot and the center of the origin
        self.t_spent = 0                    # time spent based on time simulator T = i*dt (dt = 0.2)
        self.t_expected = 400/v_max                 # time expected from A to B: t_expected = length(AB)./v_max
        self.flag_appear = 1        # whether the robot has disappeared
        self.flag_stat = 1          # whether the robot has been calculated
        self.alpha = 0              # The accelerate rate
        self.flag_dir = 0           # flag_dir = 0: move forward flag_dir = 1:turn right flag_dir = 2:turn left

    def dist_frontback(self, Robots, flag_lane, flag_robot):        # test in traffic control
        if len(Robots[flag_lane]) == 1:
            self.dis_front = 0
            self.dis_back = 0
        if len(Robots[flag_lane]) > 1:
            if flag_robot == Robots[flag_lane][0].ID:       # The first one only has back robot
                self.dis_front = 0
                self.dis_back = dist.euclidean(Robots[flag_lane][flag_robot].pos, Robots[flag_lane][flag_robot+1].pos)
            if flag_robot == Robots[flag_lane][-1].ID:      # The last one only has front robot
                self.dis_back == 0
                self.dis_front = dist.euclidean(Robots[flag_lane][flag_robot].pos, Robots[flag_lane][flag_robot-1].pos)
            else:
                self.dis_front = dist.euclidean(Robots[flag_lane][flag_robot].pos, Robots[flag_lane][flag_robot-1].pos)
                self.dis_back = dist.euclidean(Robots[flag_lane][flag_robot].pos, Robots[flag_lane][flag_robot+1].pos)

    def exp_time(self, flag_policy):
        if flag_policy == 1: # crosspass
            self.t_expected = 400/self.v_max
        if flag_policy == 2: # traffic light
            delta_t_cross = 5   # the time to cross the intersection
            self.t_expected = 400/self.v_max + delta_t_cross

    def spend_time(self, T):    # T: time step in the big loop
        if self.dist_spent <= 400:
            dt = 0.2
            old_t_spent = self.t_spent
            self.t_spent = old_t_spent + dt

    def spend_dist(self):
        # if math.fabs(self.dist_spent - 400) <= self.v and self.dist_spent >= 400:
        if math.fabs(self.dist_spent - 400) < 5:
            #print('The dist_spent is ', self.dist_spent)
            self.flag_appear = 0

        if self.dist_spent <= 400:
            dt = 0.2
            self.dist_spent = self.dist_spent + self.v*dt

    def position(self, flag_lane):
        dt = 0.2
        delta_dist = self.v*dt
        x_old = self.pos[0]
        y_old = self.pos[1]
        if self.v > 0 and self.flag_dir == 0:         # The car cannot go back
            if flag_lane == 0:  # lane A
                self.pos[0] = x_old + delta_dist
            if flag_lane == 1:  # lane B
                self.pos[1] = y_old + delta_dist
            if flag_lane == 2:  # lane C
                self.pos[0] = x_old - delta_dist
            if flag_lane == 3:  # lane D
                self.pos[1] = y_old - delta_dist

        # turn right
        if self.v > 0 and self.flag_dir == 1 : # turn right
            if flag_lane == 0 and self.dist_spent > 207:  # lane A
                self.pos[0] = x_old
                self.pos[1] = y_old - delta_dist
            if flag_lane == 1 and self.dist_spent > 193:  # lane B
                self.pos[0] = x_old + delta_dist
                self.pos[1] = y_old
            if flag_lane == 2 and self.dist_spent > 207:  # lane C
                self.pos[0] = x_old
                self.pos[1] = y_old + delta_dist
            if flag_lane == 3 and self.dist_spent > 193:  # lane D
                self.pos[0] = x_old - delta_dist
                self.pos[1] = y_old

        # turn left
        if self.v > 0 and self.flag_dir == 2 :  # turn left
            if flag_lane == 0 and self.dist_spent > 193:  # lane A
                self.pos[0] = x_old
                self.pos[1] = y_old + delta_dist
            if flag_lane == 1 and self.dist_spent > 207:  # lane B
                self.pos[0] = x_old - delta_dist
                self.pos[1] = y_old
            if flag_lane == 2 and self.dist_spent > 193:  # lane C
                self.pos[0] = x_old
                self.pos[1] = y_old - delta_dist
            if flag_lane == 3 and self.dist_spent > 207:  # lane D
                self.pos[0] = x_old + delta_dist
                self.pos[1] = y_old

    def velocity(self, flag_policy, flag_lane, flag_robot, Robots):
        # collision model and control the velocity
        d_sense = 60
        d_half = 7
        d_sense_safe = 100
        alpha_start = 50
        dt = 0.2
        d_safe = 100
        if flag_policy == 1: # crosspass
            self.v = self.v_max

        if flag_policy == 2 and self.dist_spent < (200 - d_half - d_sense):
            self.v = 20

        if flag_policy == 2: #and self.dist_spent >= (200 - d_half - d_sense) and self.dist_spent <= (200 - d_half):

            distfront = self.dis_front

            if self.v >= 20:  # maintein the max velocity
                self.v = 20

            if self.v < 0:  # in case the decelerate case
                self.alpha = alpha_start
                self.v = self.v + self.alpha * dt

            if distfront < 40 and distfront > 0 and self.v >= 0:
                self.alpha = self.collision_line(distfront)
                self.v = self.v + self.alpha * dt

            if distfront < 5 and distfront > 0 and self.dist_spent >= (200 - d_half - d_safe) and self.dist_spent <= (200 - d_half):
                self.v = 0

    def traffic_behavior(self, flag_light, time_clock, flag_lane, time_inter, timeclock):

        dt = 0.2
        d_sense = 15
        d_half = 7
        #time_inter = 20
        #timeclock = 35
        dist_safe = 10
        alpha_start = 100        # The alpha after stopping the car
        p_dir = np.random.choice(np.arange(0, 3), p=[0.5, 0.25, 0.25])

        # green light h and red light v
        if flag_light == 1 and time_clock <= timeclock and self.dist_spent >= (200 - d_half - d_sense) and self.dist_spent <= (200-d_half):

            # move forward choice
            if flag_lane == 0:  # lane A
                self.flag_dir = p_dir
                self.dist_origin = - d_half - self.pos[0]
                if time_clock >= time_inter and self.dist_origin >= dist_safe:
                    self.alpha = self.decelerate_line(self.dist_origin)
                    self.v = self.v + self.alpha * dt
                if time_clock < time_inter:
                    self.v = 20
                    # self.alpha = alpha_start
                    # self.v = self.v + self.alpha * dt

            if flag_lane == 1:  # lane B
                self.dist_origin = - d_half - self.pos[1]
                self.alpha = self.decelerate_line(self.dist_origin)
                self.v = self.v + self.alpha * dt

            if flag_lane == 2:  # lane C
                self.flag_dir = p_dir
                self.dist_origin = self.pos[0] - d_half
                if time_clock >= time_inter and self.dist_origin >= dist_safe:
                    self.alpha = self.decelerate_line(self.dist_origin)
                    self.v = self.v + self.alpha * dt
                if time_clock < time_inter:
                    self.v = 20
                    # self.alpha = alpha_start
                    # self.v = self.v + self.alpha * dt

            if flag_lane == 3:  # lane D
                self.dist_origin = self.pos[1] - d_half
                self.alpha = self.decelerate_line(self.dist_origin)
                self.v = self.v + self.alpha * dt

        # green light v and red light h
        if flag_light == 0 and time_clock <= timeclock and self.dist_spent >= (200 - d_half - d_sense) and self.dist_spent <= (200-d_half):

            if flag_lane == 0:  # lane A
                self.dist_origin = -d_half - self.pos[0]
                self.alpha = self.decelerate_line(self.dist_origin)
                self.v = self.v + self.alpha * dt

            if flag_lane == 1:  # lane B
                self.flag_dir = p_dir
                self.dist_origin = -d_half - self.pos[1]
                if time_clock >= time_inter and self.dist_origin >= dist_safe:
                    self.alpha = self.decelerate_line(self.dist_origin)
                    self.v = self.v + self.alpha * dt
                if time_clock < time_inter:
                    self.v = 20
                    # self.alpha = alpha_start
                    # self.v = self.v + self.alpha * dt

            if flag_lane == 2:  # lane C
                self.dist_origin = self.pos[0] - d_half
                self.alpha = self.decelerate_line(self.dist_origin)
                self.v = self.v + self.alpha * dt

            if flag_lane == 3:  # lane D
                self.flag_dir = p_dir
                self.dist_origin = self.pos[1] - d_half
                if time_clock >= time_inter and self.dist_origin >= dist_safe:
                    self.alpha = self.decelerate_line(self.dist_origin)
                    self.v = self.v + self.alpha * dt
                if time_clock < time_inter:
                    self.v = 20
                    # self.alpha = alpha_start
                    # self.v = self.v + self.alpha * dt

        if self.dist_spent >= (200 - d_half):
            self.v = 20

        if self.v >= 20:
            self.v = 20

        if self.v <= 0:
            self.v = 0

        if self.dis_front < 5 and self.dis_front > 0 and self.dist_spent >= (200 - d_half - d_sense) and self.dist_spent <= (200-d_half):
            #print('The dis_front is ', self.dist_front)
            self.v = 0

    def decelerate_line(self, dist_origin):
        alpha = 3 * dist_origin - 180
        return alpha

    def collision_line(self, dis_front):
        alpha = 2.5 * dis_front - 50
        return alpha

