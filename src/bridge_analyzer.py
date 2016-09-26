import sys
import protocol

if __name__ == "__main__":
    lineno = 0 
    #for l in sys.stdin.readlines():
    for l in open("misc_from_app.txt", "r").readlines():
        if not l:
            break
        lineno += 1
        if not l.startswith("RC"):
            continue
        
        fromRc = l[2] == '>'
        if not fromRc and False:
            print "%s" % l[0:-1]
            continue
        
        #                        [25:27] crc8
        #                          vv
        # RC> len=0014 == 55 0e 04 66
        #                    ^^
        #                  [19:21] packetLen
        crc8 = int(l[25:27], 16)
        packetLen = int(l[19:21], 16)
                
        cmdSet = int(l[43:45], 16)
        cmd = int(l[46:48], 16)
    
        # 55 13 04 03 1b 02 c7 1d 00 07 11
        allPacket = l[16:].replace(' ', '').replace("\n", '').decode('hex')[0:packetLen]
        
        eField = ord(allPacket[4]) >> 5
        senderType = ord(allPacket[4]) & 0x1f

        gField = ord(allPacket[5]) >> 5
        deviceType = ord(allPacket[5]) & 0x1f

        isResponse = (ord(allPacket[8]) & 0x80) != 0
        kField = ((ord(allPacket[8]) >> 5) & 0x03)
        lField = ord(allPacket[8]) & 0x07
        payload = l[49:-7].replace(" ", '').decode('hex')
        
        instance = protocol.getCommandInstance(cmdSet, cmd)
        if not instance:
            instance = protocol.djiprotocol.BaseCommand(cmdSet, cmd)
        
        if instance.hasByte11InResponse() and isResponse:
            payload = payload[1:]
        
        if not instance.parseImpl(payload):
            print "error parsing %s" % l[0:-1]
            continue
        
        toPrint = "%0.3d %s e=0x%x senderType=0x%0.2x g=0x%x deviceType=0x%0.2x " % (lineno, fromRc and "RC " or "APP", eField, senderType, gField, deviceType)
        toPrint += "isResp=%d k=%d l=%d" % (isResponse, kField, lField)  
        toPrint += "%s" % instance
        print toPrint
    
        