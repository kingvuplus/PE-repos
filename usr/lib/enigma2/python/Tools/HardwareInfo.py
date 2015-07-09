from boxbranding import getBoxType
from Components.About import *

class HardwareInfo:
    device_name = None
    device_version = None

    def __init__(self):
        if HardwareInfo.device_name is not None:
            return
        HardwareInfo.device_name = 'unknown'
        try:
            file = open('/proc/stb/info/model', 'r')
            HardwareInfo.device_name = file.readline().strip()
            file.close()
            try:
                file = open('/proc/stb/info/version', 'r')
                HardwareInfo.device_version = file.readline().strip()
                file.close()
            except:
                pass

        except:
            print '----------------'
            print 'you should upgrade to new drivers for the hardware detection to work properly'
            print '----------------'
            print 'fallback to detect hardware via /proc/cpuinfo!!'
            try:
                rd = open('/proc/cpuinfo', 'r').read()
                if rd.find('Brcm4380 V4.2') != -1:
                    HardwareInfo.device_name = 'dm8000'
                    print 'dm8000 detected!'
                elif rd.find('Brcm7401 V0.0') != -1:
                    HardwareInfo.device_name = 'dm800'
                    print 'dm800 detected!'
                elif rd.find('MIPS 4KEc V4.8') != -1:
                    HardwareInfo.device_name = 'dm7025'
                    print 'dm7025 detected!'
            except:
                pass

    def get_device_name(self):
        return HardwareInfo.device_name

    def get_device_version(self):
        return HardwareInfo.device_version

    def has_hdmi(self):
        return getBoxType().startswith('ebox') or getBoxType().startswith('et') or getBoxType().startswith('spar') or getBoxType().startswith('cube') or getBoxType().startswith('su9') or getBoxType().startswith('sog') or getBoxType().startswith('gb') or getBoxType().startswith('ios') or getBoxType().startswith('opti') or getBoxType().startswith('ixuss') or getBoxType().startswith('odin') or getBoxType().startswith('e3') or getBoxType().startswith('tm') or getBoxType().startswith('force') or getBoxType().startswith('vu') or getBoxType().startswith('ini') or getBoxType().startswith('venton') or getBoxType().startswith('xp') or getBoxType().startswith('media') or getBoxType().startswith('az') or getBoxType().startswith('en') or getBoxType() == 'dm7020hd' or getBoxType() == 'dm7020hdv2' or getBoxType() == 'dm800se' or getBoxType() == 'dm800sev2' or getBoxType() == 'dm500hd' or getBoxType() == 'dm500hdv2' or getBoxType() == 'dm8000' and HardwareInfo.device_version != None

    def has_rca(self):
        return getBoxType() == 'gbquad' or getBoxType() == 'gbquadplus' or getBoxType() == 'et5x00' or getBoxType().startswith('ixuss') or getBoxType() == 'enfinity' or getBoxType() == 'force1' or getBoxType().startswith('e3') or getBoxType() == 'eboxlumi' or getBoxType() == 'ebox7358' or getBoxType() == 'tmnanooe' or getHardwareTypeString() == 'ultra' or getBoxType() == 'azboxme' or getBoxType() == 'azboxminime' or getBoxType().startswith('opti') or getBoxType() == 'gb800seplus' or getBoxType() == 'gb800ueplus' or getHardwareTypeString() == 'ini-1000ru' or getHardwareTypeString() == 'ini-1000sv' or getHardwareTypeString() == 'et6000'
