import unittest
from protocol.djiprotocol import parseBuffer, Packet
from protocol import getCommandInstance, cmdsetcamera
from datetime import datetime

def unhexa(s):
    return s.replace(" ", '').decode('hex')
    
class Test(unittest.TestCase):
    


    def testParsing(self):
        # trivial correct packet
        payload = unhexa("55 0e 04 66 02 1b 22 18  80 00 0e 00 88 4d") 
        (packet, rest) = parseBuffer(payload)
        
        self.assertIsInstance(packet, Packet)
        self.assertEquals(rest, '')
        self.assertEquals(packet.sourceType, 'APP')
        self.assertEquals(packet.targetType, 'WIFI_G')
        self.assertTrue(packet.isResponse)

        # packet not completely there
        payload = unhexa("55 0e 04 66 02 1b 22 18  80 00 0e 00") 
        (packet, rest) = parseBuffer(payload)
        
        self.assertIsNone(packet)
        self.assertEquals(rest, payload)

        # some padding, and an invalid crc8 in front of the right one
        #                 [padding][invalid crc8] [good packet]                              [rest of the bytes ]
        payload = unhexa("00 00 00 55 0e 04 00 00 55 0e 04 66 02 1b 22 18  80 00 0e 00 88 4d 01 02 03 04 06 07 08")                       
        (packet, rest) = parseBuffer(payload)
        
        self.assertIsInstance(packet, Packet)
        self.assertEquals(rest, unhexa("01 02 03 04 06 07 08"))

        # invalid crc16
        #                                                     [invalid CRC16]  v v            [potential packet]
        payload = unhexa("55 0e 04 00 00 55 0e 04 66 02 1b 22 18  80 00 0e 00 5F 5F 00 00 00 55 0e")
        (packet, rest) = parseBuffer(payload)
        
        self.assertIsNone(packet)
        self.assertEquals(rest, unhexa("55 0e"))
        
    
    def testCameraRc(self):
        payload = unhexa("55 14 04 6d 02 01 14 00 40 02 54 e0 07 08 12 00 1d 20 f7 da") 
        (packet, rest) = parseBuffer(payload)
        
        self.assertEqual(rest, "")
        self.assertIsInstance(packet, Packet)
        
        command = getCommandInstance(packet)
        self.assertIsInstance(command, cmdsetcamera.CameraSetDate)
        self.assertTrue(command.parse(payload))
        self.assertEquals(command.date, datetime(2016, 8, 18, 0, 29, 32) )
        




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testParsing']
    unittest.main()