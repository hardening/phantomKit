import struct
from protocol import crc8
import crc16

PHANTOM3_MAGIC = '\x55'
PHANTOM3_PROTOCOL_VERSION = 1

def hexDump(buf):
    arr = []
    for b in buf:
        arr.append("%0.2x" % ord(b))
    return " ".join(arr)


class BaseCommand(object):
    def __init__(self, packet):
        self.cmdSetId = packet.cmdSetId
        self.cmdId = packet.cmdId
        self.isResponse = packet.isResponse
        self.packet = packet
        self.dump = None
    
    def parse(self, payload):
        dataPayload = payload[11:-2]
        
        if self.packet.isResponse and self.hasByte11InResponse():
            dataPayload = dataPayload[1:]

        strPayload = hexDump(payload)
        strDataPayload = hexDump(dataPayload)
        
        if (self.cmdSetId in [2, 3]) and len(dataPayload) and ord(dataPayload[0]) == self.packet.magic:
            return False
        
        return self.parseImpl(dataPayload)
        
    def parseImpl(self, payload):
        self.dump = hexDump(payload)
        return True
    
    def hasByte11InResponse(self):
        return False
    
    def __str__(self, *args, **kwargs):
        return "<%s%s(set=0x%x cmd=0x%x) %s>" % (self.__class__.__name__, self.isResponse and "Resp" or "Req",
                        self.cmdSetId, self.cmdId, self.dump)

class StringGetterCommand(BaseCommand):
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)
        self.str = None
        
    def parseImpl(self, payload):
        if len(payload):
            strlen = ord(payload[0])
            self.str = payload[1:strlen]
        return True
        
    def __str__(self, *args, **kwargs):
        s = "<%s" % self.__class__.__name__
        if self.isResponse:
            return s + "Resp str=%s>" % self.str
        else:
            return s + "Req>"


PARSE_OK, PARSE_ERROR, PARSE_NEED_MORE = range(0, 3)

def parseBuffer(buf):
    while True:
        pos = buf.find(PHANTOM3_MAGIC)
        if pos < 0:
            return (None, '')
        
        buf = buf[pos:]
        
        if len(buf) < 4:
            return (None, buf)
    
        (magic, lenVer, crc8val) = struct.unpack("<BhB", buf[0:4])
    
        packetLen = lenVer & 0x3ff
        version = lenVer >> 10
        
        if crc8.compute_crc8(buf[0:3], crc8.CRC8_INIT) != crc8val:
            buf = buf[4:]
            continue
            
        if version != PHANTOM3_PROTOCOL_VERSION:
            buf = buf[4:]
            continue
        
        if len(buf) < 4:
            buf = buf[4:]
            continue
        
        if len(buf) < packetLen:
            return (None, buf)
        
        packetMinusCrc = buf[0 : packetLen-2]
        crc16val = ord(buf[packetLen-2]) | ord(buf[packetLen-1]) << 8
        if crc16.Get_CRC16_Check_Sum(packetMinusCrc, crc16.CRC_INIT) != crc16val:
            buf = buf[packetLen:]
            continue
        
        packet = Packet(magic, version)
        if not packet.parse(packetMinusCrc):
            buf = buf[packetLen:]
            continue
        
        return (packet, buf[packetLen:])
            
         
DEVICE_TYPES = [
    "WHO", "CAMERA", "APP", "FLYC", "GIMBAL", "CENTER", "RC", "WIFI", "DM368", "OFDM", 
    "PC",  "BATTERY", "DIGITAL", "DM368_G", "OSD", "TRANSFORM", "TRANSFORM_G", "SINGLE", "DOUBLE", "FPGA",
    "FPGA_G", None, None, None, None, None, None, "WIFI_G", None, None,
    None, "BROADCAST",
] 
 
def getDeviceType(t):
    if t == 100:
        return "OTHER"    
    if t >= len(DEVICE_TYPES):
        return None
    
    return DEVICE_TYPES[t]
    
         

class Packet(object):
    def __init__(self, magic=PHANTOM3_MAGIC, version=PHANTOM3_PROTOCOL_VERSION):    
        self.magic = magic
        self.version = version
        self.sourceType = None
        self.targetType = None
        self.seqNumber = None
        self.isResponse = None
        self.cmdSetId = None
        self.cmdId = None
        self.k = None
        self.l = None
        
    def parse(self, payload):
        if len(payload) < 11:
            return False

        self.sourceType = getDeviceType(ord(payload[4]) & 0x1f)
        self.sourceSubType = ord(payload[4]) >> 5 
        self.targetType = getDeviceType(ord(payload[5]) & 0x1f)
        self.targetSubType = ord(payload[5]) >> 5
        self.seqNumber = struct.unpack("<B", payload[6:7])[0]
        self.isResponse = (ord(payload[8]) & 0x80) > 0
        self.k = (ord(payload[8]) >> 5) & 0x03
        self.l = ord(payload[8]) & 0x07
        self.cmdSetId = ord(payload[9])
        self.cmdId = ord(payload[10])
        return True
    
    

