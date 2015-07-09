from Screen import Screen
from Components.ActionMap import ActionMap
from Components.Sources.StaticText import StaticText
from Components.Harddisk import harddiskmanager
from Components.NimManager import nimmanager
from Components.About import about
from Components.ScrollLabel import ScrollLabel
from Components.Button import Button
from os import path
from Tools.StbHardware import getFPVersion
from enigma import eTimer
from boxbranding import getBoxType, getImageVersion

class About(Screen):

    def __init__(self, session):
        Screen.__init__(self, session)
        AboutText = _('STB : ') + getBoxType() + '\n'
        AboutText += _('Brand : ') + about.getBrandString() + '\n'
        AboutText += _('Image : Persian Empire') + '\n'
        AboutText += _('Version : ') + getImageVersion() + '\n'
        AboutText += _('Kernel : ') + about.getKernelVersionString() + ' PE Mode REDOUANE\n'
        EnigmaVersion = 'Enigma2 : ' + about.getEnigmaVersionString()
        self['EnigmaVersion'] = StaticText(EnigmaVersion)
        AboutText += EnigmaVersion + ' PE Mode REDOUANE\n'
        AboutText += _('For More Information Visit http://e2pe.com') + '\n'
        fp_version = getFPVersion()
        if fp_version is None:
            fp_version = ''
        else:
            fp_version = _('Frontprocessor : %d') % fp_version
            AboutText += fp_version + '\n'
        self['FPVersion'] = StaticText(fp_version)
        tempinfo = ''
        if path.exists('/proc/stb/sensors/temp0/value'):
            f = open('/proc/stb/sensors/temp0/value', 'r')
            tempinfo = f.read()
            f.close()
        elif path.exists('/proc/stb/fp/temp_sensor'):
            f = open('/proc/stb/fp/temp_sensor', 'r')
            tempinfo = f.read()
            f.close()
        if tempinfo and int(tempinfo.replace('\n', '')) > 0:
            mark = str('\xc2\xb0')
            AboutText += _('System Temperature : %s') % tempinfo.replace('\n', '') + mark + 'C\n'
        if path.exists('/proc/stb/info/chipset'):
            AboutText += '\n' + _('Chipset : %s') % about.getChipSetString() + '\n'
        AboutText += _('CPU : %s') % about.getCPUString() + _(' , Cores : %s') % about.getCpuCoresString() + '\n'
        self['TunerHeader'] = StaticText(_('NIMs :'))
        AboutText += '\n' + _('NIMs :') + '\n'
        nims = nimmanager.nimList()
        for count in range(len(nims)):
            if count < 4:
                self['Tuner' + str(count)] = StaticText(nims[count])
            else:
                self['Tuner' + str(count)] = StaticText('')
            AboutText += ' ' + nims[count] + '\n'

        self['HDDHeader'] = StaticText(_('HDD :'))
        AboutText += '\n' + _('HDD :') + '\n'
        hddlist = harddiskmanager.HDDList()
        hddinfo = ''
        if hddlist:
            for count in range(len(hddlist)):
                if hddinfo:
                    hddinfo += '\n'
                hdd = hddlist[count][1]
                if int(hdd.free()) > 1024:
                    hddinfo += '%s\n(%s, %d GB %s)' % (hdd.model(),
                     hdd.capacity(),
                     hdd.free() / 1024,
                     _('free'))
                else:
                    hddinfo += '%s\n(%s, %d MB %s)' % (hdd.model(),
                     hdd.capacity(),
                     hdd.free(),
                     _('free'))

        else:
            hddinfo = _('none')
        self['hddA'] = StaticText(hddinfo)
        AboutText += hddinfo
        self['AboutScrollLabel'] = ScrollLabel(AboutText)
        self['key_green'] = Button(_('Translations'))
        self['key_red'] = Button(_('Latest Commits'))
        self['actions'] = ActionMap(['ColorActions', 'SetupActions', 'DirectionActions'], {'cancel': self.close,
         'ok': self.close,
         'red': self.showCommits,
         'green': self.showTranslationInfo,
         'up': self['AboutScrollLabel'].pageUp,
         'down': self['AboutScrollLabel'].pageDown})

    def showTranslationInfo(self):
        self.session.open(TranslationInfo)

    def showCommits(self):
        self.session.open(CommitInfo)


class TranslationInfo(Screen):

    def __init__(self, session):
        Screen.__init__(self, session)
        info = _('TRANSLATOR_INFO')
        if info == 'TRANSLATOR_INFO':
            info = '(N/A)'
        infolines = _('').split('\n')
        infomap = {}
        for x in infolines:
            l = x.split(': ')
            if len(l) != 2:
                continue
            type, value = l
            infomap[type] = value

        print infomap
        self['TranslationInfo'] = StaticText(info)
        translator_name = infomap.get('Language-Team', 'none')
        if translator_name == 'none':
            translator_name = infomap.get('Last-Translator', '')
        self['TranslatorName'] = StaticText(translator_name)
        self['actions'] = ActionMap(['SetupActions'], {'cancel': self.close,
         'ok': self.close})


class CommitInfo(Screen):

    def __init__(self, session):
        Screen.__init__(self, session)
        self.skinName = ['CommitInfo', 'About']
        self['AboutScrollLabel'] = ScrollLabel(_('Please wait'))
        self['actions'] = ActionMap(['SetupActions', 'DirectionActions'], {'cancel': self.close,
         'ok': self.close,
         'up': self['AboutScrollLabel'].pageUp,
         'down': self['AboutScrollLabel'].pageDown})
        self.Timer = eTimer()
        self.Timer.callback.append(self.readCommitLogs)
        self.Timer.start(50, True)

    def readCommitLogs(self):
        urls = ['http://sourceforge.net/p/openpli/enigma2/feed', 'http://sourceforge.net/p/openpli/openpli-oe-core/feed']
        commitlog = ''
        from urllib2 import urlopen
        try:
            for url in urls:
                commitlog += 80 * '-' + '\n'
                commitlog += url.split('/')[-2] + '\n'
                commitlog += 80 * '-' + '\n'
                for x in urlopen(url, timeout=5).read().split('<title>')[2:]:
                    for y in x.split('><'):
                        if '</title' in y:
                            title = y[:-7]
                        if '</dc:creator' in y:
                            creator = y.split('>')[1].split('<')[0]
                        if '</pubDate' in y:
                            date = y.split('>')[1].split('<')[0][:-6]

                    commitlog += date + ' ' + creator + '\n' + title + '\n\n'

        except:
            commitlog = _('Currently the commit log cannot be retreived - please try later again')

        self['AboutScrollLabel'].setText(commitlog)
