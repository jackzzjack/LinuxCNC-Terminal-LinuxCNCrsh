#! /bin/python
# Don't forget when you use the write function, you need to insert "\r\n" at the end of the string. 

import telnetlib
import sys
import time
import os
  
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
        print self.connect.read_until("HELLO ACK EMCNETSVR 1.1", 10)
        
    def enable(self):
        self.connect.write("SET ENABLE " + self.EMC_ENABLE_PW + "\r\n")
        print self.connect.read_until("SET ENABLE EMCTOO", 10)
        
    def setEcho(self, echo):
        if echo == True:
            self.connect.write("SET ECHO ON\r\n")
        elif echo == False:
            self.connect.write("SET ECHO OFF\r\n")
            print self.connect.read_until("SET ECHO OFF", 10)
            
    # True means on, False means off.
    def setEStop(self, status):
        if status == True:
            eStop = "ON"
        else:
            eStop = "OFF"
        self.connect.write("SET ESTOP " + eStop + "\r\n")
	print self.connect.read_until("SET ESTOP " + eStop, 10)
        
    def setPower(self, status):
        if status == True:
            power = "ON"
            self.setMode("MANUAL")
        else:
            power = "OFF"  
        self.connect.write("SET MACHINE " + power + "\r\n")
	print self.connect.read_until("SET MACHINE " + power)
                
    def setHome(self, axis):
        self.connect.write("SET HOME " + str(axis) + "\r\n")
	print self.connect.read_until("SET HOME " + str(axis))
        
    def run(self):
        self.setMode("AUTO")
        self.connect.write("SET RUN \r\n")
	print self.connect.read_until("SET RUN", 10)
        
    def setMode(self, mode):
        self.connect.write("SET MODE " + mode + "\r\n")
        print self.connect.read_until("SET MODE " + mode)
        
    def checkJointHomed(self, axis):
        self.connect.write("GET JOINT_HOMED " + str(axis) + "\r\n")
        # print "Hi "+str(self.connect.read_some().split())
        
    def ready(self):
        self.connect.read_until("JOINT_HOMED 2 YES", 10)
    
    def shutdown(self):
        self.connect.write("SHUTDOWN")
        
    def quit(self):
        self.connect.write("quit")
        
    def close(self):
        self.connect.close()

    def checkLinuxCNCStatus(self):
	self.connect.write("GET PROGRAM_STATUS\r\n")

	msg = self.connect.read_some()
	index = msg.find("IDLE")
	print "msg: " + msg
	print "index: " + str(index)
	if index >= 0:
		return False
	else:
		return True
#	if (self.connect.read_until("PROGRAM_STATUS RUNNING", 1)):
#		return True
#	elif (self.connect.read_until("PROGRAM_STATUS IDLE", 1)):
#		return False
#	else:
#		return False
#	print self.connect.read_until("PROGRAM_STATUS RUNNING", 1)
#	print "OK"

#	return 1
#	self.connect.read_until("IDLE")
#	print "OK"
#	return False
#	print self.connect.read_some()
#	print self.connect.read_very_eager()
#	print self.connect.read_very_eager()
        
if __name__ == '__main__':
    if len(sys.argv) == 3:
        time.sleep(5)
        
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
        
        # newone.checkJointHomed(0)
        # newone.checkJointHomed(1)
        # newone.checkJointHomed(2)
        
        # newone.ready()
        newone.run()
        
        time.sleep(2)
	while newone.checkLinuxCNCStatus():
		time.sleep(1)
	
	os.system("killall axis");
        
	newone.close()
    else:
        print "Usage: Host Port"
