import protocol
from protocol import getCommandInstance, cmdsetflyc, cmdset0, cmdsetwifi
from protocol.djiprotocol import hexDump


if __name__ == '__main__':
    appStream = ''
    droneStream = ''
    
#    for l in open("/home/david/Bureau/todrone.txt", "r").readlines():
    #for l in open("../bigcapture_drone2.txt", "r").readlines():
    for l in open("../capture_portforward_drone.txt", "r").readlines():
        #    00000000  55 3f 04 8f 03 02 74 03  00 03 43 00 00 00 00 00   U?....t. ..C.....
        fromDrone = l.startswith("    ")
        
        if fromDrone:
            l = l[4:]
        
        pos = l.find("   ")
        bytesStr = l[8:pos]
        rawBytes = bytesStr.replace(" ", '').decode("hex")
        
        if fromDrone:
            droneStream += rawBytes
            toAnalyze = droneStream
        else:
            appStream += rawBytes
            toAnalyze = appStream
        
        while len(toAnalyze):
            (packet, remains) = protocol.djiprotocol.parseBuffer(toAnalyze)
            if fromDrone:
                droneStream = remains
            else:
                appStream = remains
            
            if packet is None:
                break
            
            command = getCommandInstance(packet)
            if command is None:
                print "%s Unknown command 0x%x/0x%x => %s" % (fromDrone and "DRONE" or "APP  ", packet.cmdSetId, packet.cmdId, hexDump(toAnalyze))
                toAnalyze = remains
                continue
            
            if not command.parse(toAnalyze):
                #print "parseImpl error on command 0x%x/0x%d" % (packet.cmdSetId, packet.cmdId)
                toAnalyze = remains
                continue
            
            #if isinstance(command, cmdsetflyc.DataFlycGetPushSmartBattery):
            #if isinstance(command, cmdset0.GetPushCheckStatus):
            #if isinstance(command, cmdsetflyc.OsdGetPushHome):
            if isinstance(command, cmdsetflyc.OsdGetPushCommon) or isinstance(command, cmdsetflyc.FlycFunctionControl):
            #if True:                
                print "%s %s" % (fromDrone and "DRONE" or "APP  ", command)
            
            toAnalyze = remains
            
        