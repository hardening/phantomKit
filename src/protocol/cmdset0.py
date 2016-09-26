from protocol.djiprotocol import BaseCommand, hexDump
import struct
from datetime import datetime
from protocol.cmdsetcommon import FieldsDumpable

class Ping(BaseCommand):
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)
    
    def hasByte11InResponse(self):
        return True

    def parseImpl(self, payload):
        return True
    
    def __str__(self, *args, **kwargs):
        return "<Ping%s>" % (self.isResponse and "Resp" or "Req")

class GetVersion(BaseCommand):
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)
    
    def hasByte11InResponse(self):
        return True

    def parseImpl(self, payload):
        if self.packet.isResponse:
            return True
        return True
    
    def __str__(self, *args, **kwargs):
        return "<GetVersion%s>" % (self.isResponse and "Resp" or "Req")
    
class SetDate(FieldsDumpable, BaseCommand):
    _REQ_FIELDS = ("date", )
    _IS_PUSH_COMMAND = False
    
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)
        self.date = None
    
    def hasByte11InResponse(self):
        return True

    def parseImpl(self, payload):
        if not self.isResponse and len(payload) >= 7:
            (year, month, day, hour, minutes, second) = struct.unpack("<HBBBBB", payload[0:7])
            self.date = datetime(year, month, day, hour, minutes, second)
        return True
    

class GetDeviceInfo(BaseCommand):
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)

    def __str__(self, *args, **kwargs):
        if self.isResponse:
            return "<%sResp dump=%s>" % (self.__class__.__name__, self.dump)
        else:
            return "<%sReq target=%s/%s>" % (self.__class__.__name__, self.packet.targetType, self.packet.targetSubType)

        
        
class ActiveStatus(FieldsDumpable, BaseCommand):
    _REQ_FIELDS = ("component",)
    _RESP_FIELDS = ("dump",)
    _IS_PUSH_COMMAND = False
    
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)
        self.component = None
    
    def parseImpl(self, payload):
        if not self.isResponse:
            self.component = "%s/%s" % (self.packet.targetType, self.packet.targetSubType)
        else:
            self.dump = hexDump(payload)
        return True
            
    
class GimbalGetPushCheckStatus(FieldsDumpable):
    _FIELDS = ("b", "c", "d", "e", "f",)
    
    def __init__(self, b, c, d, e, f):
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f

class FlycGetPushCheckStatus(FieldsDumpable):
    _FIELDS = ("b", "c", "d", "e", "f", "g",)
    
    def __init__(self, b, c, d, e, f, g):
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        self.g = g

class BatteryGetPushCheckStatus(FieldsDumpable):
    _FIELDS = ("b", "c", "d", "e", "f", "g",)
    
    def __init__(self, b, c, d, e, f, g):
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        self.g = g
    
class GetPushCheckStatus(BaseCommand):
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)
        self.component = None
        self.value = None
    
    def parseImpl(self, payload):
        if self.packet.sourceType == "DM368" and self.packet.targetSubType == 1:
            self.component = "1860"
        elif self.packet.sourceType == "DOUBLE" and self.packet.targetSubType == 0:
            self.component = "2100"
        else:
            self.component = self.packet.sourceType
            
        if self.component == "GIMBAL":
            (b0, ) = struct.unpack("<I", payload[0:4])
            self.value = GimbalGetPushCheckStatus((b0 & 0x01) != 0, (b0 & 0x02) != 0, (b0 & 0x04) != 0, (b0 & 0x08) != 0, (b0 & 0x10) != 0)
        elif self.component == "FLYC":
            (b0, ) = struct.unpack("<I", payload[0:4])
            self.value = FlycGetPushCheckStatus((b0 & 0x01) != 0, (b0 & 0x02) != 0, 
                            (b0 & 0x04) != 0, (b0 & 0x08) != 0, (b0 & 0x10) != 0, (b0 & 0x20) != 0)
        elif self.component == "BATTERY":
            (b0, ) = struct.unpack("<I", payload[0:4])
            self.value = BatteryGetPushCheckStatus((b0 & 0x01) != 0, (b0 & 0x02) != 0, 
                            (b0 & 0x04) != 0, (b0 & 0x08) != 0, (b0 & 0x10) != 0, (b0 & 0x20) != 0)
        else:
            self.dump = hexDump(payload)
        return True
    
    def __str__(self, *args, **kwargs):
        ret = "<%s component=%s " % (self.__class__.__name__, self.component)
        if self.value:
            ret += "(" + self.value.dumpFields(self.value._FIELDS) + ")"
        else:
            ret += "dump=%s>" % self.dump
        return ret + ">"
    
class ZeroUnknown0x26(BaseCommand):
    pass
