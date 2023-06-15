#import pythomcom
#pythomcom.CoInitialize()
import ctypes
ctypes.windll.ole32.CoInitialize(None)

import clr #pythonnet
import sys
print(sys.path)
import pdb
import threading
import wx
#USAGE: python 3+, pip install wxpython, pip install pythonnet, pip install pdb, cmd /k python.exe -i %thisscript%
#recording inputs are displayed, check boxes for which ones will be recorded, timestamped wavs recorded to same directory, close app to finish recording.
#haven't implemented the monitoring things that are reflected on the UI yet... although it isn't really necessary
#if you go into the windows audio control panel there is an checkbox to toggle to monitor called "listen to this device"
#compared to the earlier version the difference in behavior is that this supports up to 11 inputs and doesn't record anything for unchecked inputs.
#TODO: add config for stereo/mono & sampling rate.. currently just stereo and 44.1 khz
from System import Environment
name = Environment.MachineName
print(name)
import os
import datetime
print(os.getcwd())
from System import Console
#clr.AddReference('Microsoft.VisualStudio.Tools.Office.Excel.HostAdapter.v10.0.dll')
clr.AddReference('NAudio') #ildasm used on NAudio.dll showed this was the namespace
import NAudio as NAudio
from System import EventHandler, EventArgs
#https://stackoverflow.com/questions/52612651/pythonnet-delegate-method-with-generics-not-being-called
########
#c
#like the yatta moni case of comments here, most variables have one or two pairings of data transfer lol.........
global testmdupefixcounter
global tbee
tbee = 0

#test65
import pyogg
#try this instead? https://github.com/orion-labs/opuslib

#dont read this look at FileMgr and FileMgr2, those are the two windows that get shown


class AudioPlayerDisplay(wx.Window): #pygamedisplay from pydubmanager7
    def __init__(self, parent, ID):
        wx.Window.__init__(self, parent, ID)
        self.parent = parent
        self.hwnd = self.GetHandle()

        self.size = self.GetSize()
        #print(self.size)
        self.size_dirty = True

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.Update, self.timer)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        #
        self.Bind(wx.EVT_LEFT_DOWN, self.CLICKH)
        self.Bind(wx.EVT_RIGHT_DOWN, self.CLICKR)
        self.Bind(wx.EVT_LEFT_UP, self.CLICKUP)
        self.Bind(wx.EVT_RIGHT_UP, self.CLICKUPR)
        self.Bind(wx.EVT_MOTION, self.MOTION)
        #self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.fps = 60.0
        self.timespacing = 1000.0 / self.fps
        self.timer.Start(self.timespacing, False)

        self.linespacing = 5

        self.FILELIST = []
        self.LOADLIST = []
        self.mHELD = 0
        self.mHELDr = 0
        self.xLAST = 0
        self.yLAST = 0

        #self.COLORA = pygame.Color(0,128,256,a=100)
        #self.COLORA = pygame.Color(256,256,256)
        self.COLORA = (0,128,256,100)
        self.COLORA = (0,128,256)
        #print("self.screen is " + self.screen)
        pygame.init() #needed for font to work
        self.screen = pygame.Surface((500,500))

        self.font1 = pygame.font.SysFont("agencyfb",12,False,False)

class AudioLibrary(wx.Panel): #this isnt used at all. the main wx.panels are monitorpanel and monitorpanelrev
    def __init__(self,parent):
        wx.Panel.__init__(self,parent,2345,(0,0),(400,400))
        wx.CheckBox(self,56, "librarybutton1", (20,20), (20,20))
        
'''
class AudioPlayer(wx.Panel):
    def __init__(self,parent,id,pos,size):
        wx.Panel.__init__(self,parent,id,pos,size)
        '''        
class AudioPlayer(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self,parent,1234,"audioplayerframe",(0,0),(600,600))
        topshift = 40
        '''
        a1=wx.CheckBox(self,1501, "", (0,topshift+0), (20,20))
        a2=wx.CheckBox(self,1502, "", (20,topshift+0), (20,20))
        a3=wx.CheckBox(self,1503, "", (40,topshift+0), (20,20))
        a4=wx.CheckBox(self,1504, "", (60,topshift+0), (20,20))
        a5=wx.CheckBox(self,1505, "", (80,topshift+0), (20,20))
        a6=wx.CheckBox(self,1506, "", (100,topshift+0), (20,20))
        a7=wx.CheckBox(self,1507, "", (120,topshift+0), (20,20))#@wx.Button.__init__(self
        a8=wx.CheckBox(self,1508, "", (140,topshift+0), (20,20))        
        b1=wx.CheckBox(self,1511, "", (0,topshift+20), (20,20))
        b2=wx.CheckBox(self,1512, "", (20,topshift+20), (20,20))
        b3=wx.CheckBox(self,1513, "", (40,topshift+20), (20,20))
        b4=wx.CheckBox(self,1514, "", (60,topshift+20), (20,20))
        b5=wx.CheckBox(self,1515, "", (80,topshift+20), (20,20))
        b6=wx.CheckBox(self,1516, "", (100,topshift+20), (20,20))
        b7=wx.CheckBox(self,1517, "", (120,topshift+20), (20,20))#@wx.Button.__init__(self
        b8=wx.CheckBox(self,1518, "", (140,topshift+20), (20,20))        
        c1=wx.CheckBox(self,1521, "", (0,topshift+40), (20,20))
        c2=wx.CheckBox(self,1522, "", (20,topshift+40), (20,20))
        c3=wx.CheckBox(self,1523, "", (40,topshift+40), (20,20))
        c4=wx.CheckBox(self,1524, "", (60,topshift+40), (20,20))
        c5=wx.CheckBox(self,1525, "", (80,topshift+40), (20,20))
        c6=wx.CheckBox(self,1526, "", (100,topshift+40), (20,20))
        c7=wx.CheckBox(self,1527, "", (120,topshift+40), (20,20))#@wx.Button.__init__(self
        c8=wx.CheckBox(self,1528, "", (140,topshift+40), (20,20))        
        d1=wx.CheckBox(self,1531, "", (0,topshift+60), (20,20))
        d2=wx.CheckBox(self,1532, "", (20,topshift+60), (20,20))
        d3=wx.CheckBox(self,1533, "", (40,topshift+60), (20,20))
        d4=wx.CheckBox(self,1534, "", (60,topshift+60), (20,20))
        d5=wx.CheckBox(self,1535, "", (80,topshift+60), (20,20))
        d6=wx.CheckBox(self,1536, "", (100,topshift+60), (20,20))
        d7=wx.CheckBox(self,1537, "", (120,topshift+60), (20,20))#@wx.Button.__init__(self
        d8=wx.CheckBox(self,1538, "", (140,topshift+60), (20,20))        
        e1=wx.CheckBox(self,1539, "", (0,topshift+80), (20,20))
        e2=wx.CheckBox(self,1540, "", (20,topshift+80), (20,20))
        e3=wx.CheckBox(self,1541, "", (40,topshift+80), (20,20))
        e4=wx.CheckBox(self,1542, "", (60,topshift+80), (20,20))
        e5=wx.CheckBox(self,1543, "", (80,topshift+80), (20,20))
        e6=wx.CheckBox(self,1544, "", (100,topshift+80), (20,20))
        e7=wx.CheckBox(self,1545, "", (120,topshift+80), (20,20))#@wx.Button.__init__(self
        e8=wx.CheckBox(self,1546, "", (140,topshift+80), (20,20))  
        f1=wx.CheckBox(self,1547, "", (0,topshift+100), (20,20))
        f2=wx.CheckBox(self,1548, "", (20,topshift+100), (20,20))
        f3=wx.CheckBox(self,1549, "", (40,topshift+100), (20,20))
        f4=wx.CheckBox(self,1550, "", (60,topshift+100), (20,20))
        f5=wx.CheckBox(self,1551, "", (80,topshift+100), (20,20))
        f6=wx.CheckBox(self,1552, "", (100,topshift+100), (20,20))
        f7=wx.CheckBox(self,1553, "", (120,topshift+100), (20,20))#@wx.Button.__init__(self
        f8=wx.CheckBox(self,1554, "", (140,topshift+100), (20,20))  
        g1=wx.CheckBox(self,1555, "", (0,topshift+120), (20,20))
        g2=wx.CheckBox(self,1556, "", (20,topshift+120), (20,20))
        g3=wx.CheckBox(self,1557, "", (40,topshift+120), (20,20))
        g4=wx.CheckBox(self,1559, "", (60,topshift+120), (20,20))
        g5=wx.CheckBox(self,1560, "", (80,topshift+120), (20,20))
        g6=wx.CheckBox(self,1561, "", (100,topshift+120), (20,20))
        g7=wx.CheckBox(self,1562, "", (120,topshift+120), (20,20))#@wx.Button.__init__(self
        g8=wx.CheckBox(self,1563, "", (140,topshift+120), (20,20))  
        h1=wx.CheckBox(self,1564, "", (0,topshift+140), (20,20))
        h2=wx.CheckBox(self,1565, "", (20,topshift+140), (20,20))
        h3=wx.CheckBox(self,1566, "", (40,topshift+140), (20,20))
        h4=wx.CheckBox(self,1567, "", (60,topshift+140), (20,20))
        h5=wx.CheckBox(self,1568, "", (80,topshift+140), (20,20))
        h6=wx.CheckBox(self,1569, "", (100,topshift+140), (20,20))
        h7=wx.CheckBox(self,1570, "", (120,topshift+140), (20,20))#@wx.Button.__init__(self
        h8=wx.CheckBox(self,1571, "", (140,topshift+140), (20,20))
        '''
        
        #self.tb= self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT)
        
        #self.tb.Realize()
        
        #line1 = wx.TextCtrl(self,4001,"line1",(160,0),(300,20))
        #line2 = wx.TextCtrl(self,4002,"line2",(160,20),(300,20))
        #line3 = wx.TextCtrl(self,4003,"line3",(160,40),(300,20))
        #line4 = wx.TextCtrl(self,4004,"line4",(160,60),(300,20))
        #line5 = wx.TextCtrl(self,4005,"line5",(160,80),(300,20))
        #line6 = wx.TextCtrl(self,4006,"line6",(160,100),(300,20))
        #line7 = wx.TextCtrl(self,4007,"line7",(160,120),(300,20))
        #line8 = wx.TextCtrl(self,4008,"line8",(160,140),(300,20))
