from math import *

class User_interface:
    def __init__(self, conf_file_name):
        self.area = []
        self.activators = []
        
        # +y forward, +x right, [cm]
        self.parse_conf(conf_file_name)

        self.pressed = [False]*len(self.activators)
        self.activation = 0

    def parse_conf(self, file_name):
        
        f = open(file_name, "r")
        first = True

        for line in f:
            line = line.strip()
            
            if len(line) == 0:
                continue

            # comment in configuration file
            if line[0] == "#":
                continue

            line = line.split(",")

            if first and len(line) == 4:
                self.area = [float(line[0]), float(line[1]), float(line[2]), float(line[3])]
                first = False
            elif len(line) == 5:
                self.activators.append([float(line[0]), float(line[1]), float(line[2]), 
                                        float(line[3]), int(line[4])])
            else:
                raise "Syntax error in configuration file", line


    def in_area(self, pt):
        if pt[0] > self.area[0] and pt[1] < self.area[1] and \
           pt[0] < self.area[2] and pt[1] > self.area[3]:
            return True
        return False

    def is_in_circle(self, pt, circle, old_status):
        if old_status == 1:
            r = circle[3]
        else:
            r = circle[2]

        l = sqrt((pt[0]-circle[0])**2 + (pt[1]-circle[1])**2)

        #print pt, circle
        #print l, r

        if l < r:
            return True
        else:
            return False
        
    def cartesian(self, pt):
        y = pt[1]/10*cos(pt[0]*pi/180)
        x = pt[1]/10*sin(pt[0]*pi/180)
        return (x,y)

    def update(self, laser_meas, mouse_pos_cm):

        for i in range(len(self.activators)):

            old_status = self.pressed[i]
            self.pressed[i] = False
        
            for pt in laser_meas:

                pt_pos_cm = self.cartesian(pt)
                
                if not self.in_area(pt_pos_cm):
                    continue

                status = self.is_in_circle(pt_pos_cm, self.activators[i], old_status)

                if status == True:
                    self.pressed[i] = True
                    break
                
            status2 = self.is_in_circle(mouse_pos_cm, self.activators[i], old_status)
            if status2 == True:
                self.pressed[i] = True
            

        return self.pressed, self.video_activation()

    def video_activation(self):
        #all_released = True

        for i in range(len(self.pressed)):
            #if self.pressed[i]:
            #    all_released = False

            if self.pressed[i] and self.activation == 0:
                self.activation = self.activators[i][4]
                break

            elif not self.pressed[i] and self.activation == self.activators[i][4]:
                self.activation = 0

        #if all_released:
        #    self.activation = -1

        return self.activation


    def get_bounding_box(self):
        return self.area

    def get_circles(self):
        return self.activators
        

if __name__ == "__main__":
    ui = User_interface("conf.ini")

    laser_points = []
    for i in range(-20, 20):
        laser_points.append([i, 1000])

    print ui.get_bounding_box()
    print ui.get_circles()
    print ui.update(laser_points)
    
            
            
