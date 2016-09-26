from djiprotocol import BaseCommand
from protocol.cmdsetcommon import FieldsDumpable

class Dm368SetGParams(FieldsDumpable, BaseCommand):
    _IS_PUSH_COMMAND = False
    _REQ_FIELDS = ('subCmdId', 'value',)
    
    def __init__(self, packet):
        BaseCommand.__init__(self, packet)
        self.subCmdId = None
        self.value = None

    def parseImpl(self, payload):
        if not self.isResponse and len(payload) >= 3:
            self.subCmdId = ord(payload[0])
            self.value = ord(payload[2])
            
        return True
    