class FileMgr2(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self,parent,570,title,(850,50),(800,300))
        self.sbf = self.CreateStatusBar()
        fm2tb = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT)
        
        #okay so fm2bt1 and fm2bt2 are coninected to fm2test1 and fm2test2
        #"okay so"
        fm2bt1 = fm2tb.AddTool(801,"Test",wx.Bitmap("icon.png"))
        self.Bind(wx.EVT_TOOL,fm2test1,fm2bt1)
        fm2bt2 = fm2tb.AddTool(802,"Tes2",wx.Bitmap("icon.png"))
        self.Bind(wx.EVT_TOOL,fm2test2,fm2bt2)
        fm2bt3 = fm2tb.AddTool(803,"Tes3",wx.Bitmap("icon.png"))
        self.Bind(wx.EVT_TOOL,fm2test1partial,fm2bt3)
        fm2tb.Realize()
        
        self.topsplitter2 = wx.SplitterWindow(self,808,pos=wx.Point(0,0),size=wx.Size(800,600),style=wx.SP_BORDER,name="TopSplitterW")
        self.AudioChecker2 = AudioCheckListB(self.topsplitter2, 778)
        
        blankstr2 = []
        for itbs2 in range(self.AudioChecker2.recdevct):
            blankstr2.append("1")#gotta instantiate the mmdeviceenumerator...... we might have to move the entire thing into the filemgr2 class or something :(
        global coolstring2
        coolstring2 = blankstr2
        #wth
        self.rightside = MonitorPanelRevW(self.topsplitter2,999,self.AudioChecker2.recdevct,self.AudioChecker2.recdevct)#pos1 #loc1
        self.topsplitter2.SplitVertically(self.AudioChecker2,self.rightside)
        
        #self.topsplitter.SplitVertically(self.AudioChecker,self.rightside)
        
        #part35
        #$$
        '''
        blankstr2 = []
        for itbs2 in range(self.AudioChecker2.recdevct):
            blankstr2.append("1")#gotta instantiate the mmdeviceenumerator...... we might have to move the entire thing into the filemgr2 class or something :(
        global coolstring2
        coolstring2 = blankstr2
        '''
        
        #read this 35
        '''
        self.recdevct = self.AudioChecker.Count
        
        #so FileMgr has self.topsplitter and self.AudioChecker, sac contains AudioCheckList, recdevct prob passed 2 function
        #self.MonitorChoice = MonitorChoice(self.topsplitter, 888)
        
        self.outdevct = NAudio.Wave.WaveOut.DeviceCount
        print("outdevct =" + str(self.outdevct))
        
        #usedtobe#self.rightside = MonitorPanel(self.topsplitter,999,self.recdevct)
        #self.rightside = MonitorPanelRev(self.topsplitter,999,self.recdevct,self.outdevct)#pos1 #loc1
        #decided we actually need the recdevct for both 2 righthabnd paramaters
        blankstr = []
        #tempstr is not defined
        '''
        
        '''
        for cta in range( self.outdevct):
            blankstr.append(NAudio.Wave.WaveOut.GetCapabilities(cta).ProductName)
   #        tempstring = NAudio.Wave.WaveOut.GetCapabilities(itb).ProductName
        print(blankstr)
        global tempstring
        tempstring = blankstr
        '''
        
        '''
        for cta in range( self.recdevct):
            blankstr.append(NAudio.Wave.WaveIn.GetCapabilities(cta).ProductName)
        print(blankstr)
        global coolstring
        coolstring = blankstr
        '''
        
        
        
#okay so i wrote this FileMgr2 and fm2test1 and loopbackwriter2 based on the stuff from FileMgr
#but it gives me some kind of marshalling error. i think it's cause of the second window
#i will try to modify FileMgr to just run fm2test1 and see if it works from the first window.....

def loopbackwriter2(sender,e):
    if 1 == 1:
        myww.WriteData(e.Buffer,0,e.BytesRecorded)
        myww.Flush()
#above only deals with the file writer
#this should add to the buffered wave
def loopbackwriter2play(sender,e):
    if 1 == 1:
        ##global thisbwp
        ##thisbwp.AddSamples(e.Buffer,0,e.BytesRecorded)
        global myz
        myz.AddSamples(e.Buffer,0,e.BytesRecorded)
        #myz = NAudio.Wave.BufferedWaveProvider(myw.WaveFormat)
        pass
        
        
        
def fm2test1partial(e):
    print("button 3 pressed.")
    global enumerator2
    enumerator2 = NAudio.CoreAudioApi.MMDeviceEnumerator()
    wlist2 = enumerator.EnumerateAudioEndPoints(NAudio.CoreAudioApi.DataFlow.All,NAudio.CoreAudioApi.DeviceState.Active)
    #wlist2 should contain a list now of the endpoints that were active
    #if you dont use devicestate active and use all or whatever its called then you'll get inactive ones like stuff that used to be on your computers usb
    

def fm2test1(e):
    print("hewwo")
    global enumerator
    enumerator = NAudio.CoreAudioApi.MMDeviceEnumerator()
    print(enumerator)
    
    print(type(enumerator))
    #used to be good line!
    ##wlist = enumerator.EnumerateAudioEndPoints(NAudio.CoreAudioApi.DataFlow.All,NAudio.CoreAudioApi.DeviceState.All)
    #okay so it turns out that we do need just the active ones.
    wlist = enumerator.EnumerateAudioEndPoints(NAudio.CoreAudioApi.DataFlow.All,NAudio.CoreAudioApi.DeviceState.Active)
    #https://github.com/naudio/NAudio/blob/master/Docs/EnumerateOutputDevices.md#enumerating-audio-devices
    #str(wlist[0]) = #device name#
    #location02
    #myw = NAudio.wlist[0]
    #
    #myw = NAudio.Wave.WasapiLoopbackCapture(wlist[0])
    #maybe i cant really pass this list in?
    
    #wlist.__sizeof__() >> 16
    #wlist[15] out of range!
    #wlist[14] last one somehow.
    
    #upgrayde bobobo
    
    #range(wlist.__sizeof__())
    
    #example loop
    #print("fm2test1 line prior to for xx in range wlist sizeof -1....... print wlist [xx]")
    for xx in range(wlist.__sizeof__()-1):
        print(str(wlist[xx]))
    
    #pdb.set_trace()
    
    myw = NAudio.Wave.WasapiLoopbackCapture()
    mya = myw.GetDefaultLoopbackCaptureDevice()
    #uh doesnt make sense but lets try this again
    ##pdb.set_trace()
    print(str(wlist[6]))
    myw = NAudio.Wave.WasapiLoopbackCapture(wlist[6])
    #item six was speakers usb audio dac and it worked.....
    global myww #gbw equivalent
    timestampz = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    myww = NAudio.Wave.WaveFileWriter(timestampz + "." + '.doopbak.wav', myw.WaveFormat)
    global myz
    myz = NAudio.Wave.BufferedWaveProvider(myw.WaveFormat)
    global fm2out
    fm2out = NAudio.Wave.WaveOut()
    global myx
    myx = NAudio.Wave.WaveFloatTo16Provider(myz)
    myw.DataAvailable += loopbackwriter2 #writedata to myww
    myw.DataAvailable += loopbackwriter2play #adds samples to myz
    '''
    def loopbackwriter2(sender,e):
    if 1 == 1:
        myww.WriteData(e.Buffer,0,e.BytesRecorded)
        myww.Flush()
    if 1 == 1:
        ##global thisbwp
        ##thisbwp.AddSamples(e.Buffer,0,e.BytesRecorded)
        global myz
        myz.AddSamples(e.Buffer,0,e.BytesRecorded)
        #myz = NAudio.Wave.BufferedWaveProvider(myw.WaveFormat)
        pass
    '''
    #pdb.set_trace()
    myw.StartRecording()
    #pdb.set_trace()
    
    #these don't even work with myx
    ##fm2out.Init(myx)
    ##fm2out.Play()
    #don't need these two above lines for the recording to work.
    fm2out.Init(myz)
    fm2out.Play()
    pass

def fm2test2(e):
    print("check fm2test2 passed")
    pass
