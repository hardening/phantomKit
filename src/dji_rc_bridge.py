from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory, Protocol, ClientFactory
from twisted.internet.task import LoopingCall

def hexdumpBuffer(buf):
    items = []
    for b in buf:
        items.append("%0.2x" % ord(b))
        
    return " ".join(items)



class RcProtocol(Protocol):
    
    def __init__(self, peer, direction):
        self.peer = peer
        self.direction = direction
    
    def connectionLost(self, reason):
        print "disconnected reason=%s" % reason        
        
    def dataReceived(self, data):
        print "%s len=%0.4d == %s" % (self.direction, len(data), hexdumpBuffer(data))
        self.peer.transport.write(data)
                

class ServerRcProtocol(RcProtocol):

    def connectionMade(self):
        self.peer = reactor.connectTCP("127.0.0.1", 2345, ClientRcFactory(self))
        print "app connecting"
    
    
class ClientRcFactory(ClientFactory):
    def __init__(self, serverPart):
        self.serverPart = serverPart
        
    def buildProtocol(self, addr):
        return RcProtocol(self.serverPart, "RC>")
    
class ServerRcFactory(ServerFactory):
    def __init__(self):
        pass
    
    def buildProtocol(self, addr):
        return ServerRcProtocol(None, "RC<")


if __name__ == '__main__':      
    server = reactor.listenTCP(12345, ServerRcFactory())
    reactor.run()
    