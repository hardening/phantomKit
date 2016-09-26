
import crc16
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet import reactor
from protocol import djiprotocol


    
class RcFactory(ClientFactory):
    def buildProtocol(self, addr):
        return RcProtocol()
    
    def clientConnectionFailed(self, connector, reason):
        print "connection failed, reason=%s" % reason

    def clientConnectionLost(self, connector, reason):
        print "connection lost, reason=%s" % reason

class RcProtocol(Protocol):
    def __init__(self):
        self.buffer = ""
        
    def dataReceived(self, data):
        self.buffer += data
        
        while True:
            pos = self.buffer.find('\x55')
            if pos < 0:
                return
            
            self.buffer = self.buffer[pos:]
            if len(self.buffer) < 13:
                return
            
            packetLen = ord(self.buffer[1])
            if packetLen < 13:
                continue
            
            if len(self.buffer) < packetLen:
                return
            
            
            packet = self.buffer[0 : packetLen]
            computedCrc = crc16.Get_CRC16_Check_Sum(packet[0:-2], crc16.CRC_INIT)
            crc = ord(packet[-2]) | ord(packet[-1]) << 8
            
            crcNotice = ""
            if crc != computedCrc:
                crcNotice = "invalidCrc(comp=%0.4x packet=%0.4x) " % (computedCrc, crc)
            
            #bufferDump = hexDump(self.buffer)

            cmdSet = ord(packet[9])
            cmd = ord(packet[10])
            
            parser = djiprotocol.getCommandInstance(cmdSet, cmd)
            if not parser:
                parser = djiprotocol.BaseCommand(cmdSet, cmd)
            if not parser.parseImpl(packet[11:-2]):
                print "parsing error..."
                
            if not parser.__class__.__name__ in ["DataRcGetPushParams"] or True:
                print "%s%s" % (crcNotice, parser)
            
            self.buffer = self.buffer[packetLen:]
        

if __name__ == '__main__':
    #reactor.connectTCP("127.0.0.1", 12345, RcFactory())
    reactor.connectTCP("127.0.0.1", 5678, RcFactory())
    reactor.run()
    

    