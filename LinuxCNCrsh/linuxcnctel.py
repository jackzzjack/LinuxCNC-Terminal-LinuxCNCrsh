import telnetlib
import sys
  
class LinuxCNCTelnet:
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
    
    def printout(self):
        print self.host
        print self.port
    
    def connection(self):
        connect = telnetlib.Telnet(self.host, self.port)
        connect.write("HELLO EMC x 1.0\r\n")
        print connect.read_some()
        
if __name__ == '__main__':
    if len(sys.argv) == 3:
        newone = LinuxCNCTelnet(sys.argv[1], sys.argv[2])
        newone.printout()
        newone.connection()
    else:
        print "Usage: Host Port"