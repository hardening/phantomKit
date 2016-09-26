from protocol.djiprotocol import BaseCommand
from protocol.cmdsetcommon import FieldsDumpable

class OsdGetPushSignalQuality(FieldsDumpable, BaseCommand):
    '''
    '''
    _FIELDS = ("b", "c", "d", "e", "f", "g",)
    
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)
        self.b = self.c = self.d = self.e = self.f = self.g = None

    def parseImpl(self, payload):
        if len(payload):
            b0 = ord(payload[0])
            if (b0 & 0x80) != 0:
                self.b = b0 & 0x7f
                if len(payload) >= 3:
                    self.d = ord(payload[1])
                    self.f = ord(payload[2])
                else:
                    self.d = self.f = 0
            else:
                self.b = 0
                self.d = self.f = 0
                        
            if (b0 & 0x80) == 0:
                self.c = b0 & 0x7f
                if len(payload) >= 3:
                    self.e = ord(payload[1])
                    self.g = ord(payload[2])
                else:
                    self.e = self.g = 0
            else:
                self.c = 0
                self.e = self.g = 0
        return True
    
