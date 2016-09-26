from protocol.djiprotocol import BaseCommand
import struct
import math
from protocol.cmdsetcommon import FieldsDumpable
from datetime import datetime



class FlycSetTimeZone(FieldsDumpable, BaseCommand):
    _REQ_FIELDS = ("timezone", )
    _IS_PUSH_COMMAND = False
    
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)
        self.timezone = None
        
    def parseImpl(self, payload):
        if not self.isResponse and len(payload) >= 2:
            (self.timezone, ) = struct.unpack("<h", payload[0:2])
        return True


class FlycGetPushDeformStatus(FieldsDumpable, BaseCommand):
    '''
    '''
    _FIELDS = ("deformMode", "tripodStatus",)
    
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)
        self.deformMode = self.tripodStatus = None
        
    def parseImpl(self, payload):
        if len(payload):
            b1 = ord(payload[0])
            self.deformMode = (b1 & 0x30) >> 4
            self.tripodStatus = (b1 & 0xE) >> 1
            
        return True

class UnlimitedArea(object):
    def __init__(self, a, b, c, d, e, f):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
    
class FlycGetPushUnlimitState(FieldsDumpable, BaseCommand):
    _FIELDS = ("#areas", )
    
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)
        self.areas = None
        
    def parseImpl(self, payload):
        if len(payload) > 2:
            nAreas = ord(payload[2])
            possibleAreas = (len(payload) - 7) / 21
            if possibleAreas < nAreas:
                nAreas = possibleAreas
            
            self.areas = []
            for i in range(0, nAreas):
                startAt = 7 + i * 21
                (a, b, c, d, e, f) = struct.unpack("<IIIBII", payload[startAt:startAt+21])
                
                self.areas.append(UnlimitedArea(a / 1000000.0, b / 1000000.0, c, d, e, f))
            
        return True


FLYC_COMMAND = {
    1: "takeoff",
    2: "land",
}

class FlycFunctionControl(FieldsDumpable, BaseCommand):
    '''
    '''
    _REQ_FIELDS = ('command',)
    _RESP_FIELDS = ('code',)
    _IS_PUSH_COMMAND = False

    
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)
        self.planeName = None
        
    def parseImpl(self, payload):
        b0 = ord(payload[0])
        if self.isResponse:
            self.code = b0
        else:
            self.command = FLYC_COMMAND.get(b0, "unknow(%d)" % b0) 
        return True
    
    
class FlycGetPlaneName(FieldsDumpable, BaseCommand):
    '''
    '''
    _RESP_FIELDS = ('planeName',)
    _IS_PUSH_COMMAND = False

    
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)
        self.planeName = None
    
    def hasByte11InResponse(self):
        return True
    
    def parseImpl(self, payload):
        if len(payload) >= 32:
            try:
                self.planeName = payload[0:32].decode('utf-8')
            except:
                print "invalid plane name"
                return False
        return True
    

