from protocol.djiprotocol import BaseCommand
import struct
from protocol.cmdsetcommon import FieldsDumpable

class DataGimbalGetPushParams(FieldsDumpable, BaseCommand):
    _FIELDS = ("mode", "isAhead",)
    
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)
        self.a = None
        self.b = None
        self.c = None
        self.d = None
        self.e = None
        self.f = None
        self.g = None
        self.h = None
        self.i = None
        self.l = None        
        self.mode = None
        self.isAhead = None
        
    def parseImpl(self, payload):
        if len(payload) >= 12:
            (self.a, self.b, self.c, modeAhead, self.d, self.e, fghi, self.l) = struct.unpack("<HHHBBHBB", payload[0:12])
            self.mode = modeAhead >> 6
            self.isAhead = (modeAhead >> 5) & 0x01
            self.f = (fghi & 0x08) != 0
            self.g = (fghi & 0x10) != 0
            self.h = (fghi & 0x02) != 0
            self.i = (fghi & 0x40) != 0
        return True
    
    