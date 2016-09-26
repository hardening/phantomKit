from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory, Protocol
from twisted.internet.task import LoopingCall
from protocol import crc8
import crc16

def hexdumpBuffer(buf):
    items = []
    for b in buf:
        items.append("%0.2x" % ord(b))
        
    return " ".join(items)


class RcProtocol(Protocol):
    
    def __init__(self):
        self.powerTimer = LoopingCall(self.sendPowerLevel)
        self.packetSeq = 1
    
    
    def connectionMade(self):
        print "app connecting"
        self.powerTimer.start(2.0, False)
    
    def connectionLost(self, reason):
        self.powerTimer.stop()
        print "disconnected reason=%s" % reason        
    
    def sendPowerLevel(self):
        print "sending power level"
    
    def dataReceived(self, data):
        print "len=%0.4d == %s" % (len(data), hexdumpBuffer(data))
    
    def formatPacket(self, data):
        buf = '\x55%c\x04' % chr(len(data))
        crc = crc8.compute_crc8(buf, 0)
        
        buf += chr(crc) + data
        crc = crc16.Get_CRC16_Check_Sum(buf, crc16.CRC_INIT)
        buf += "%c%c" % (chr(crc & 0xff), chr((crc >> 8) & 0xff))
        return buf
        
    

class RcFactory(ServerFactory):
    def __init__(self):
        pass
    
    def buildProtocol(self, addr):
        return RcProtocol()


if __name__ == '__main__':      
    server = reactor.listenTCP(12345, RcFactory())
    reactor.run()
    