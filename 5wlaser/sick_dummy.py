import random

class SICK:
    def __init__(self):
        self.range = 2000

    def start_measurement(self):
        pass

    def measurement_status(self):
        return 7

    def scan_once(self):
        laser_points = []
        #if self.range < 2500:
        #    self.range += 1


        for i in range(-20, 20):
            laser_points.append([i, self.range])
        return True, laser_points

    def close_connection(self):
        pass

    
            
