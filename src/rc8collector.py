import sys

if __name__ == "__main__":
    fromCrc8 = {}
    toCrc8 = {}
    
    for l in sys.stdin.readlines():
        if not l:
            break
        
        fromRc = l[2] == '>'
        
        #                        [25:27] crc8
        #                          vv
        # RC> len=0014 == 55 0e 04 66
        #                    ^^
        #                  [19:21] packetLen
        crc8 = int(l[25:27], 16)
        packetLen = int(l[19:21], 16)
        
        target = toCrc8
        if fromRc:
            target = fromCrc8
        
        if not target.has_key(packetLen):
            target[packetLen] = crc8
         
        if target[packetLen] != crc8:
            print "got changing value for crc8(0x%x)" % packetLen
    
    
    arr = []
    for k, v in fromCrc8.items():
        arr.append("0x%0.2x: 0x%0.2x" % (k, v))
    print "from remote = {%s}" % ", ".join(arr)
    
    arr = []
    for k, v in toCrc8.items():
        arr.append("0x%0.2x: 0x%0.2x" % (k, v))
    print "to remote = {%s}" % ", ".join(arr)
    