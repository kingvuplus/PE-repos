from boxbranding import getBoxType, getImageVersion
import sys
import os
import time

def getVersionString():
    return getImageVersion()


def getEnigmaVersionString():
    import enigma
    enigma_version = enigma.getEnigmaVersionString()
    if '-(no branch)' in enigma_version:
        enigma_version = enigma_version[:-12]
    return enigma_version


def getKernelVersionString():
    try:
        f = open('/proc/version', 'r')
        kernelversion = f.read().split(' ', 4)[2].split('-', 2)[0]
        f.close()
        return kernelversion
    except:
        return _('unknown')


def getHardwareTypeString():
    try:
        if os.path.isfile('/proc/stb/info/boxtype'):
            return open('/proc/stb/info/boxtype').read().strip().lower()
        if os.path.isfile('/proc/stb/info/vumodel'):
            return open('/proc/stb/info/vumodel').read().strip().lower()
        if os.path.isfile('/proc/stb/info/hwmodel'):
            return open('/proc/stb/info/hwmodel').read().strip().lower()
        if os.path.isfile('/proc/stb/info/gbmodel'):
            return open('/proc/stb/info/gbmodel').read().strip().lower()
        if os.path.isfile('/proc/stb/info/gmmodel'):
            return open('/proc/stb/info/gmmodel').read().strip().lower()
        if os.path.isfile('/proc/stb/info/azmodel'):
            return open('/proc/stb/info/model').read().strip().lower()
        if os.path.isfile('/proc/stb/info/model'):
            return open('/proc/stb/info/model').read().strip().lower()
    except:
        pass

    return _('unavailable')


def getChipSetString():
    try:
        f = open('/proc/stb/info/chipset', 'r')
        chipset = f.read()
        f.close()
        return str(chipset.lower().replace('\n', '').replace('bcm', ''))
    except IOError:
        return 'unavailable'


def getBrandString():
    try:
        if getBoxType().startswith('ebox'):
            brand = 'EBox'
            return brand
        if getBoxType().startswith('dm'):
            brand = 'DreamBox'
            return brand
        if getBoxType().startswith('et'):
            brand = 'Xtrend'
            return brand
        if getBoxType().startswith('gb'):
            brand = 'GigaBlue'
            return brand
        if getBoxType().startswith('ios') or getBoxType().startswith('force'):
            brand = 'iqON'
            return brand
        if getBoxType().startswith('opti'):
            brand = 'Edision'
            return brand
        if getBoxType().startswith('ixuss'):
            brand = 'IXUSS'
            return brand
        if getBoxType().startswith('tm'):
            brand = 'Technomate'
            return brand
        if getBoxType().startswith('odin') or getBoxType().startswith('e3'):
            brand = 'Odin'
            return brand
        if getBoxType().startswith('vu'):
            brand = 'VuPlus'
            return brand
        if getBoxType().startswith('xp'):
            brand = 'MaxDigital'
            return brand
        if getBoxType().startswith('media'):
            brand = 'Jepssen'
            return brand
        if getBoxType().startswith('sog'):
            brand = 'Sogno'
            return brand
        if getBoxType().startswith('cube'):
            brand = 'E2BMC'
            return brand
        if getBoxType().startswith('spar'):
            brand = 'Spark'
            return brand
        if getBoxType().startswith('su'):
            brand = 'Golden Media'
            return brand
        if getBoxType().startswith('mb'):
            brand = 'MiracleBox'
            return brand
        if getBoxType().startswith('az'):
            brand = 'AZBox'
            return brand
        if getBoxType().startswith('en'):
            brand = 'Evo'
            return brand
        if model.startswith('ini'):
            if model.endswith('sv'):
                brand = 'MiracleBox'
            elif model.endswith('de'):
                brand = 'Golden Interstar'
            elif model.endswith('ru'):
                brand = 'Sezam'
            else:
                brand = 'Venton'
            return brand
    except:
        pass

    return _('unavailable')


def getCPUString():
    try:
        file = open('/proc/cpuinfo', 'r')
        lines = file.readlines()
        for x in lines:
            splitted = x.split(': ')
            if len(splitted) > 1:
                splitted[1] = splitted[1].replace('\n', '')
                if splitted[0].startswith('system type'):
                    system = splitted[1].split(' ')[0]

        file.close()
        return system
    except IOError:
        return 'unavailable'


def getCpuCoresString():
    try:
        file = open('/proc/cpuinfo', 'r')
        lines = file.readlines()
        for x in lines:
            splitted = x.split(': ')
            if len(splitted) > 1:
                splitted[1] = splitted[1].replace('\n', '')
                if splitted[0].startswith('processor'):
                    if int(splitted[1]) > 0:
                        cores = 2
                    else:
                        cores = 1

        file.close()
        return cores
    except IOError:
        return 'unavailable'


def getImageTypeString():
    try:
        return open('/etc/issue').readlines()[-2].capitalize().strip()[:-6]
    except:
        pass

    return _('undefined')


about = sys.modules[__name__]