class OsdGetPushCommon(FieldsDumpable, BaseCommand):
    _FIELDS = ("longitude", "latitude", "c", "d", "e", "f", "g", "h", "i", "j", "flycState", 
                  "A", "B", "motorStartFailed", "motorStartFailedCause", "nonGpsCause", "G", "H",
                  "I", "J", "KdroneType", "LmotorStartFailedCause", "MinitIMUFailReason", "N", "O", 
                  "PmotorFailedReason", "l", "m", "n", "oGoHomeStatus", "p", "q", "r",
                  "sRcModeChannel", "tRcModeChannel", "u", "v", "w", "xBatteryType",
                  "y", "z", "flightAction", )
    
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)
        self.longitude = self.latitude = None
        self.c = self.d = self.e = self.f = self.g = self.h = self.i = self.j = self.A = self.B = self.C = None
        self.G = self.H = self.I = self.J = self.KdroneType = self.LmotorStartFailedCause = self.MinitIMUFailReason = self.N = self.O = self.PmotorFailedReason = None
        self.l = self.m = self.n = self.oGoHomeStatus = self.p = self.q = self.r = self.sRcModeChannel = self.tRcModeChannel = self.u = self.v = self.w = self.xBatteryType = self.y = self.z = None
        self.flycState = None
        self.flightAction = None
        self.motorStartFailed = None
        self.motorStartFailedCause = None
        self.nonGpsCause = None
        
    def parseImpl(self, payload):
        if len(payload) >= 50:
            (double1, double2, self.c, self.d, self.e, self.f, self.g, 
             self.h, self.i, j_flyc_state) = struct.unpack("<ddHHHHHHHBx", payload[0:32])
            
            self.latitude = double2 * 180.0 / math.pi
            self.longitude = double1 * 180.0 / math.pi
            self.j = (j_flyc_state & 0x80) == 0
            self.flycState = j_flyc_state & 0x7F;
            
            (bitsValue, self.C, self.flightAction, motorStart, self.nonGpsCause, self.G, self.H) = struct.unpack("<IBBBBBB", payload[32:42])
            
            self.A = (bitsValue >> 28) & 0x1 != 0
            self.B = (bitsValue >> 29) & 0x1 != 0
            self.l = (bitsValue >> 1) & 0x3
            self.m = ((bitsValue >> 3) & 0x1) == 0x1
            self.n = (bitsValue & 0x10) != 0x0
            self.oGoHomeStatus = (bitsValue >> 5) & 0x7
            self.p = (bitsValue & 0x1000) != 0x0
            self.q = (bitsValue & 0x100) != 0x0
            self.r = (bitsValue & 0x600) >> 9
            self.sRcModeChannel = (bitsValue & 0x6000) >> 13
            self.tRcModeChannel = (bitsValue & 0x6000) >> 13
            self.u = (bitsValue & 0x10000) != 0x0
            self.v = (bitsValue & 0x20000) != 0x0
            self.w = (bitsValue >> 18) & 0xF
            self.xBatteryType = (bitsValue >> 22) & 0x3
            self.y = ((bitsValue >> 26) & 0x1) != 0x0
            self.z = ((bitsValue >> 27) & 0x1) != 0x0
            
            self.motorStartFailed = motorStart & 0x80 != 0
            if self.motorStartFailed:
                self.motorStartFailedCause = motorStart & 0x7f
                
            (self.I, self.J, self.KdroneType, self.MinitIMUFailReason, self.PmotorFailedReason, self.LmotorStartFailedCause) = struct.unpack("<HBBBBB", payload[42:49])
            
        return True


class FlycGetPushPowerParams(FieldsDumpable, BaseCommand):
    _FIELDS = ("float1", "float2",)
    
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)
        self.float1 = None
        self.float2 = None

    def parseImpl(self, payload):
        if len(payload) >= 8:
            (self.float1, self.float2) = struct.unpack("<ff", payload[0:8])
        return True

    
class FlycGetPushSmartBattery(FieldsDumpable, BaseCommand):
    _FIELDS = ("a", "b", "c", "d", "smartGoHomeStatus", "f", "volts", "h", "i", "j", "k",)
    
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)
        self.a = self.b = self.c = self.d = self.smartGoHomeStatus = self.f = self.volts = None
        self.h = self.i = self.j = self.k = None

    def parseImpl(self, payload):
        (self.a, ) = struct.unpack("<H", payload[0:2])
        (self.b, self.c) = struct.unpack("<HH", payload[6:10])
        (self.d, self.smartGoHomeStatus, self.f, volts, self.h, i, j, self.k) = struct.unpack("<IBBHBBBB", payload[18:30])
        self.volts = volts / 1000.0
        self.i = i & 0x7f
        self.j = j & 0x7f
        return True

    
class LedStatus(object):
    def __init__(self, color, b):
        self.color = color
        self.b = b
        
    def __str__(self, *args, **kwargs):
        return "(%s,%s)" % (self.color, self.b)
    
    def __unicode__(self, *args, **kwargs):
        return "(%s,%s)" % (self.color, self.b)
        
class FlycGetPushLedStatus(FieldsDumpable, BaseCommand):
    _FIELDS = ("ledReason", "ledStatus",)
    
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)
        self.ledReason = None
        self.ledStatus = None

    
    def parseImpl(self, payload):
        (self.ledReason, nbLedStatus) = struct.unpack("<II", payload[0:8])
        
        if nbLedStatus > 20:
            nbLedStatus = 20
        if len(payload) < 8 + nbLedStatus * 4:
            print "payload is too small to hold %d ledStatus" %  nbLedStatus
            return False
        
        self.ledStatus = []
        startAt = 8        
        for _ in range(0, nbLedStatus):
            (color, b) = struct.unpack("<HH", payload[startAt:startAt+4])
            self.ledStatus.append(LedStatus(color, b))
            startAt += 4
        
        return True
    
