from protocol.djiprotocol import BaseCommand
from protocol.cmdset0 import SetDate
import struct
from protocol.cmdsetcommon import FieldsDumpable


class CameraSetDate(SetDate):
    pass

class CameraGetPushStateInfo(FieldsDumpable, BaseCommand):
    _FIELDS = ("sdcardState", "firmwareError", "j", "k", "l", "m", "encryptStatus",
            "o", "q", "r", "s", "fileIndexMode", "u", "v", "w", "x", "cameraType", "z", "mode",)
        
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)
        self.sdcardState = None
        self.firmwareError = None
        self.j = self.k = self.l = self.m = self.encryptStatus = self.o = None
        self.q = self.r = self.s = self.fileIndexMode = self.u = self.v = self.w = self.x = self.cameraType = self.z = None
        self.mode = None
    
    def parseImpl(self, payload):
        if len(payload) > 4:
            (flags, self.mode, self.q, self.r, self.s, self.fileIndexMode, uv) = struct.unpack("<IBxxxxIIIBB", payload[0:23])
            self.sdcardState = (flags >> 10) & 0xF
            self.firmwareError = (flags >> 15) & 0x3
            self.j = (flags >> 17) & 0x1 != 0
            self.k = (flags >> 18) & 0x1 != 0
            self.l = (flags >> 19) & 0x1 != 0
            self.m = (flags >> 20) & 0x1 != 0
            self.encryptStatus = (flags >> 23) & 0x3
            self.o = (flags >> 20) & 0x1 != 0
            self.u = (uv >> 7) == 1
            self.v = (uv & 0x7f)
            
            (self.w, x, self.cameraType, self.z) = struct.unpack("<HxBBxB", payload[29:36])
            self.x = (x & 0x1) != 0
        return True
        

class CameraGetPushShotParams(FieldsDumpable, BaseCommand):
    _FIELDS = ("panoMode", "exposureMode", "iso", "sizeType", "ratioType", )
    
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)
        self.panoMode = self.exposureMode = self.iso = self.sizeType = self.ratioType = None
    
    def parseImpl(self, payload):
        if len(payload) > 62:
            self.iso = ord(payload[5])
            self.sizeType = ord(payload[9])
            self.ratioType = ord(payload[9])
            self.panoMode = ord(payload[61])
            self.exposureMode = ord(payload[20])
        return True
    

class CameraSetMode(FieldsDumpable, BaseCommand):
    _IS_PUSH_COMMAND = False
    _REQ_FIELDS = ("mode",)
    
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)
        self.mode = None
    
    def parseImpl(self, payload):
        if not self.isResponse:
            self.mode = ord(payload[0])
            
        return True
    
class CameraSetPhotoMode(FieldsDumpable, BaseCommand):
    _IS_PUSH_COMMAND = False
    _REQ_FIELDS = ("photoType", "c", "d", "e", "f",)
    
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)
        self.photoType = self.c = self.d = self.e = self.f = None
    
    def parseImpl(self, payload):
        if not self.isResponse:
            (self.photoType, self.c, self.d, self.e, self.f) = struct.unpack("<BBBBH", payload[0:6])
            
        return True

    