import struct
from djiprotocol import BaseCommand
from protocol.cmdsetcommon import SetPowerMode, FieldsDumpable

class ChannelCustomModel(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b 
        

class DataRcGetControlMode(FieldsDumpable, BaseCommand):
    _RESP_FIELDS = ('controlMode', '#customChannels')
    _IS_PUSH_COMMAND = False
    
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)
        self.controlMode = None
        self.customChannels = None
    
    def parseImpl(self, payload):
        if self.isResponse:
            self.controlMode = ord(payload[0])
            
            if len(payload) >= 5:
                self.customChannels = []
                for i in range(1, 5):
                    i = ord(payload[i])
                    self.customChannels.append( ChannelCustomModel(i & 0x80 != 0, i & 0x7f) )
            
        return True
  

class DataRcGetCustomFunction(BaseCommand):
    pass
    
    
class DataRcSetSearchMode(BaseCommand):
    pass
    
class DataRcGetGimbalCtrlMode(BaseCommand):
    pass
        
class DataRcGetWheelGain(FieldsDumpable, BaseCommand):
    _RESP_FIELDS = ("gain",)
    _IS_PUSH_COMMAND = False
    
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)
        self.gain = None

    def parseImpl(self, payload):
        if len(payload):
            self.gain = ord(payload[0])
        return True
    
    
class DataRcGetPushBatteryInfo(FieldsDumpable, BaseCommand):
    _FIELDS = ("batteryLevel",)
    
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)
        self.batteryLevel = None
    
    def parseImpl(self, payload):
        if len(payload) < 5:
            return False
        
        self.batteryLevel = ord(payload[4])
        return True
    

class DataRcGetPushParams(FieldsDumpable, BaseCommand):
    _FIELDS = ("rstick_x", "rstick_y", "lstick_x", "lstick_y", "gimble", "f", "g", 
               "h", "videoRecord", "takePhoto", "ioc_mode", "l", "p_mode", "bandwidth", )
    
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)
        self.rstick_x = None
        self.rstick_y = None
        self.lstick_x = None
        self.lstick_y = None
        self.gimble = None
        self.f = None
        self.g = None
        self.h = None
        self.videoRecord = None
        self.takePhoto = None
        self.ioc_mode = None
        self.l = None
        self.p_mode = None
        self.bandwidth = None
    
    def parseImpl(self, payload):
        if len(payload) < 13:
            return False
        
        (self.rstick_x, self.rstick_y, self.lstick_x, self.lstick_y, 
         self.gimble, fgh, ijklm, self.bandwidth) = struct.unpack("<hhhhhBBB", payload[0:13])
        self.f = (fgh & 0x80) != 0
        self.g = (fgh & 0x40) != 0
        self.h = (fgh & 0x3E) >> 1
        
        self.videoRecord = (ijklm & 0x80) != 0
        self.takePhoto = (ijklm & 0x40) != 0
        self.ioc_mode = (ijklm & 0x20) != 0
        self.p_mode = (ijklm & 0x10) != 0
        self.l = (ijklm & 0x08) != 0
        return True
    

        
class DataRcGetPushGpsInfo(FieldsDumpable, BaseCommand):
    _FIELDS = ("a", "b", "c",)
    
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)
        self.a = None
        self.b = None
        self.c = None

    def parseImpl(self, payload):
        if len(payload) < 30:
            return False
        
        self.a = struct.unpack("<i", payload[7:11])[0]
        self.b = struct.unpack("<i", payload[11:15])[0]
        self.c = struct.unpack("<h", payload[28:30])[0]
        return True

class DataRcSetPowerMode(SetPowerMode):
    pass