'''
def loopbackwriter(sender,e):
    if 1 == 1:
        gbw.WriteData(e.Buffer,0,e.BytesRecorded)
        gbw.Flush()
'''
class FileMgr(wx.Frame):
#this class is important. top level class.
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self,parent,569,title,(50,50),(800,300))#orig 800 300
        self.sb = self.CreateStatusBar()
        tb = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT)
        bt1 = tb.AddTool(701,"Rec",wx.Bitmap("icon.png"))
        bt2 = tb.AddTool(702,"PDB",wx.Bitmap("icon.png"))
        bt3 = tb.AddTool(703,"DBG",wx.Bitmap("icon.png"))
        
        bt4 = tb.AddTool(704,"TEST",wx.Bitmap("icon.png"))
        bt5 = tb.AddTool(705,"T666",wx.Bitmap("icon.png"))
        
        bt6 = tb.AddTool(706,"T6ST",wx.Bitmap("icon.png"))
        bt7 = tb.AddTool(707,"MONI",wx.Bitmap("icon.png"))
        bt8 = tb.AddTool(708,"LSRC",wx.Bitmap("icon.png"))
        bt9 = tb.AddTool(709,"TST1",wx.Bitmap("icon.png"))
        bt10 = tb.AddTool(710,"TST2",wx.Bitmap("icon.png"))
        bt11 = tb.AddTool(711,"WIN2",wx.Bitmap("icon.png"))
        
        self.Bind(wx.EVT_TOOL,gorecordA,bt1)
        self.Bind(wx.EVT_TOOL,gorecordA,bt2)
        self.Bind(wx.EVT_TOOL,mytest2,bt3)
        
        self.Bind(wx.EVT_TOOL,test64,bt4)#wasapi!
        self.Bind(wx.EVT_TOOL,test666,bt5)
        self.Bind(wx.EVT_TOOL,testlistrec,bt6)#this shows the recording devices
        self.Bind(wx.EVT_TOOL,yatta,bt7)#moni
        
        self.Bind(wx.EVT_TOOL,listrec,bt8)
        
        self.Bind(wx.EVT_TOOL,testone,bt9)
        
        self.Bind(wx.EVT_TOOL,testtwo,bt10)
        #self.Bind(wx.EVT_TOOL,test65,bt11)
        self.Bind(wx.EVT_TOOL,fm2test1,bt11)
        #testthree was placeholder, now test65 for TST3 button
        
        tb.Realize()
        #self.asplitter = wx.SplitterWindow(self, 858,pos=wx.Point*(0,400),size=wx.Size(600,300),style=wx.SP_BORDER,name="ASplitter")
        ####self.asplitter = wx.SplitterWindow(self,809,pos=wx.Point(0,0),size=wx.Size(400,400),style=wx.SP_BORDER,name="ASplitter")
        aid = 811 #audiolibrary
        apos = (0,0)
        asize = (300,300)
        #self.audiolibrary = AudioLibrary(self.asplitter)
        pid = 812 #audioplayer
        ppos = (0,0)
        psize = (300,300)
        #self.audioplayer = AudioPlayer(self.asplitter)
        #self.asplitter.SplitVertically(self.audiolibrary,self.audioplayer)
        
        #original size 400x400#self.topsplitter = wx.SplitterWindow(self,808,pos=wx.Point(0,0),size=wx.Size(400,400),style=wx.SP_BORDER,name="TopSplitter")
        self.topsplitter = wx.SplitterWindow(self,808,pos=wx.Point(0,0),size=wx.Size(800,600),style=wx.SP_BORDER,name="TopSplitter")
        #uh okay so we have the thing filething.topsplitter which is a wx.SplitterWindow initialized with the size 800x 600
        self.AudioChecker = AudioCheckList(self.topsplitter, 777) #this has the waveins info
        #this makes filething.AudioChecker with the AudioCheckList, line 286 or so, making it a child of the self.topsplitter
        self.recdevct = self.AudioChecker.Count
        
        #so FileMgr has self.topsplitter and self.AudioChecker, sac contains AudioCheckList, recdevct prob passed 2 function
        #self.MonitorChoice = MonitorChoice(self.topsplitter, 888)
        
        self.outdevct = NAudio.Wave.WaveOut.DeviceCount
        print("outdevct =" + str(self.outdevct))
        
        #usedtobe#self.rightside = MonitorPanel(self.topsplitter,999,self.recdevct)
        #self.rightside = MonitorPanelRev(self.topsplitter,999,self.recdevct,self.outdevct)#pos1 #loc1
        #decided we actually need the recdevct for both 2 righthabnd paramaters
        blankstr = []
        #tempstr is not defined
        '''
        for cta in range( self.outdevct):
            blankstr.append(NAudio.Wave.WaveOut.GetCapabilities(cta).ProductName)
   #        tempstring = NAudio.Wave.WaveOut.GetCapabilities(itb).ProductName
        print(blankstr)
        global tempstring
        tempstring = blankstr
        '''
        for cta in range( self.recdevct):
            blankstr.append(NAudio.Wave.WaveIn.GetCapabilities(cta).ProductName)
        print(blankstr)
        global coolstring
        coolstring = blankstr
        
        
        self.rightside = MonitorPanelRev(self.topsplitter,999,self.recdevct,self.recdevct)#pos1 #loc1
        #here we make the monitorpanelrev which is the thing that shows the checkboxes and dropdowns.
        #the self.recdevct is the dimensions, based on the number of input devices (cant monitor if theres not an input)
        #for now we just have one input going to one output at a time.
        #basically what you do is check the box for the input that you want to monitor and select the device to hear on, then hit the MONI button (i think bt6).
        
        #self.rightside = MonitorChoice(self.topsplitter,999,self.recdevct, (500,500))
        
        #self.splitter = wx.SplitterWindow(self.topsplitter, ID_SPLITTER,pos=wx.Point(0,0),size=wx.Size(400,400),style=wx.SP_BORDER,name="Splitter")
        self.topsplitter.SplitVertically(self.AudioChecker,self.rightside)
        #^ monitor panel and audiochecklist attach to self.topsplitter as first param of constructor
        # self.topsplitter.SplitVertically(self.AudioChecker,selfrightside) is necessary too.
        
        #
        #seems like the SplitterWindow is messed up.
        #plus there's already one called ASplitter........
        #okay that did it. commenting out asplitter did it.
        
    def OnExit(self,e):
        self.Close(True)


    
'''
class AudioLibrary(wx.Panel):
    def __init__(self,parent,id,pos,size):
        wx.Panel.__init__(self,parent,id,pos,size)
'''

#@AudioCheckListB
#@FileMgr2
#this is called AudioChecker2
#it would be nice if we could write a comment automatically that tells us the name of the object at runtime.....

#inside of AudioCheckListB there's an MMDeviceEnumerator called enumeratorB

#self.recdevct = wlen = enumeratorB.__sizeof__()
#^this should be like a legitimate grammar in some language

class AudioCheckListB(wx.CheckListBox):#this is audiochecklist for filemgr2. it has wasapi and you need to use the mmdeviceenumerator
    def __init__(self, parent, id):
        #devicecount2 = NAudio.Wave.Wasapi
        enumeratorB = NAudio.CoreAudioApi.MMDeviceEnumerator()
        wlistB = enumeratorB.EnumerateAudioEndPoints(NAudio.CoreAudioApi.DataFlow.All,NAudio.CoreAudioApi.DeviceState.Active)
        #pdb.set_trace()
        wlen = enumeratorB.__sizeof__()
        
        #global wlenJ
        #wlenJ = wlen
        
        #recdevct = wlen
        self.recdevct = wlen
        #print("123432 is str " + str(type(wlenJ) ) )
        print("123432 is str " + str(type(self.recdevct) ) )
        
        global wlistStr
        wlistStr = []
        for xx in range(wlen-1):
            wlistStr.append(str(wlistB[xx]))
        print(wlistStr)
        #print(len(wlistB)) ##MMDeviceCollection has no len
        #wx.CheckListBox.__init__(self, parent, id, (0,0),(50,50),wlistB)
        wx.CheckListBox.__init__(self, parent, id, (0,0),(400,400),wlistStr)
        #getdefaultcapturedevice
#location01

class AudioCheckList(wx.CheckListBox):#loc4
    def __init__(self, parent, id):
        devicecount = NAudio.Wave.WaveIn.DeviceCount
        devicelist = []
        for n in range(devicecount):
            devicelist.append(NAudio.Wave.WaveIn.GetCapabilities(n).ProductName)
            
        wx.CheckListBox.__init__(self, parent, id,(0,0),(50,50),devicelist)
        #https://docs.wxpython.org/gallery.html shows most widgets

class WasapiCheckList(wx.CheckListBox):
    def __init__(self, parent, id):
        wowlist = enumerator.EnumerateAudioEndPoints(NAudio.CoreAudioApi.DataFlow.All,NAudio.CoreAudioApi.DeviceState.Active)
        for xx in range(wowlist.__sizeof__()-1):
            print(str(wowlist[xx]))
        pass
        #devicecountW = NAudio.
#class ASIOChoice(wx.Choice):
#lol
class ASIOChoice(wx.CheckListBox):
    def __init__(self, parent, id, pos, size):
        print('init ASIOChoice')
        global availables
        availables = NAudio.Wave.AsioOut.GetDriverNames()
        print('init ASIOChoice position 2')
        #global asiolist
        global asiolist
        asiolist = []
        for n in range(10):
            try:
                #asiolist.append(availables.Get(n))
                print('iterator')
            except:
                pass
        print('asiolist?')
        print(asiolist)
        wx.CheckListBox.__init__(self, parent, id, pos,size, asiolist)

#monitorchoice is inside of monitorpanel
class MonitorChoice(wx.Choice): #need to run mon0.GetSelection() to return an int that will go into DeviceNumber
    #def __init__(self,parent,id):
    #when this gets initialized it puts the stuff into the list from the waveout productname thing below
    #monitor choice gets number of wave outs
    def __init__(self,parent,id,pos,size):
        devicecount = NAudio.Wave.WaveOut.DeviceCount
        devicelist = []
        for n in range(devicecount):
            devicelist.append(NAudio.Wave.WaveOut.GetCapabilities(n).ProductName)
        #wx.Choice.__init__(self, parent, id, (0,0), (50,50), devicelist)
        
        wx.Choice.__init__(self, parent, id, pos, size, devicelist)
        #line342 wx.Choice.__init__(self, parent, id, pos, size, devicelist)
        
    '''read this
    for xx in checkedlist:
        globals()["waveIn" + str(xx)].DeviceNumber = xx
    '''
        #^^ important line
    def retrieveA(inputone):
        pass
    def getselection():
        return self.GetSelection()

