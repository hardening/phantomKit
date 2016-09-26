from protocol import cmdset0, cmdsetrc, cmdsetwifi, cmdsetspecial, cmdsetdm368,\
    cmdsetcamera, cmdsetbattery, cmdsetflyc, cmdsetgimbal, cmdsetosd

CMD_SETS = {
    0x00: {
        0x01: cmdset0.GetVersion,
        0x0e: cmdset0.Ping,
        0x26: cmdset0.ZeroUnknown0x26,
        0x32: cmdset0.ActiveStatus,
        0x4a: cmdset0.SetDate,
        0xf1: cmdset0.GetPushCheckStatus,
        0xff: cmdset0.GetDeviceInfo,
    },
            
    0x01: {
        0x01: cmdsetspecial.DataSpecialControl,
    },

    0x02: {
        0x10: cmdsetcamera.CameraSetMode,
        0x54: cmdsetcamera.CameraSetDate,
        0x6a: cmdsetcamera.CameraSetPhotoMode,
        0x80: cmdsetcamera.CameraGetPushStateInfo,
        0x81: cmdsetcamera.CameraGetPushShotParams,
    },
            
    0x03: {
        0x09: cmdsetflyc.FlycGetPushForbidStatus,
        0x1c: cmdsetflyc.FlycSetDate,
        0x2a: cmdsetflyc.FlycFunctionControl,
        0x32: cmdsetflyc.FlycGetPushDeformStatus,
        0x34: cmdsetflyc.FlycGetPlaneName,
        0x3d: cmdsetflyc.FlycSetTimeZone,
        0x3f: cmdsetflyc.FlycSetFlyForbidAreaData,
        0x42: cmdsetflyc.FlycGetPushUnlimitState,
        0x43: cmdsetflyc.OsdGetPushCommon,
        0x44: cmdsetflyc.OsdGetPushHome,
        0x51: cmdsetflyc.FlycGetPushSmartBattery,
        0x55: cmdsetflyc.FlycGetPushLimitState,
        0x56: cmdsetflyc.FlycGetPushLedStatus,
        0x67: cmdsetflyc.FlycGetPushPowerParams,
        0xf8: cmdsetflyc.FlycUnknownf8,
    },
            
    0x04: {
        0x05: cmdsetgimbal.DataGimbalGetPushParams,
    },
    
    0x05: {
        0x05: cmdsetbattery.SetBatteryCommon,
        0x06: cmdsetbattery.GetPushBatteryCommon,
        0x31: cmdsetbattery.CenterGetSelfDischarge,
        0x33: cmdsetbattery.GetBoardNumber,
    },
            
    0x06: {
        0x05: cmdsetrc.DataRcGetPushParams,
        0x0f: cmdsetrc.DataRcSetSearchMode,
        0x1a: cmdsetrc.DataRcGetControlMode,
        0x1b: cmdsetrc.DataRcGetPushGpsInfo,
        0x1e: cmdsetrc.DataRcGetPushBatteryInfo,
        0x20: cmdsetrc.DataRcSetPowerMode,
        0x2e: cmdsetrc.DataRcGetCustomFunction,
        0x34: cmdsetrc.DataRcGetWheelGain,
        0x36: cmdsetrc.DataRcGetGimbalCtrlMode,
    },
            
    0x07: {
        0x01: cmdsetwifi.DataWifiUnknown1,
        0x07: cmdsetwifi.DataWifiGetSSID,
        0x0e: cmdsetwifi.DataWifiGetPassword,
        0x09: cmdsetwifi.DataWifiGetPushSignal,
        0x11: cmdsetwifi.DataWifiGetPushFirstAppMac,
        0x12: cmdsetwifi.DataWifiGetPushElecSignal,
        0x13: cmdsetwifi.DataWifiSetPowerMode,
    },
    
    0x08: {
        0x01: cmdsetdm368.Dm368SetGParams,
    },
            
    0x09: {
        0x08: cmdsetosd.OsdGetPushSignalQuality,
    },
}

def getCommandInstance(packet):
    s = CMD_SETS.get(packet.cmdSetId, None)
    if not s:
        return None
    
    ctor = s.get(packet.cmdId, None)
    if not ctor:
        return None
    
    return ctor(packet)
