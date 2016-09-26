from djiprotocol import BaseCommand
import struct
import datetime
from protocol.cmdsetcommon import FieldsDumpable

class GetBoardNumber(FieldsDumpable, BaseCommand):
    _IS_PUSH_COMMAND = False
    _RESP_FIELDS = ('number',)
    
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)
        self.number = None

    def parseImpl(self, payload):
        if len(payload) and self.isResponse:
            self.number = ''
            for b in payload:
                if b.isalpha():
                    self.number += b
                else:
                    self.number += "%s" % ord(b)
                    
        return True


(BATTERY_STATUS_OK, BATTERY_STATUS_INVALID, BATTERY_STATUS_EXCEPTION) = range(0, 3)
BATTERY_STATUS_NAMES = ("OK", "INVALID", "EXCEPTION")

class GetPushBatteryCommon(FieldsDumpable, BaseCommand):
    _FIELDS = ("date", "connStatus",)
    
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)
        self.date = None
        self.connStatus = None
        
    def parseImpl(self, payload):
        if len(payload) < 35:
            print "%s: payload too small(%d)" % (self.__class__.__name__, len(payload))
            return True
        
        dateInt = struct.unpack("<H", payload[30:32])[0]
        self.date = datetime.date(1980 + ((dateInt & 0xfe00) >> 9), (dateInt & 0x1e0) >> 5, dateInt & 0x1f)
        connStatus = ord(payload[34])
        self.connStatus = (connStatus < len(BATTERY_STATUS_NAMES)) and BATTERY_STATUS_NAMES[connStatus] or "UNKNOWN"
        return True


class CenterGetSelfDischarge(FieldsDumpable, BaseCommand):
    _IS_PUSH_COMMAND = False
    _REQ_FIELDS = ('b',)
    _RESP_FIELDS = ('a',)
    
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)
        self.a = self.b = None
        
    def parseImpl(self, payload):
        if self.isResponse:
            (self.a, ) = struct.unpack("<I", payload[0:4])
        else:
            self.b = ord(payload[0])
        return True
    
class SetBatteryCommon(FieldsDumpable, BaseCommand):
    _IS_PUSH_COMMAND = False
    _REQ_FIELDS = ('b', 'c',)
    
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)
        self.b = None
        self.c = 10
        
    def parseImpl(self, payload):
        if not self.isResponse:
            (self.b, self.c,) = struct.unpack("<BH", payload[0:3])
        return True
    