#locX
class MonitorPanel(wx.Panel):
    def __init__(self,parent,id, countt): #monitorpanel gets initialized with a count of items that populate diagonallyi down to teh right
        wx.Panel.__init__(self,parent,id, (0,0), (50,50), 0, "Monitor-Panel")
        for xx in range(countt):
            globals()["mon" + str(xx)] = MonitorChoice(self, 1200 + xx, (0+(xx*5),0+(xx*23)), (120,23))
            ##line342 wx.Choice.__init__(self, parent, id, pos, size, devicelist)
            print("mon" + str(xx) + "<-created")
        for xx in range(countt):
            globals()["monbt" + str(xx)] = wx.CheckBox(self,1400 + xx, "mon"+str(xx), (127+(xx*5),0+(xx*23)), (70,23))
            #globals()["label" + str(xx)] = wx.StaticText(self,1600 + xx, "
            #GetCapabilities(xx).ProductName
            print("monbt" + str(xx) + "<-checkbox-made")
        print("printing dir(mon0)")
        print(dir(mon0))
        #global asiochoice
        #asiochoice = ASIOChoice(self, 5678,(220,0),(200,200))
        #disabling the asio thing cause it's borked

#locX1

class MonitorPanelRevW(wx.Panel): #loc3
    def __init__(self,parent,id,countt1,countt2):
        wx.Panel.__init__(self,parent,id,(0,0),(50,50),0,"Monitor-Panel")
        global countahw1
        global countahw2
        countahw1 = countt1
        countahw2 = countt2
        for ita in range(countt1):#countt1 is for the monitorchoice, so should correspond to waveIn
            globals()["mon" + str(ita)] = MonitorChoice(self, 1200 + ita, (0+(ita*5),0+(ita*23)), (120,23))
            print("mon" + str(ita) + "<-created")
        for itb in range(countt2-1):#countt2 is for the checkbox, so should correspond to waveout??
            #tempstring = NAudio.Wave.WaveOut.GetCapabilities(itb).ProductName
            #globals()["ck"+str(itb)]=wx.CheckBox(self,1400 + itb, "output"+str(itb), (127+(itb*5),0+(itb*23)), (70,23))
            #pdb.set_trace()
            #loc5
            print("prior to running main line this line is " + str(itb))
            #globals()["ck"+str(itb)]=wx.CheckBox(self,1400 + itb, tempstring[itb] + ":" + str(itb), (127+(itb*5),0+(itb*23)), (70,23))
            globals()["ckw"+str(itb)]=wx.CheckBox(self,1400 + itb, "input"+str(itb)+coolstring2[itb], (127+(itb*5),0+(itb*23)), (70,23))#coolstring needs to be something else right now it's a glob$
            print("ck" + str(itb) + "<-checkbox-made")

class MonitorPanelRev(wx.Panel): #loc3
    #self.rightside = MonitorPanelRev(self.topsplitter,999,self.recdevct,self.recdevct)
    #^ above line initializes this class in this program. called in FileMgr
    def __init__(self,parent,id,countt1,countt2):
        wx.Panel.__init__(self,parent,id,(0,0),(50,50),0,"Monitor-Panel")
        #count1 will be the number of monitorchoices
        #count2 will be the number of checkboxes
        #  [1] -  - [2] - -
        #the comments below are probably wrong
        #monitorchoice is the dropdown box
        #those are waveouts
        #checkboxes correspond to waveins
        #the number of overall routings should be equal to the waveins amount
        #so if count1 is really teh number of monitorchoices we should go by countah2 later but
        global countah1
        global countah2
        countah1 = countt1
        countah2 = countt2
        for ita in range(countt1):#countt1 is for the monitorchoice, so should correspond to waveIn
            globals()["mon" + str(ita)] = MonitorChoice(self, 1200 + ita, (0+(ita*5),0+(ita*23)), (120,23))
            print("mon" + str(ita) + "<-created")
        for itb in range(countt2):#countt2 is for the checkbox, so should correspond to waveout??
            #tempstring = NAudio.Wave.WaveOut.GetCapabilities(itb).ProductName
            #globals()["ck"+str(itb)]=wx.CheckBox(self,1400 + itb, "output"+str(itb), (127+(itb*5),0+(itb*23)), (70,23))
            #pdb.set_trace()
            #loc5
            print("prior to running main line this line is " + str(itb))
            #globals()["ck"+str(itb)]=wx.CheckBox(self,1400 + itb, tempstring[itb] + ":" + str(itb), (127+(itb*5),0+(itb*23)), (70,23))
            globals()["ck"+str(itb)]=wx.CheckBox(self,1400 + itb, "input"+str(itb)+coolstring[itb], (127+(itb*5),0+(itb*23)), (70,23))
            print("ck" + str(itb) + "<-checkbox-made")
            #loc2
#there should be two levels or three levels of comments and you shoudl be able to check their visibility on or off and choose their colors and bakcgcorunds
#one level would be fore like old code lines like these. i would usually not show these
#another level would be for comments that are informative
#another level would be for perhaps comments like LocX1
#MonitorPanelRev

#def beginRecording:
class MonitorSource(wx.Choice):
    def __init__(self,parent,id,pos,size):
        devicecount = NAudio.Wave.WaveIn.DeviceCount
        devicelist = []
        for n in range(devicecount):
            devicelist.append(NAudio.Wave.WaveOut.GetCapabilities(n).ProductName)
        wx.Choice.__init__(self,parent,id,pos,size,devicelist)
    def retrieveA(inputone):
        pass
########
######vvvvv
#new shit from 5-29-203
#get ready for the illness

#made test64 5-29-2023, records loopback fine
# working on NAudio.Wave.IWaveProvider connecting to NAudio.Wave.WaveOut with initializer (<NWIWP)



######^^^^^
def gorecordA(shelf):
    devicecount = NAudio.Wave.WaveIn.DeviceCount
    devicelist = []
    for n in range(devicecount):
        devicelist.append(NAudio.Wave.WaveIn.GetCapabilities(n).ProductName)
    print(devicelist)

    traceyesno = 0
    if traceyesno == 0:
        pass
    elif traceyesno == 1:
        pdb.set_trace()

    checkedlist = filething.AudioChecker.GetChecked()
    print(checkedlist)
    #pdb.set_trace()
    #filething.rightside.

    #for xx in range(devicecount):
        #global globals()["waveIn" + str(xx)]

    ## replacing range devicecount with for xx in checkedlist:
    for xx in checkedlist:
        globals()["waveIn" + str(xx)] = NAudio.Wave.WaveIn()
    #this initializes the waveIn0-XX objects with defaults important
    for xx in checkedlist:
        globals()["waveIn" + str(xx)].DeviceNumber = xx
    #this line above is important! the DeviceNumber of the waveIn0-XX needs to be set!
    
    ##global waveIn
    ##global waveIn2
    ##global waveIn3
    ###waveIn = NAudio.Wave.WaveIn()
    ###waveIn2 = NAudio.Wave.WaveIn()
    ###waveIn3 = NAudio.Wave.WaveIn()
    ####waveIn.DeviceNumber = 0
    ####waveIn2.DeviceNumber = 1
    ####waveIn3.DeviceNumber = 2
    fourfour = 44100
    foureight = 48000
    channels = 2
    for xx in checkedlist:
        globals()["waveIn" + str(xx)].WaveFormat = NAudio.Wave.WaveFormat(fourfour,channels)
    #this is also important the waveFormat gets set to my default of 44100 and stereo
    
    #####waveIn.WaveFormat = NAudio.Wave.WaveFormat(fourfour,channels)
    #####waveIn2.WaveFormat = NAudio.Wave.WaveFormat(fourfour,channels)
    #####waveIn3.WaveFormat = NAudio.Wave.WaveFormat(fourfour,channels)
    #a#import datetime
    timestampz = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    for xx in checkedlist:
        globals()["writer" + str(xx)] = NAudio.Wave.WaveFileWriter(timestampz + "." + str(xx) + '.wav', globals()["waveIn" + str(xx)].WaveFormat)
    #important: the above two lines create the writer0-xx WaveFileWriter with first input filename (.wav) and second input waveIn0-xx.WaveFormat
    ###@
    
        #interesting: globals()["waveIn" + str(xx)].WaveFormat )
        #prev: NAudio.Wave.WaveFileWriter(timestampz + "." + str(xx) + '.wav'

    ##writer1 = NAudio.Wave.WaveFileWriter(timestampz + ".1.wav", waveIn.WaveFormat)
    ##writer2 = NAudio.Wave.WaveFileWriter(timestampz + ".2.wav", waveIn2.WaveFormat)
    ##writer3 = NAudio.Wave.WaveFileWriter(timestampz + ".3.wav", waveIn3.WaveFormat)

    def wave0write(sender, e):
        if 1 == 1:
            writer0.WriteData(e.Buffer,0,e.BytesRecorded)
            writer0.Flush()
    def wave1write(sender, e):
        if 1 == 1:
            writer1.WriteData(e.Buffer,0,e.BytesRecorded)
            writer1.Flush()
    def wave2write(sender, e):
        if 1 == 1:
            writer2.WriteData(e.Buffer,0,e.BytesRecorded)
            writer2.Flush()
    def wave3write(sender, e):
        if 1 == 1:
            writer3.WriteData(e.Buffer,0,e.BytesRecorded)
            writer3.Flush()
    def wave4write(sender, e):
        if 1 == 1:
            writer4.WriteData(e.Buffer,0,e.BytesRecorded)
            writer4.Flush()
    def wave5write(sender, e):
        if 1 == 1:
            writer5.WriteData(e.Buffer,0,e.BytesRecorded)
            writer5.Flush()
    def wave6write(sender, e):
        if 1 == 1:
            writer6.WriteData(e.Buffer,0,e.BytesRecorded)
            writer6.Flush()
    def wave7write(sender, e):
        if 1 == 1:
            writer7.WriteData(e.Buffer,0,e.BytesRecorded)
            writer7.Flush()
    def wave8write(sender, e):
        if 1 == 1:
            writer8.WriteData(e.Buffer,0,e.BytesRecorded)
            writer8.Flush()
    def wave9write(sender, e):
        if 1 == 1:
            writer9.WriteData(e.Buffer,0,e.BytesRecorded)
            writer9.Flush()
    def wave10write(sender, e):
        if 1 == 1:
            writer10.WriteData(e.Buffer,0,e.BytesRecorded)
            writer10.Flush()



    #for xx in range(devicecount):
        #globals()["waveIn" + str(xx)].DataAvailable += locals()["wave"+str(xx)+"write"]
    ##for xx in range(devicecount):
    '''
    if 'waveIn0' in globals():
        waveIn0.DataAvailable += wave0write
        waveIn0.StartRecording()
    '''

    if 0 in checkedlist:
        waveIn0.DataAvailable += wave0write
        waveIn0.StartRecording()
    if 1 in checkedlist:
        waveIn1.DataAvailable += wave1write
        waveIn1.StartRecording()
    if 2 in checkedlist:
        waveIn2.DataAvailable += wave2write
        waveIn2.StartRecording()
    if 3 in checkedlist:
        waveIn3.DataAvailable += wave3write
        waveIn3.StartRecording()
    if 4 in checkedlist:
        waveIn4.DataAvailable += wave4write
        waveIn4.StartRecording()
    if 5 in checkedlist:
        waveIn5.DataAvailable += wave5write
        waveIn5.StartRecording()
    if 6 in checkedlist:
        waveIn6.DataAvailable += wave6write
        waveIn6.StartRecording()
    if 7 in checkedlist:
        waveIn7.DataAvailable += wave7write
        waveIn7.StartRecording()
    if 8 in checkedlist:
        waveIn8.DataAvailable += wave8write
        waveIn8.StartRecording()
    if 9 in checkedlist:
        waveIn9.DataAvailable += wave9write
        waveIn9.StartRecording()
    if 10 in checkedlist:
        waveIn10.DataAvailable += wave10write
        waveIn10.StartRecording()
        
    
    #waveIn.DataAvailable += wave1write
    #waveIn2.DataAvailable += wave2write
    #waveIn3.DataAvailable += wave3write

    #waveIn.StartRecording()
    #waveIn2.StartRecording()
    #waveIn3.StartRecording()
    filething.sb.SetStatusText("recording started")
    
