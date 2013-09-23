# Don't forget when you use the write function, you need to insert "\r\n" at the end of the string. 

import telnetlib
import sys
import time
  
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
        
    def setEcho(self, echo):
        if echo == True:
            self.connect.write("SET ECHO ON\r\n");
        elif echo == False:
            self.connect.write("SET ECHO OFF\r\n");
            
    # True means on, False means off.
    def setEStop(self, status):
        if status == True:
            eStop = "ON"
        else:
            eStop = "OFF"
        self.connect.write("SET ESTOP " + eStop + "\r\n")
        
    def setPower(self, status):
        if status == True:
            power = "ON"
            self.setMode("MANUAL")
        else:
            power = "OFF"  
        self.connect.write("SET MACHINE " + power + "\r\n")
                
    def setHome(self, axis):
        self.connect.write("SET HOME " + str(axis) + "\r\n")
        
    def run(self):
        self.setMode("AUTO")
        self.connect.write("SET RUN \r\n")
        
    def setMode(self, mode):
        self.connect.write("SET MODE " + mode + "\r\n")
        print self.connect.read_some()
        
    def checkJointHomed(self, axis):
        self.connect.write("GET JOINT_HOMED " + str(axis) + "\r\n")
        print "Hi "+str(self.connect.read_some().split())
        
    def ready(self):
        self.connect.read_until("JOINT_HOMED 2 YES", 10)
        
if __name__ == '__main__':
    if len(sys.argv) == 3:
        newone = LinuxCNCTelnet(sys.argv[1], sys.argv[2])
        newone.printout()
        newone.connection()
        newone.enable()
        
        # newone.setEcho(False)
        
        # Set 505
        newone.setEStop(False)
        
        newone.setPower(True)
        
        time.sleep(2)
        newone.setHome(0)
        newone.setHome(1)
        newone.setHome(2)
        time.sleep(2)
        
        newone.checkJointHomed(0);
        newone.checkJointHomed(1);
        newone.checkJointHomed(2);
        
        newone.ready()
        newone.run()
    else:
        print "Usage: Host Port"