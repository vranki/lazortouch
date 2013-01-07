import socket
import struct
import string
import time

HOST = "192.168.0.200"
PORT = 2111


class SICK:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.sock = socket.create_connection((HOST, PORT), 5, ("192.168.0.101",0))
        self.sock.connect((HOST,PORT))
        self.sock.settimeout(0.01)
        self.dev_status = 0
        self.frequency = 50

        self.stream = ""

    def device_status(self):
        return self.dev_status

    def frame(self, msg):
        return struct.pack("b", 2) + msg + struct.pack("b", 3)

    def meas_receiver(self):
        data1 = ""
        data2 = ""

        try:
            data1 = self.sock.recv(65536)
        except:
            return False, ""

        if len(data1) < 1600: 

            try:
                data2 = self.sock.recv(65536)
            except:
                return False, ""

            msg = (data1[1:] + data2[:-1]).split()

        else:
            msg = data1[1:-1].split()

        if len(msg) < 2:
            return False, ""

        if msg[0] == "sRA" and msg[1] == "LMDscandata":        
            return True, msg

        return False, ""  
        

    def receiver(self, exp_msg):
        data = ""

        try:
            data = self.sock.recv(12288)
        except:
            return False, ""

        if len(exp_msg) > 0 and data[1:len(exp_msg)+1] == exp_msg:
            return True, data[1:-1]
        if len(exp_msg) == 0 and len(data) > 0:
            return True, data[1:-1]
        
        return False, data[1:-1]

    def req_scan_data(self):
        self.sock.send(self.frame("sRN LMDscandata"))

    def recv_scan_data(self):
        while True:
            try:
                self.stream += self.sock.recv(65536)
            except:
                #timeout
                break

        msg_end = string.rfind(self.stream, "")
        if msg_end == -1:
            return False, ""

        msg_start = string.rfind(self.stream, "", 0, msg_end)
        if msg_start == -1:
            self.stream = ""
            return False, ""

        scan_data = self.stream[msg_start+1:msg_end].split()
        self.stream = self.stream[msg_end+1:]

        if scan_data[0] == "sRA" and scan_data[1] == "LMDscandata":        
            return True, scan_data

        return False, ""

    def start_measurement(self):
        self.sock.send(self.frame("sMN LMCstartmeas"))
        self.receiver("sFA 1")

    def measurement_status(self):
        self.sock.send(self.frame("sRN STlms"))
        found, data = self.receiver("sRA STlms")
        return int(data[10])

    def scan_once(self):

        self.req_scan_data()
        found, data = self.recv_scan_data()

        if not found:
            print "Error: laser data missing / in wrong format"
            return False, []

        self.dev_status = int(data[6])

        freq = data[16]
        if freq == "1388":
            self.frequency = 50
        elif freq == "9C4":
            self.frequency = 25
        
        data_start = 26

        meas_table = []
        
        ang = -135.0
        step_ang = 0.5

        for meas in data[data_start:-6]:
            l = len(meas)
            if l == 1:
                meas = "000" + meas
            elif l == 2:
                meas = "00" + meas
            elif l == 3:
                meas = "0" + meas

            try:    
                meas_table.append([ang, int(meas, 16)])
                ang += step_ang
            except:
                return False, []           

        #print mean_tilt, len(meas_table)
        return True, meas_table
        

    def close_connection(self):
        self.sock.close()


if __name__ == "__main__":
    print "1"
    my_laser = SICK()
    print "2"
    my_laser.start_measurement()
    print "3"
    my_laser.req_scan_data()
    my_laser.req_scan_data()
    print "4"
    my_laser.req_scan_data()
    print "5"
    print my_laser.recv_scan_data()
    print "6"
    time.sleep(0.5)
    print "7"
    print my_laser.recv_scan_data()