class OsdGetPushHome(FieldsDumpable, BaseCommand):
    _FIELDS = ("lattitude", "longitude", "c", "iocMode", "e", "f", "g", "h", "i", "altitudeLimit", "distanceLimit",
               "l", "m", "n", "o", "heightLimitStatus", "q", "r", "motorStates")
    
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)
        self.longitude = self.lattitude = None
        self.c = self.iocMode = self.e = self.f = self.g = self.h = None
        self.i = self.altitudeLimit = self.k = self.l = self.m = self.n = None
        self.o = self.heightLimitStatus = self.q = self.r = None
        self.motorStates = None
        
    def parseImpl(self, payload):
        (a, b, self.c, defghijkl, self.m, self.n, self.o) = struct.unpack("<ddfHHHB", payload[0:27])
        
        self.longitude = a * 180.0 / math.pi 
        self.lattitude = b * 180.0 / math.pi
        self.iocMode = (defghijkl & 0xE000) >> 13  
        self.e = ((defghijkl & 0x1000) >> 12) != 0
        self.f = ((defghijkl >> 11) & 0x1) != 0
        self.g = ((defghijkl & 0x400) >> 10) != 0
        self.h = ((defghijkl & 0x300) >> 8)
        self.i = ((defghijkl >> 6) & 0x1) != 0
        self.altitudeLimit = ((defghijkl & 0x20) >> 5) != 0
        self.distanceLimit = ((defghijkl & 0x10) >> 4) != 0
        self.l = (defghijkl & 0x1) != 0
        
        r = ord(payload[32])
        self.r = (r & 0x01) != 0
        if len(payload) >= 49:
            (self.heightLimitStatus, self.q, motorEscmState) = struct.unpack("<BIxI", payload[35:45])
            
            self.motorStates = []
            for i in range(0, 8):
                self.motorStates.append((motorEscmState >> i * 4) & 0xf)
        return True

class FlightLimitArea(object):
    def __init__(self, lattitude, longitude, innerRadius, outerRadius, t):
        self.lattitude = lattitude
        self.longitude = longitude
        self.innerRadius = innerRadius
        self.outerRadius = outerRadius
        self.type = t
    
class FlycGetPushForbidStatus(FieldsDumpable, BaseCommand):
    _FIELDS = ("flightLimitAreaState", "flightLimitActionEvent", "#areas",)
    
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)
        self.flightLimitAreaState = self.flightLimitActionEvent = self.areas = None
        
    def parseImpl(self, payload):
        (self.flightLimitAreaState, self.flightLimitActionEvent, nAreas) = struct.unpack("<BBB", payload[0:3])
        
        if len(payload) < 3 + nAreas * 17:
            nAreas = (len(payload) - 3) / 17
            print "invalid nAreas value, clamping to %d" % nAreas
        
        self.areas = []
        for i in range(0, nAreas):
            startAt = 3 + i * 17
            (lattitude, longitude, innerRadius, outerRadius, t) = struct.unpack("<IIIIB", payload[startAt : startAt+17])
            self.areas.append( FlightLimitArea(lattitude, longitude, innerRadius, outerRadius, t) )
            
        return True
    
class FlycUnknownf8(BaseCommand):
    pass

class FlycGetPushLimitState(BaseCommand):
    pass

class FlycSetDate(FieldsDumpable, BaseCommand):
    _REQ_FIELDS = ("date",)
    _IS_PUSH_COMMAND = False
    
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)
        self.date = None
    
    def hasByte11InResponse(self):
        return True

    def parseImpl(self, payload):
        if not self.isResponse and len(payload) >= 7:
            (hour, minutes, second, year, month, day) = struct.unpack("<BBBHBB", payload[0:7])
            self.date = datetime(year, month, day, hour, minutes, second)
        return True
    
    
class FlyForbidArea():
    def __init__(self, countryCode, areaId, lat, longi, radius, t):
        self.countryCode = countryCode
        self.id = areaId
        self.latitude = lat
        self.longitude = longi
        self.radius = radius
        self.type = t
        
class FlycSetFlyForbidAreaData(FieldsDumpable, BaseCommand):
    _REQ_FIELDS = ("areaType", "#areas",)
    _IS_PUSH_COMMAND = False
    
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)
        self.areaType = None
        self.areas = None
    
    def parseImpl(self, payload):
        if not self.isResponse and len(payload) >= 4:
            (nAreas, self.areaType) = struct.unpack("<BB", payload[0:2])
            
            possibleArea = (len(payload) - 5) / 17
            if nAreas > possibleArea:
                print "clamping number of areas from %d to %d" % (nAreas, possibleArea)
                nAreas = possibleArea
            
            self.areas = []
            for i in range(0, nAreas):
                startAt = 5 + i * 17;
                (lat, longi, radius, country, t, areaId) = struct.unpack("<IIHHBI", payload[startAt : startAt+17])
                self.areas.append(FlyForbidArea(country, areaId, lat, longi, radius, t))
                
        return True
