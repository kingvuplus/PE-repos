from config import config, ConfigSlider, ConfigSelection, ConfigYesNo, ConfigEnableDisable, ConfigSubsection, ConfigBoolean, ConfigSelectionNumber, ConfigNothing, NoSave
from enigma import eAVSwitch, getDesktop
from boxbranding import getBoxType
from Components.About import *
from SystemInfo import SystemInfo
import os
config.av = ConfigSubsection()

class AVSwitch:

    def setInput(self, input):
        INPUT = {'ENCODER': 0,
         'SCART': 1,
         'AUX': 2}
        eAVSwitch.getInstance().setInput(INPUT[input])

    def setColorFormat(self, value):
        eAVSwitch.getInstance().setColorFormat(value)

    def setAspectRatio(self, value):
        eAVSwitch.getInstance().setAspectRatio(value)

    def setSystem(self, value):
        eAVSwitch.getInstance().setVideomode(value)

    def getOutputAspect(self):
        valstr = config.av.aspectratio.value
        if valstr in ('4_3_letterbox', '4_3_panscan'):
            return (4, 3)
        if valstr == '16_9':
            try:
                aspect_str = open('/proc/stb/vmpeg/0/aspect', 'r').read()
                if aspect_str == '1':
                    return (4, 3)
            except IOError:
                pass

        elif valstr in ('16_9_always', '16_9_letterbox'):
            pass
        elif valstr in ('16_10_letterbox', '16_10_panscan'):
            return (16, 10)
        return (16, 9)

    def getFramebufferScale(self):
        aspect = self.getOutputAspect()
        fb_size = getDesktop(0).size()
        return (aspect[0] * fb_size.height(), aspect[1] * fb_size.width())

    def getAspectRatioSetting(self):
        valstr = config.av.aspectratio.value
        if valstr == '4_3_letterbox':
            val = 0
        elif valstr == '4_3_panscan':
            val = 1
        elif valstr == '16_9':
            val = 2
        elif valstr == '16_9_always':
            val = 3
        elif valstr == '16_10_letterbox':
            val = 4
        elif valstr == '16_10_panscan':
            val = 5
        elif valstr == '16_9_letterbox':
            val = 6
        return val

    def setAspectWSS(self, aspect = None):
        if not config.av.wss.value:
            value = 2
        else:
            value = 1
        eAVSwitch.getInstance().setWSS(value)


iAVSwitch = AVSwitch()