def gorecordAMODD(shelf):
    devicecount = NAudio.Wave.WaveIn.DeviceCount
    devicelist = []
    for n in range(devicecount):
        devicelist.append(NAudio.Wave.WaveIn.GetCapabilities(n).ProductName)
    print(devicelist)
    #NAudio.Wave.WaveIn.GetCapabilities(0<->range(devicecount)).ProductName
    #-> devicelist !!!
    traceyesno = 0
    if traceyesno == 0:
        pass
    elif traceyesno == 1:
        pdb.set_trace()

    checkedlist = filething.AudioChecker.GetChecked()
    print(checkedlist)
    #pdb.set_trace()
    #filething.rightside.

    #for xx in range(devicecount):
        #global globals()["waveIn" + str(xx)]

    ## replacing range devicecount with for xx in checkedlist:
    for xx in checkedlist:
        globals()["waveIn" + str(xx)] = NAudio.Wave.WaveIn()
    for xx in checkedlist:
        globals()["waveIn" + str(xx)].DeviceNumber = xx
    ##global waveIn
    ##global waveIn2
    ##global waveIn3
    ###waveIn = NAudio.Wave.WaveIn()
    ###waveIn2 = NAudio.Wave.WaveIn()
    ###waveIn3 = NAudio.Wave.WaveIn()
    ####waveIn.DeviceNumber = 0
    ####waveIn2.DeviceNumber = 1
    ####waveIn3.DeviceNumber = 2
    fourfour = 44100
    foureight = 48000
    channels = 2
    for xx in checkedlist:
        globals()["waveIn" + str(xx)].WaveFormat = NAudio.Wave.WaveFormat(fourfour,channels)
    #####waveIn.WaveFormat = NAudio.Wave.WaveFormat(fourfour,channels)
    #####waveIn2.WaveFormat = NAudio.Wave.WaveFormat(fourfour,channels)
    #####waveIn3.WaveFormat = NAudio.Wave.WaveFormat(fourfour,channels)
    #a#import datetime
    timestampz = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    for xx in checkedlist:
        globals()["writer" + str(xx)] = NAudio.Wave.WaveFileWriter(timestampz + "." + str(xx) + '.wav', globals()["waveIn" + str(xx)].WaveFormat)

    ##writer1 = NAudio.Wave.WaveFileWriter(timestampz + ".1.wav", waveIn.WaveFormat)
    ##writer2 = NAudio.Wave.WaveFileWriter(timestampz + ".2.wav", waveIn2.WaveFormat)
    ##writer3 = NAudio.Wave.WaveFileWriter(timestampz + ".3.wav", waveIn3.WaveFormat)

    def wave0write(sender, e):
        if 1 == 1:
            writer0.WriteData(e.Buffer,0,e.BytesRecorded)
            writer0.Flush()
    def wave1write(sender, e):
        if 1 == 1:
            writer1.WriteData(e.Buffer,0,e.BytesRecorded)
            writer1.Flush()
    def wave2write(sender, e):
        if 1 == 1:
            writer2.WriteData(e.Buffer,0,e.BytesRecorded)
            writer2.Flush()
    def wave3write(sender, e):
        if 1 == 1:
            writer3.WriteData(e.Buffer,0,e.BytesRecorded)
            writer3.Flush()
    def wave4write(sender, e):
        if 1 == 1:
            writer4.WriteData(e.Buffer,0,e.BytesRecorded)
            writer4.Flush()
    def wave5write(sender, e):
        if 1 == 1:
            writer5.WriteData(e.Buffer,0,e.BytesRecorded)
            writer5.Flush()
    def wave6write(sender, e):
        if 1 == 1:
            writer6.WriteData(e.Buffer,0,e.BytesRecorded)
            writer6.Flush()
    def wave7write(sender, e):
        if 1 == 1:
            writer7.WriteData(e.Buffer,0,e.BytesRecorded)
            writer7.Flush()
    def wave8write(sender, e):
        if 1 == 1:
            writer8.WriteData(e.Buffer,0,e.BytesRecorded)
            writer8.Flush()
    def wave9write(sender, e):
        if 1 == 1:
            writer9.WriteData(e.Buffer,0,e.BytesRecorded)
            writer9.Flush()
    def wave10write(sender, e):
        if 1 == 1:
            writer10.WriteData(e.Buffer,0,e.BytesRecorded)
            writer10.Flush()



    #for xx in range(devicecount):
        #globals()["waveIn" + str(xx)].DataAvailable += locals()["wave"+str(xx)+"write"]
    ##for xx in range(devicecount):
    '''
    if 'waveIn0' in globals():
        waveIn0.DataAvailable += wave0write
        waveIn0.StartRecording()
    '''

    if 0 in checkedlist:
        waveIn0.DataAvailable += wave0write
        waveIn0.StartRecording()
    if 1 in checkedlist:
        waveIn1.DataAvailable += wave1write
        waveIn1.StartRecording()
    if 2 in checkedlist:
        waveIn2.DataAvailable += wave2write
        waveIn2.StartRecording()
    if 3 in checkedlist:
        waveIn3.DataAvailable += wave3write
        waveIn3.StartRecording()
    if 4 in checkedlist:
        waveIn4.DataAvailable += wave4write
        waveIn4.StartRecording()
    if 5 in checkedlist:
        waveIn5.DataAvailable += wave5write
        waveIn5.StartRecording()
    if 6 in checkedlist:
        waveIn6.DataAvailable += wave6write
        waveIn6.StartRecording()
    if 7 in checkedlist:
        waveIn7.DataAvailable += wave7write
        waveIn7.StartRecording()
    if 8 in checkedlist:
        waveIn8.DataAvailable += wave8write
        waveIn8.StartRecording()
    if 9 in checkedlist:
        waveIn9.DataAvailable += wave9write
        waveIn9.StartRecording()
    if 10 in checkedlist:
        waveIn10.DataAvailable += wave10write
        waveIn10.StartRecording()

    #waveIn.DataAvailable += wave1write
    #waveIn2.DataAvailable += wave2write
    #waveIn3.DataAvailable += wave3write

    #waveIn.StartRecording()
    #waveIn2.StartRecording()
    #waveIn3.StartRecording()
    filething.sb.SetStatusText("recording started")
