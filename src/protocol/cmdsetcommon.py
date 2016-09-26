from protocol.djiprotocol import BaseCommand

class FieldsDumpable(object):
    _FIELDS = ()
    _REQ_FIELDS = ()
    _RESP_FIELDS = ()
    _IS_PUSH_COMMAND = True
    
    def dumpFields(self, fields):
        arr = [] 
        for f in fields:
            fname = f
            if f.startswith("#"):
                fname = f[1:]
                
            v = getattr(self, fname)
            if f.startswith("#"):
                strVal = "%s" % len(v)
            elif isinstance(v, list):
                tokens = []
                for item in v:
                    tokens.append("%s" % item)
                strVal = "[" + ",".join(tokens) + "]"
            else:
                strVal = v
                
            arr.append("%s=%s" % (f, strVal))
        return " ".join(arr)
    
    def __str__(self, *args, **kwargs):
        ret = "<%s" % self.__class__.__name__
        if not self._IS_PUSH_COMMAND:
            if self.packet.isResponse:
                ret += "Resp " + self.dumpFields(self._RESP_FIELDS)
            else: 
                ret += "Req " + self.dumpFields(self._REQ_FIELDS)
        else:
            ret += " " + self.dumpFields(self._FIELDS)
        return ret + ">"


class SetPowerMode(FieldsDumpable, BaseCommand):
    _IS_PUSH_COMMAND = False
    _REQ_FIELDS = ("powerMode",)
    
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)
        self.powerMode = None
        
    def parseImpl(self, payload):
        if not self.isResponse and len(payload) > 0:
            self.powerMode = ord(payload[0])
            
        return True