def InitAVSwitch():
    if getBoxType() == 'vuduo' or getBoxType().startswith('ixuss'):
        config.av.yuvenabled = ConfigBoolean(default=False)
    else:
        config.av.yuvenabled = ConfigBoolean(default=True)
    colorformat_choices = {'cvbs': _('CVBS'),
     'rgb': _('RGB'),
     'svideo': _('S-Video')}
    if config.av.yuvenabled.getValue():
        colorformat_choices['yuv'] = _('YPbPr')
    config.av.colorformat = ConfigSelection(choices=colorformat_choices, default='rgb')
    config.av.aspectratio = ConfigSelection(choices={'4_3_letterbox': _('4:3 Letterbox'),
     '4_3_panscan': _('4:3 PanScan'),
     '16_9': _('16:9'),
     '16_9_always': _('16:9 always'),
     '16_10_letterbox': _('16:10 Letterbox'),
     '16_10_panscan': _('16:10 PanScan'),
     '16_9_letterbox': _('16:9 Letterbox')}, default='16_9')
    config.av.aspect = ConfigSelection(choices={'4_3': _('4:3'),
     '16_9': _('16:9'),
     '16_10': _('16:10'),
     'auto': _('Automatic')}, default='auto')
    policy2_choices = {'letterbox': _('Letterbox'),
     'panscan': _('Pan&scan'),
     'scale': _('Just scale')}
    if os.path.exists('/proc/stb/video/policy2_choices') and 'auto' in open('/proc/stb/video/policy2_choices').readline():
        policy2_choices.update({'auto': _('Auto')})
    config.av.policy_169 = ConfigSelection(choices=policy2_choices, default='scale')
    policy_choices = {'pillarbox': _('Pillarbox'),
     'panscan': _('Pan&scan'),
     'nonlinear': _('Nonlinear'),
     'scale': _('Just scale')}
    if os.path.exists('/proc/stb/video/policy_choices') and 'auto' in open('/proc/stb/video/policy_choices').readline():
        policy_choices.update({'auto': _('Auto')})
    config.av.policy_43 = ConfigSelection(choices=policy_choices, default='scale')
    config.av.tvsystem = ConfigSelection(choices={'pal': _('PAL'),
     'ntsc': _('NTSC'),
     'multinorm': _('multinorm')}, default='pal')
    config.av.wss = ConfigEnableDisable(default=True)
    config.av.generalAC3delay = ConfigSelectionNumber(-1000, 1000, 5, default=0)
    config.av.generalPCMdelay = ConfigSelectionNumber(-1000, 1000, 5, default=0)
    config.av.vcrswitch = ConfigEnableDisable(default=False)

    def setColorFormat(configElement):
        if getBoxType() == 'et6x00':
            map = {'cvbs': 3,
             'rgb': 3,
             'svideo': 2,
             'yuv': 3}
        elif getBoxType() == 'gbquad' or getBoxType() == 'gbquadplus' or getBoxType().startswith('et'):
            map = {'cvbs': 0,
             'rgb': 3,
             'svideo': 2,
             'yuv': 3}
        else:
            map = {'cvbs': 0,
             'rgb': 1,
             'svideo': 2,
             'yuv': 3}
        iAVSwitch.setColorFormat(map[configElement.getValue()])

    def setAspectRatio(configElement):
        map = {'4_3_letterbox': 0,
         '4_3_panscan': 1,
         '16_9': 2,
         '16_9_always': 3,
         '16_10_letterbox': 4,
         '16_10_panscan': 5,
         '16_9_letterbox': 6}
        iAVSwitch.setAspectRatio(map[configElement.value])

    def setSystem(configElement):
        map = {'pal': 0,
         'ntsc': 1,
         'multinorm': 2}
        iAVSwitch.setSystem(map[configElement.value])

    def setWSS(configElement):
        iAVSwitch.setAspectWSS()

    config.av.colorformat.addNotifier(setColorFormat)
    config.av.aspectratio.addNotifier(setAspectRatio)
    config.av.tvsystem.addNotifier(setSystem)
    config.av.wss.addNotifier(setWSS)
    iAVSwitch.setInput('ENCODER')
    if getBoxType() in ('gbquad', 'gbquadplus', 'et5x00', 'ixussone', 'ixusszero', 'omtimussos1', 'omtimussos2', 'gb800seplus', 'gb800ueplus') or getHardwareTypeString() == 'et6000':
        detected = False
    else:
        detected = eAVSwitch.getInstance().haveScartSwitch()
    SystemInfo['ScartSwitch'] = detected
    if os.path.exists('/proc/stb/hdmi/bypass_edid_checking'):
        f = open('/proc/stb/hdmi/bypass_edid_checking', 'r')
        can_edidchecking = f.read().strip().split(' ')
        f.close()
    else:
        can_edidchecking = False
    SystemInfo['Canedidchecking'] = can_edidchecking
    if can_edidchecking:

        def setEDIDBypass(configElement):
            try:
                f = open('/proc/stb/hdmi/bypass_edid_checking', 'w')
                f.write(configElement.value)
                f.close()
            except:
                pass

        config.av.bypass_edid_checking = ConfigSelection(choices={'00000000': _('off'),
         '00000001': _('on')}, default='00000000')
        config.av.bypass_edid_checking.addNotifier(setEDIDBypass)
    else:
        config.av.bypass_edid_checking = ConfigNothing()
    if os.path.exists('/proc/stb/audio/3d_surround_choices'):
        f = open('/proc/stb/audio/3d_surround_choices', 'r')
        can_3dsurround = f.read().strip().split(' ')
        f.close()
    else:
        can_3dsurround = False
    SystemInfo['Can3DSurround'] = can_3dsurround
    if can_3dsurround:

        def set3DSurround(configElement):
            f = open('/proc/stb/audio/3d_surround', 'w')
            f.write(configElement.value)
            f.close()

        choice_list = [('none', _('off')),
         ('hdmi', _('HDMI')),
         ('spdif', _('SPDIF')),
         ('dac', _('DAC'))]
        config.av.surround_3d = ConfigSelection(choices=choice_list, default='none')
        config.av.surround_3d.addNotifier(set3DSurround)
    else:
        config.av.surround_3d = ConfigNothing()
    try:
        can_pcm_multichannel = os.access('/proc/stb/audio/multichannel_pcm', os.W_OK)
    except:
        can_pcm_multichannel = False

    SystemInfo['supportPcmMultichannel'] = can_pcm_multichannel
    if can_pcm_multichannel:

        def setPCMMultichannel(configElement):
            open('/proc/stb/audio/multichannel_pcm', 'w').write(configElement.value and 'enable' or 'disable')

        config.av.pcm_multichannel = ConfigYesNo(default=False)
        config.av.pcm_multichannel.addNotifier(setPCMMultichannel)
    try:
        f = open('/proc/stb/audio/ac3_choices', 'r')
        file = f.read()[:-1]
        f.close()
        can_downmix_ac3 = 'downmix' in file
    except:
        can_downmix_ac3 = False

    SystemInfo['CanDownmixAC3'] = can_downmix_ac3
    if can_downmix_ac3:

        def setAC3Downmix(configElement):
            f = open('/proc/stb/audio/ac3', 'w')
            f.write(configElement.value and 'downmix' or 'passthrough')
            f.close()
            if SystemInfo.get('supportPcmMultichannel', False) and not configElement.value:
                SystemInfo['CanPcmMultichannel'] = True
            else:
                SystemInfo['CanPcmMultichannel'] = False
                if can_pcm_multichannel:
                    config.av.pcm_multichannel.setValue(False)

        config.av.downmix_ac3 = ConfigYesNo(default=True)
        config.av.downmix_ac3.addNotifier(setAC3Downmix)
    try:
        f = open('/proc/stb/audio/aac_choices', 'r')
        file = f.read()[:-1]
        f.close()
        can_downmix_aac = 'downmix' in file
    except:
        can_downmix_aac = False

    SystemInfo['CanDownmixAAC'] = can_downmix_aac
    if can_downmix_aac:

        def setAACDownmix(configElement):
            f = open('/proc/stb/audio/aac', 'w')
            f.write(configElement.value and 'downmix' or 'passthrough')
            f.close()

        config.av.downmix_aac = ConfigYesNo(default=True)
        config.av.downmix_aac.addNotifier(setAACDownmix)
    if os.path.exists('/proc/stb/audio/avl_choices'):
        f = open('/proc/stb/audio/avl_choices', 'r')
        can_autovolume = f.read().strip().split(' ')
        f.close()
    else:
        can_autovolume = False
    SystemInfo['CanAutoVolume'] = can_autovolume
    if can_autovolume:

        def setAutoVulume(configElement):
            f = open('/proc/stb/audio/avl', 'w')
            f.write(configElement.value)
            f.close()

        choice_list = [('none', _('off')),
         ('hdmi', _('HDMI')),
         ('spdif', _('SPDIF')),
         ('dac', _('DAC'))]
        config.av.autovolume = ConfigSelection(choices=choice_list, default='none')
        config.av.autovolume.addNotifier(setAutoVulume)
    else:
        config.av.autovolume = ConfigNothing()
    try:
        can_osd_alpha = open('/proc/stb/video/alpha', 'r') and True or False
    except:
        can_osd_alpha = False

    SystemInfo['CanChangeOsdAlpha'] = can_osd_alpha

    def setAlpha(config):
        open('/proc/stb/video/alpha', 'w').write(str(config.value))

    if can_osd_alpha:
        config.av.osd_alpha = ConfigSlider(default=255, limits=(0, 255))
        config.av.osd_alpha.addNotifier(setAlpha)
    if os.path.exists('/proc/stb/vmpeg/0/pep_scaler_sharpness'):

        def setScaler_sharpness(config):
            myval = int(config.value)
            try:
                print '--> setting scaler_sharpness to: %0.8X' % myval
                f = open('/proc/stb/vmpeg/0/pep_scaler_sharpness', 'w')
                f.write('%0.8X' % myval)
                f.close()
                f = open('/proc/stb/vmpeg/0/pep_apply', 'w')
                f.write('1')
                f.close()
            except IOError:
                print "couldn't write pep_scaler_sharpness"

        config.av.scaler_sharpness = ConfigSlider(default=13, limits=(0, 26))
        config.av.scaler_sharpness.addNotifier(setScaler_sharpness)
    else:
        config.av.scaler_sharpness = NoSave(ConfigNothing())