'''
def gorecord(shelf): #unused. for reference.
    devicecount = NAudio.Wave.WaveIn.DeviceCount
    devicelist = []
    for n in range(devicecount):
        devicelist.append(NAudio.Wave.WaveIn.GetCapabilities(n).ProductName)
    print(devicelist)

    waveIn = NAudio.Wave.WaveIn()
    waveIn2 = NAudio.Wave.WaveIn()
    waveIn3 = NAudio.Wave.WaveIn()

    waveIn.DeviceNumber = 0
    waveIn2.DeviceNumber = 1
    waveIn3.DeviceNumber = 2

    fourfour = 44100
    foureight = 48000
    channels = 2
    waveIn.WaveFormat = NAudio.Wave.WaveFormat(fourfour,channels)
    waveIn2.WaveFormat = NAudio.Wave.WaveFormat(fourfour,channels)
    waveIn3.WaveFormat = NAudio.Wave.WaveFormat(fourfour,channels)

    import datetime
    timestampz = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')

    writer1 = NAudio.Wave.WaveFileWriter(timestampz + ".1.wav", waveIn.WaveFormat)
    writer2 = NAudio.Wave.WaveFileWriter(timestampz + ".2.wav", waveIn2.WaveFormat)
    writer3 = NAudio.Wave.WaveFileWriter(timestampz + ".3.wav", waveIn3.WaveFormat)

    def wave1write(sender, e):
        if 1 == 1:
            #print('ifone')
            ##print(e.Buffer)
            ##print(e.BytesRecorded)
            writer1.WriteData(e.Buffer,0,e.BytesRecorded)
            writer1.Flush()
    def wave2write(sender, e):
        #print('okay2')
        if 1 == 1:
            writer2.WriteData(e.Buffer,0,e.BytesRecorded)
            writer2.Flush()
    def wave3write(sender, e):
        #print('okay3')
        if 1 == 1:
            writer3.WriteData(e.Buffer,0,e.BytesRecorded)
            writer3.Flush()

    waveIn.DataAvailable += wave1write
    waveIn2.DataAvailable += wave2write
    waveIn3.DataAvailable += wave3write

    waveIn.StartRecording()
    waveIn2.StartRecording()
    waveIn3.StartRecording()
'''
def debog(shelf):
    pdb.set_trace()
#https://markheath.net/category/naudio
def mytest(shelf):
    filething.sb.SetStatusText(str(filething.AudioChecker.GetCheckedItems()))
def asio1write(sender, e):
    samples = e.GetAsInterleavedSamples()
    asio1writer.WriteSamples(samples,0,samples.Length)
    asio1writer.Flush()
def mytest2(shelf):
    filething.sb.SetStatusText(str(asiochoice.GetCheckedStrings() ) )
    global asiodev
    asiodev = NAudio.Wave.AsioOut(asiochoice.GetCheckedStrings()[0])
    #stathreadattribute needed > https://github.com/pythonnet/pythonnet/issues/108
    asiodev_channelcount = asiodev.DriverInputChannelCount #6 for Zoom H6
    #https://github.com/naudio/NAudio/blob/master/Docs/AsioRecording.md
    asiodev.InitRecordAndPlayback(None, asiodev_channelcount, 44100)
    import datetime
    timestampz = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    #asiowaveformat = NAudio.Wave.WaveFormat(44100,24,asiodev_channelcount)
    #asiowaveformat = NAudio.Wave.WaveFormat(44100,16,asiodev_channelcount)
    asiowaveformat = NAudio.Wave.WaveFormat(44100,24,asiodev_channelcount)
    global asio1writer
    asio1writer = NAudio.Wave.WaveFileWriter(timestampz + "." + 'poly' + '.wav', asiowaveformat)
    asiodev.AudioAvailable += asio1write
    asiodev.Play()
    #pdb.set_trace()
    
def gbz_add(sender,e):
    global gbz
    gbz.AddSamples(e.Buffer,0,e.BytesRecorded)
    print("finished gbz_add")
    
    #adding samples to gbz..... interesting
    
    global gbw
    gbw.WriteData(e.Buffer,0,e.BytesRecorded)
    gbw.Flush()
    #gbw.write(e.Buffer,0,e.BytesRecorded)
    #gbw.Flush()
    
    '''
    
        def wave0write(sender, e):
        if 1 == 1:
            writer0.WriteData(e.Buffer,0,e.BytesRecorded)
            writer0.Flush()
            
    '''
def loopbackwriter(sender,e):
    if 1 == 1:
        gbw.WriteData(e.Buffer,0,e.BytesRecorded)
        gbw.Flush()
        #somewhereelse#gbw = NAudio.Wave.WaveFileWriter(timestampz + "." + '.loopbak.wav', gbc.WaveFormat)
        
        ###@
        #for xx in checkedlist:
        #globals()["writer" + str(xx)] = NAudio.Wave.WaveFileWriter(timestampz + "." + str(xx) + '.wav', globals()["waveIn" + str(xx)].WaveFormat)
        
def c_addsampz(sender, e):
    if 1 == 1:
        global thisbwp
        thisbwp.AddSamples(e.Buffer,0,e.BytesRecorded)
def c_1addsampz(sender, e):
    if 1 == 1:
        global thisbwp1
        thisbwp1.AddSamples(e.Buffer,0,e.BytesRecorded)
def c_2addsampz(sender, e):
    if 1 == 1:
        global thisbwp2
        thisbwp2.AddSamples(e.Buffer,0,e.BytesRecorded)
def c_3addsampz(sender, e):
    if 1 == 1:
        global thisbwp3
        thisbwp3.AddSamples(e.Buffer,0,e.BytesRecorded)
def c_4addsampz(sender, e):
    if 1 == 1:
        global thisbwp4
        thisbwp4.AddSamples(e.Buffer,0,e.BytesRecorded)
def c_5addsampz(sender, e):
    if 1 == 1:
        global thisbwp5
        thisbwp5.AddSamples(e.Buffer,0,e.BytesRecorded)
def c_6addsampz(sender, e):
    if 1 == 1:
        global thisbwp6
        thisbwp6.AddSamples(e.Buffer,0,e.BytesRecorded)
def c_7addsampz(sender, e):
    if 1 == 1:
        global thisbwp7
        thisbwp7.AddSamples(e.Buffer,0,e.BytesRecorded)
def c_8addsampz(sender, e):
    if 1 == 1:
        global thisbwp8
        thisbwp8.AddSamples(e.Buffer,0,e.BytesRecorded)
def c_9addsampz(sender, e):
    if 1 == 1:
        global thisbwp9
        thisbwp9.AddSamples(e.Buffer,0,e.BytesRecorded)
def c_10addsampz(sender, e):
    if 1 == 1:
        global thisbwp10
        thisbwp10.AddSamples(e.Buffer,0,e.BytesRecorded)
def c_11addsampz(sender, e):
    if 1 == 1:
        global thisbwp11
        thisbwp11.AddSamples(e.Buffer,0,e.BytesRecorded)
def c_12addsampz(sender, e):
    if 1 == 1:
        global thisbwp12
        thisbwp12.AddSamples(e.Buffer,0,e.BytesRecorded)
def c_13addsampz(sender, e):
    if 1 == 1:
        global thisbwp13
        thisbwp13.AddSamples(e.Buffer,0,e.BytesRecorded)
def c_14addsampz(sender, e):
    if 1 == 1:
        global thisbwp14
        thisbwp14.AddSamples(e.Buffer,0,e.BytesRecorded)
def c_15addsampz(sender, e):
    if 1 == 1:
        global thisbwp15
        thisbwp15.AddSamples(e.Buffer,0,e.BytesRecorded)
        
def test666(e):
    print("testing monitoring")
    #think have to get the waveformat for a desired writing track
    #iwaveprovider init
    ## working on NAudio.Wave.IWaveProvider connecting to NAudio.Wave.WaveOut with initializer (<NWIWP)
    
    #trying to connect the wavein to a buffer and then play that to a waveout
    
    devicecount = NAudio.Wave.WaveIn.DeviceCount
    print('wavein devicecount: ' + str(NAudio.Wave.WaveIn.DeviceCount))
    devicelist = []
    for n in range(devicecount):
        devicelist.append(NAudio.Wave.WaveIn.GetCapabilities(n).ProductName)
    print(devicelist)
    
    #choseninput = NAudio.Wave.WaveIn.DeviceNumber = 1
    choseninput = NAudio.Wave.WaveIn()
    choseninput.DeviceNumber = 0
    choseninput.WaveFormat = NAudio.Wave.WaveFormat(44100,2)
    
    global thisbwp
    thisbwp = NAudio.Wave.BufferedWaveProvider(choseninput.WaveFormat)
    #pdb.set_trace()
    
    #NAudio.Wave.BufferedWaveProvider(gbc.WaveFormat)
    ###choseninput.DataAvailable += 
    choseninput.DataAvailable += c_addsampz
    ###3read this
    
    '''    if 0 in checkedlist:
        waveIn0.DataAvailable += wave0write
        waveIn0.StartRecording()
    '''
    '''
        def wave0write(sender, e):
        if 1 == 1:
            writer0.WriteData(e.Buffer,0,e.BytesRecorded)
            writer0.Flush()
    '''
    #anoutput = NAudio.Wave.WaveOut.Init(choseninput)
    #waveOut = NAudio.Wave.WaveOut.Init(thisbwp)
    waveOut = NAudio.Wave.WaveOut(thisbwp)
    waveOut.Init(thisbwp)
    #pdb.set_trace()
    #anoutput = NAudio.Wave.WaveOut()
    choseninput.StartRecording()
    waveOut.DeviceNumber = 0
    waveOut.Play()
    
    # read this vv v vvv vv
    '''
    class AudioCheckList(wx.CheckListBox):
    def __init__(self, parent, id):
        devicecount = NAudio.Wave.WaveIn.DeviceCount
        devicelist = []
        for n in range(devicecount):
            devicelist.append(NAudio.Wave.WaveIn.GetCapabilities(n).ProductName)
        wx.CheckListBox.__init__(self, parent, id,(0,0),(50,50),devicelist)
        #https://docs.wxpython.org/gallery.html shows most widgets
    '''
    # read this vvv vv vvv 
    '''
    for xx in checkedlist:
        globals()["waveIn" + str(xx)] = NAudio.Wave.WaveIn()
    #this initializes the waveIn0-XX objects with defaults important
    for xx in checkedlist:
        globals()["waveIn" + str(xx)].DeviceNumber = xx
    '''
    
    #read this
    '''
    for xx in checkedlist:
        globals()["waveIn" + str(xx)].WaveFormat = NAudio.Wave.WaveFormat(fourfour,channels)
    '''
#def yatta(e,waveoutno,waveinno):
def listrec(e):
    pass
