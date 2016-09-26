from djiprotocol import BaseCommand
from protocol.djiprotocol import StringGetterCommand
from protocol.cmdsetcommon import SetPowerMode, FieldsDumpable

class DataWifiUnknown1(BaseCommand):
    pass

class DataWifiGetSSID(StringGetterCommand):        
    def hasByte11InResponse(self):
        return True

    
class DataWifiGetPassword(StringGetterCommand):
    def hasByte11InResponse(self):
        return True


class DataWifiGetPushFirstAppMac(FieldsDumpable, BaseCommand):
    _FIELDS = ('macAddr', )
    
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)
        self.macAddr = None
        
    def parseImpl(self, payload):
        if len(payload) < 6:
            return False

        arr = []
        for i in range(0, 6):
            arr.append("%0.2x" % ord(payload[i]))
        self.macAddr = ":".join(arr)
        return True

    def __str__(self, *args, **kwargs):
        return "<DataWifiGetPushFirstAppMac macAddr=%s>" % self.macAddr 


class DataWifiGetPushSignal(BaseCommand):
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)
        self.signal = None
        
    def parseImpl(self, payload):
        if len(payload) < 1:
            return False
        
        self.signal = ord(payload[0])
        return True

    def __str__(self, *args, **kwargs):
        return "<DataWifiGetPushSignal signal=%d>" % self.signal 



class DataWifiGetPushElecSignal(BaseCommand):
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)
        self.elecSignal = None

    def parseImpl(self, payload):
        if len(payload) < 1:
            return False
        
        self.elecSignal = ord(payload[0])
        return True

    def __str__(self, *args, **kwargs):
        return "<DataWifiGetPushElecSignal signal=%d>" % self.elecSignal
    
class DataWifiSetPowerMode(SetPowerMode):
    pass

