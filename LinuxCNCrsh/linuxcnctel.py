# Don't forget when you use the write function, you need to insert "\r\n" at the end of the string. 

import telnetlib
import sys
  
class LinuxCNCTelnet:
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.EMC_ENABLE_PW = "EMCTOO"
    
    def printout(self):
        print self.host
        print self.port
    
    def connection(self):
        self.connect = telnetlib.Telnet(self.host, self.port)
        self.connect.write("HELLO EMC x 1.0\r\n")
        print self.connect.read_some()
        
    def enable(self):
        self.connect.write("SET ENABLE " + self.EMC_ENABLE_PW + "\r\n")
        print self.connect.read_some()
    
    # True means on, False means off.
    def setEStop(self, status):
        if status == True:
            eStop = "ON"
        else:
            eStop = "OFF"
        
        self.connect.write("SET ESTOP " + eStop + "\r\n")
        print self.connect.read_some()
        
    def setPower(self, status):
        if status == True:
            power = "ON"
            self.setMode("MANUAL")
        else:
            power = "OFF"
            
        self.connect.write("SET MACHINE " + power + "\r\n")
        print self.connect.read_some()
        
    def setHome(self, axis):
        self.connect.write("SET HOME " + str(axis) + "\r\n")
        print self.connect.read_some()
        
    def run(self):
        self.setMode("AUTO")
        self.connect.write("SET RUN \r\n")
        print self.connect.read_some()
        
    def setMode(self, mode):
        self.connect.write("SET MODE " + mode + "\r\n")
        print self.connect.read_some()
        
    def checkJointHomed(self, axis):
        self.connect.write("GET JOINT_HOMED " + axis + "\r\n")
        print self.connect.read_some().split()
        
if __name__ == '__main__':
    if len(sys.argv) == 3:
        newone = LinuxCNCTelnet(sys.argv[1], sys.argv[2])
        newone.printout()
        newone.connection()
        newone.enable()
        newone.setEStop(False)
        
        newone.setPower(True)
        
        newone.setHome(0)
        newone.setHome(1)
        newone.setHome(2)
       
        # newone.run()
    else:
        print "Usage: Host Port"