def testone(e):
    test666mdupe(e,0,0)
    print("ran test666mdupe(0,0)")
    #didnt test this at all and it seemed to work fine...
def testthree(e):#just set a trace
    #pdb.set_trace()
    pass
    
    
def testtwo(e):
    global feepy
    global gleebo
    global zorpo
    zorpo = 857328954723
    gleebo = 842791287
    feepy = "im schweepy"
    flip1 = 0
    flip2 = 0
    flip3 = 0
    
    pass
    if flip1 == 0:
        print(type(flip1))
        flip1 = 1
        flipset = "yeas"
    elif flip1 == 1:
        print(type(flip1)+"1")
        flip1 = 0
        flipdec = "yead"
    print("==")
    print(flip1)
    #loc54
    
#def testtwo(e):
    #pass
    
#the button that does this says Moni. i think it's the sixth button
#for this you need to check the box for the input you want to monitor and select the output in the dropdown to the left of the checkbox
def yatta(e):#moni
    #locx3
    print(countah1)
    print(countah2)
    #^initialized back in monitorpanelRev
    #thisrange = range(countah1)
    thisrange = range(countah2)
    
    # this is just a test loop
    '''
    for itx in thisrange:
        #print(globals()["ck"+str(itx)])
        if globals()["ck"+str(itx)].GetValue() == False:
            print("value was false" + str(itx))
        if globals()["mon"+str(itx)].GetSelection() < 10:
            tempy = globals()["mon"+str(itx)].GetSelection()
            print("mon X had getselection less than ten")
            print(tempy)
    '''
    # this is just an end test loop
    #pdb.set_trace()
    #pdb.set_trace()
    #pass
    
    #reading section one rs001 loc5B
    #this is a line from somewhere else vvvvvvvv
    #def test666mdupe(e,waveoutno,waveinno):
    #we are going to call test666mdupe inside of the loop that iterates through the checkboxes
    #if the checkboxd GetValue() is True then the code indented under that runs
    #we want to run the checkboxed lines because the checkbox is whatw the user uses to specify
    #to specify the right hand inputs that go to the outputs in the dropdowns
    #at this point we can only see the outputs by printing them to the console because i didnt add a label object and the name runs off of the area thats inside of a splitter kind of object
    #likewise the input names on the left are cut off due to naudio itself
    #NAudio.Wave.WaveIn.GetCapabilities(n).ProductName
    
    #MonitorChoice GetSelection
    #the two different object ranges for the stupid selector interface are ck0-10ish and mon0-10ish
    #mon is a MonitorChoice type object
    #i shoulda said mon0-9 and ck0-9 cause they're in that left right order
    
    global birdo
    for itx in thisrange:
        if globals()["ck"+str(itx)].GetValue() == True:
            print("starting input"+str(itx)+" to chosen output")
            #test666mdupe(e,globals()["mon"+str(itx)].GetSelection(),itx)
            test666mdupefix(e,globals()["mon"+str(itx)].GetSelection(),itx) #def test666mdupefix(e,waveoutno,waveinno):
            print("getselection of mon " +str(globals()["mon"+str(itx)].GetSelection())+" was used along with check number deviceindex being " + str(itx))
            #pdb.set_trace()
            
            #trying to find something inside of the mon0 extcs objects that i can use to get the thing and its not getvalue
            #probably GetPosition
            #print(globals()["mon"+str(itx)].GetValue())
            ##print(globals()["mon"+str(itx)].GetPosition())
            ##print(type(globals()["mon"+str(itx)].GetPosition()))
            #this gives me the type is a wx core point
            
            #getposition does not work, will try get
            ##print(dir(globals()["mon"+str(itx)]))
            ##print(type(globals()["mon"+str(itx)]))
            print(globals()["mon"+str(itx)].GetSelection()) #dont need this actually
            #this is important line. pwease read this line. the line above prints GetSelection() of the object and this is the chosen output.
            #when we call test666mdupe(e,0,0)
            '''
            def testone(e):
                test666mdupe(e,0,0)
                print("ran test666mdupe(0,0)")
                #didnt test this at all and it seemed to work fine...
    '''
            
            print("not doing anyting")
            print("still not doint anybing")
            print("no but seriously, we are now monitoring "+str(itx) + " on " + str(globals()["mon"+str(itx)].GetSelection() ) )
            print("hit the T6ST button to display the input devices in the same order")
            #each running device chain
            #has a buffered wave provdider
            #thisbwp
            
            #choseninput.DataAvailable += c_addsampz
            #tihs is the prototype lien
            #its approximately 15 lines into the test666m(e,no1,no2) function
            
            
    
    #it will run test666mm multiple times
    #test666mm(waveoutno,waveinno)
    #if the checkbox is checked, play that wavein on the waveout on the thing on the left
def beginMon(e):
    #LocX2
    pass
    #if the checkbox is checked, play that wavein on the waveout on the thing on the left
    #LocX2
def test666mdupefix(e,waveoutno,waveinno):
    print("waveoutno is " + str(waveoutno))
    print("waveinno is " + str(waveinno))
    global tbee
    tbee = tbee + 1
    print(tbee)
    devicecount = NAudio.Wave.WaveIn.DeviceCount
    print('wavein devicecount: ' + str(NAudio.Wave.WaveIn.DeviceCount))
    devicelist = []
    for n in range(devicecount):
        devicelist.append(NAudio.Wave.WaveIn.GetCapabilities(n).ProductName)
    print(devicelist)
    choseninput = NAudio.Wave.WaveIn()
    #choseninput.DeviceNumber = 0
    choseninput.DeviceNumber = waveinno
    choseninput.WaveFormat = NAudio.Wave.WaveFormat(44100,2)
    globals()["thisbwp"+str(tbee)] = NAudio.Wave.BufferedWaveProvider(choseninput.WaveFormat)
#    thisbwp =
    #thisbwp = NAudio.Wave.BufferedWaveProvider(choseninput.WaveFormat)
    choseninput.DataAvailable += globals()["c_"+str(tbee)+"addsampz"]
    waveOut = NAudio.Wave.WaveOut( globals()["thisbwp"+str(tbee)] )
    
#    choseninput.StartRecording()
    #waveOut.DeviceNumber = 0
    waveOut.DeviceNumber = waveoutno
    if type(waveoutno)== int:
        #vvvvvvvvvvvvvvvvvvvv
        waveOut.DeviceNumber = waveoutno
        #^^^^^^^^^^^^^^^^^^
    waveOut.Init( globals()["thisbwp"+str(tbee)] )
    choseninput.StartRecording()
    waveOut.Play()
    
def test666mdupefixbackup(e,waveoutno,waveinno):
    print("waveoutno is " + str(waveoutno))
    print("waveinno is " + str(waveinno))
    global tbee
    tbee = tbee + 1
    print(tbee)
    devicecount = NAudio.Wave.WaveIn.DeviceCount
    print('wavein devicecount: ' + str(NAudio.Wave.WaveIn.DeviceCount))
    devicelist = []
    for n in range(devicecount):
        devicelist.append(NAudio.Wave.WaveIn.GetCapabilities(n).ProductName)
    print(devicelist)
    choseninput = NAudio.Wave.WaveIn()
    #choseninput.DeviceNumber = 0
    choseninput.DeviceNumber = waveinno
    choseninput.WaveFormat = NAudio.Wave.WaveFormat(44100,2)
    globals()["thisbwp"+str(tbee)] = NAudio.Wave.BufferedWaveProvider(choseninput.WaveFormat)
    #^instantiates the thisbwp
    #tbee is a global integer object that is 1 for the first thisbwp1, this is the top level of the function its not a loop
    
#    thisbwp =
    #thisbwp = NAudio.Wave.BufferedWaveProvider(choseninput.WaveFormat)
    choseninput.DataAvailable += globals()["c_"+str(tbee)+"addsampz"]
    waveOut = NAudio.Wave.WaveOut( globals()["thisbwp"+str(tbee)] )
    waveOut.Init( globals()["thisbwp"+str(tbee)] )
#    choseninput.StartRecording()
    #waveOut.DeviceNumber = 0
    waveOut.DeviceNumber = waveoutno
    if type(waveoutno)== int:
        #vvvvvvvvvvvvvvvvvvvv
        waveOut.DeviceNumber = waveoutno
        #^^^^^^^^^^^^^^^^^^
    choseninput.StartRecording()
    waveOut.Play()
def test666mdupe(e,waveoutno,waveinno):
    print("testing monitoring 666m")
    #think have to get the waveformat for a desired writing track
    #iwaveprovider init
    ## working on NAudio.Wave.IWaveProvider connecting to NAudio.Wave.WaveOut with initializer (<NWIWP)
    
    #trying to connect the wavein to a buffer and then play that to a waveout
    
    devicecount = NAudio.Wave.WaveIn.DeviceCount
    print('wavein devicecount: ' + str(NAudio.Wave.WaveIn.DeviceCount))
    devicelist = []
    for n in range(devicecount):
        devicelist.append(NAudio.Wave.WaveIn.GetCapabilities(n).ProductName)
    print(devicelist)
    
    #choseninput = NAudio.Wave.WaveIn.DeviceNumber = 1
    choseninput = NAudio.Wave.WaveIn()
    choseninput.DeviceNumber = 0
    #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    choseninput.DeviceNumber = waveinno
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    choseninput.WaveFormat = NAudio.Wave.WaveFormat(44100,2)
    
    global thisbwp
    thisbwp = NAudio.Wave.BufferedWaveProvider(choseninput.WaveFormat)
    #NAudio.Wave.BufferedWaveProvider(gbc.WaveFormat)
    ###choseninput.DataAvailable += 
    choseninput.DataAvailable += c_addsampz
    ###3read this
    
    '''    if 0 in checkedlist:
        waveIn0.DataAvailable += wave0write
        waveIn0.StartRecording()
    '''
    '''
        def wave0write(sender, e):
        if 1 == 1:
            writer0.WriteData(e.Buffer,0,e.BytesRecorded)
            writer0.Flush()
    '''
    #anoutput = NAudio.Wave.WaveOut.Init(choseninput)
    #waveOut = NAudio.Wave.WaveOut.Init(thisbwp)
    waveOut = NAudio.Wave.WaveOut(thisbwp)
    waveOut.Init(thisbwp)
    #pdb.set_trace()
    #anoutput = NAudio.Wave.WaveOut()
    choseninput.StartRecording()
    waveOut.DeviceNumber = 0
    if type(waveoutno)== int:
        #vvvvvvvvvvvvvvvvvvvv
        waveOut.DeviceNumber = waveoutno
        #^^^^^^^^^^^^^^^^^^
    waveOut.Play()
#####function 1aaa

def test666m(e,waveoutno,waveinno):
    print("testing monitoring 666m")
    #think have to get the waveformat for a desired writing track
    #iwaveprovider init
    ## working on NAudio.Wave.IWaveProvider connecting to NAudio.Wave.WaveOut with initializer (<NWIWP)
    
    #trying to connect the wavein to a buffer and then play that to a waveout
    
    devicecount = NAudio.Wave.WaveIn.DeviceCount
    print('wavein devicecount: ' + str(NAudio.Wave.WaveIn.DeviceCount))
    devicelist = []
    for n in range(devicecount):
        devicelist.append(NAudio.Wave.WaveIn.GetCapabilities(n).ProductName)
    print(devicelist)
    
    #choseninput = NAudio.Wave.WaveIn.DeviceNumber = 1
    choseninput = NAudio.Wave.WaveIn()
    choseninput.DeviceNumber = 0
    choseninput.DeviceNumber = waveinno
    choseninput.WaveFormat = NAudio.Wave.WaveFormat(44100,2)
    
    global thisbwp
    thisbwp = NAudio.Wave.BufferedWaveProvider(choseninput.WaveFormat)
    #NAudio.Wave.BufferedWaveProvider(gbc.WaveFormat)
    ###choseninput.DataAvailable += 
    choseninput.DataAvailable += c_addsampz
    ###3read this
    
    '''    if 0 in checkedlist:
        waveIn0.DataAvailable += wave0write
        waveIn0.StartRecording()
    '''
    '''
        def wave0write(sender, e):
        if 1 == 1:
            writer0.WriteData(e.Buffer,0,e.BytesRecorded)
            writer0.Flush()
    '''
    #anoutput = NAudio.Wave.WaveOut.Init(choseninput)
    #waveOut = NAudio.Wave.WaveOut.Init(thisbwp)
    waveOut = NAudio.Wave.WaveOut(thisbwp)
    waveOut.Init(thisbwp)
    #pdb.set_trace()
    #anoutput = NAudio.Wave.WaveOut()
    choseninput.StartRecording()
    waveOut.DeviceNumber = 0
    if type(waveoutno)== int:
        waveOut.DeviceNumber = waveoutno
    waveOut.Play()
def t6st(e):
    pass
    mon0.GetSelection()
    global pizza
    pizza = NAudio.Wave.WaveOut
    #
def enumerateLB(e):
    gbc = NAudio.Wave.WasapiLoopbackCapture()
    gba = gbc.GetDefaultLoopbackCaptureDevice()
    waveFormat = NAudio.Wave.WaveFormat.CreateIeeeFloatWaveFormat(44100, 2);
    pdb.set_trace()
    
def testlistrec(e):
    devicecount = NAudio.Wave.WaveIn.DeviceCount
    print('wavein devicecount: ' + str(NAudio.Wave.WaveIn.DeviceCount))
    devicelist = []
    for n in range(devicecount):
        print( "input" + str(n) + NAudio.Wave.WaveIn.GetCapabilities(n).ProductName)
        devicelist.append(NAudio.Wave.WaveIn.GetCapabilities(n).ProductName)
    #print(devicelist)

#test65
#ogg52" no bad name
def test65(e):
    #capture = WasapiLoopbackCapture()
    #this wasn't right i dont think
    captcha = NAudio.Wave.WasapiLoopbackCapture()
    captchab = captcha.GetDefaultLoopbackCaptureDevice()
    #wave_format = capture.WaveFormat
    #this was associated with that other line above
    #wave_format = NAudio.Wave.WaveFormat.Create
    wave_format = NAudio.Wave.WaveFormat(44100,2)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    #file_name = f"output_{timestamp}.ogg"
    if type(timestamp) == str:
        filename = "loopbakk" + timestamp + ".ogg"
    else:
        print("timestamp wasnt a string somehow")
    # Create an OGG Vorbis writer
    
    '''
    we need to read this
    def enumerateLB(e):
    gbc = NAudio.Wave.WasapiLoopbackCapture()
    gba = gbc.GetDefaultLoopbackCaptureDevice()
    waveFormat = NAudio.Wave.WaveFormat.CreateIeeeFloatWaveFormat(44100, 2);
    pdb.set_trace()
    '''
    #choseninput.WaveFormat = NAudio.Wave.WaveFormat(44100,2)
    #we need to set wave_format to something
    
    #writer = pyogg.Writer("output.ogg", wave_format.sample_rate, wave_format.channels)
    writer65 = pyogg.Writer(filename, wave_format.sample_rate, wave_format.channels)

    # Callback function for capturing audio data
    def callback65(data, length):
        writer65.write(data, length)

    captcha.DataAvailable += callback65

    captcha.StartRecording()

    # Run the capture for a fixed duration or until interrupted
    captcha.RecordingStopped.WaitOne()

    captcha.StopRecording()
    captcha.Dispose()

    writer65.close()

def test64(e):#button four
    #print("whatever broh")
    print("writing a wav file with default wasapilkoopbackcapture")
    gbc = NAudio.Wave.WasapiLoopbackCapture()
    gba = gbc.GetDefaultLoopbackCaptureDevice()
    #i think this line is necessary for some weird reason. gba doesnt get accessed.
    #gbc.WaveFormat goes into gbw as param 2
    #gbw is a WaveFileWriter
    waveFormat = NAudio.Wave.WaveFormat.CreateIeeeFloatWaveFormat(44100, 2);
    #pdb.set_trace()
    #xyz = gba.WaveFormat
    #xyz = gbc.WaveFormat
    
    print("gba.ID")
    print(gba.ID)
    print("gba.FriendlyName")
    print(gba.FriendlyName)
    timestampz = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    print("waveformat, capturestate, capturestate vv")
    print(gbc.WaveFormat)
    print(gbc.CaptureState)
    
    global gbw
    gbw = NAudio.Wave.WaveFileWriter(timestampz + "." + '.loopbak.wav', gbc.WaveFormat)
    #^ here they're using the gbc.WaveFormat
    print(gbw)
    
    global gbz
    gbz = NAudio.Wave.BufferedWaveProvider(gbc.WaveFormat)
    
    global WOUTZ
    WOUTZ = NAudio.Wave.WaveOut()
    
    global gbx
    gbx = NAudio.Wave.WaveFloatTo16Provider(gbz)
    
    #gbc.DataAvailable += gbz_add
    gbc.DataAvailable += loopbackwriter
    '''
    def loopbackwriter(sender,e):
    if 1 == 1:
        gbw.WriteData(e.Buffer,0,e.BytesRecorded)
        gbw.Flush()
    '''
    gbc.StartRecording()
    #i think this might be it..
    
    WOUTZ.Init(gbx)
    WOUTZ.Play()
    
    '''
    NAudio.Wave.WaveFileWriter(timestampz + "." + str(xx) + '.wav', globals()["waveIn" + str(xx)].WaveFormat)
    '''
    #NAudio.Wave.WaveFileWriter(timestampz + "." + str(xx) + '.wav', globals()["waveIn" + str(xx)].WaveFormat)

#https://markheath.net/post/how-to-record-and-play-audio-at-same
#https://archive.codeplex.com/?p=naudio
#https://github.com/naudio/NAudio/wiki
app=wx.App(0)
filething = FileMgr(None,420,'Simultaneous Multi Wav Recorder')
filething2 = FileMgr2(None,421,'WASAPI Record and/or Monitor')
filething.Show(True)
filething2.Show(True)
#try this lol
#okay so apparently you can do this
#working two lines section double ## commented
##filething2 = FileMgr(None,421,'Second Window')
##filething2.Show(True)
#"#maybe i could make another Frame with another SplitterWindow inside of it..."

##could probably do some stuff here
#\
##print(mon0.GetSelection())
##print(mon0.GetSelection())
##print(mon0.GetSelection())
##print(type(mon0.GetSelection()))
#/
#print(mon0.getselection())


#pdb.set_trace()
## i dunno though hahahaha
##pdb.set_trace()

app.MainLoop()
print("will you ever see thios?")
#http://pythonnet.github.io/
#https://channel9.msdn.com/coding4fun/articles/NET-Voice-Recorder

#things to searrch to get to places
#MonitorChoice
#
############~~!~mon0.GetSelection()
###############~DeviceNumber <------
#mon0 - mon7
#"mon"

#it's not GetPosition it's mon0.GetSelection()

#5-31-2023 12:13am 1083 lines length. looking at "thisbwp"
#6-6-2023 upgrayde.py splitterwindow only holds two things so looking into using two frames (FileMgr & NewFileMgr).. unusual behavior with using monitor on both... not going to bother debugging... commented out.
#what are we trying to do? we want to enumerate the wasapi loopback choices, create a function similar to "def test666mdupefix(e,waveoutno,waveinno):", and a function similar to "def yatta"
#was thinking a checkbox and dropdown like the other section... but maybe i could have two checkboxes, one to record or not...... that would be cool
