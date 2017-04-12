import wx
import noname
import matplotlib.pyplot as plt
import numpy as np
import csv
import stuff
import Thread
import visa
import pywxgrideditmixin
import tables
import time

class MainFrame( noname.MyFrame1 ):
    def __init__( self, parent ):
        noname.MyFrame1.__init__( self, parent)
        #the mixin below offers better ctrl c ctr v cut and paste than the basic wxgrid
        wx.grid.Grid.__bases__ += (pywxgrideditmixin.PyWXGridEditMixin,)
        self.m_grid7.__init_mixin__()
        self.EVT_RESULT_ID_1 = wx.NewId() #used for GPIB data 1 thread
        self.worker = None # for data source 1
        stuff.EVT_RESULT(self, self.OnResult1, self.EVT_RESULT_ID_1)
        self.inst_bus = visa # can be toggled (OnSimulate) to visa 2 for simulation

    def OnRun(self,event):
        Port = self.PortBox.GetValue()
        Harmonics = self.HarmonicsBox.GetValue()
        Name = self.NameBox.GetValue()
        Bursts = self.BurstsBox.GetValue()
        Readings = self.ReadingsBox.GetValue()
        Time = self.TimeBox.GetValue()
        Range = self.RangeBox.GetValue()
        ACDC = self.ACDCcheck.GetValue()
        AC = self.ACcheck.GetValue()
        MEAN = self.MEANcheck.GetValue()

        self.grid = self.m_grid7

        self.worker = Thread.Algorithm(port = Port,harmonics = Harmonics,name=Name,bursts=Bursts,readings = Readings,time=Time,rng = Range,acdc = ACDC,ac=AC,mean=MEAN,grid = self.grid)

    def OnReset(self,event):
        pass

    def OnSave(self,event):
        pass
    
    def OnGraph(self,event):
        pass
    
    def OnResult1(self, event):
        """Show Result status, event for termination of gpib thread"""
        
        if event.data is None:
            # Thread aborted (using our convention of None return)
            print('GPIB data aborted'), time.strftime("%a, %d %b %Y %H:%M:%S", Time)
        else:
            # Process results here
            print'GPIB Result: %s' % event.data,time.strftime("%a, %d %b %Y %H:%M:%S", Time)
        
    
        # In either event, the worker is done
        self.worker1 = None

    
    def OnClose(self, event):
        """
        Make sure threads not running if frame is closed before stopping everything.
        Seems to generate errors, but at least the threads do get stopped!
        The delay after stopping the threads need to be longer than the time for
        a thread to normally complete?
        """
        if self.worker: #stop main GPIB thread
            self.worker.abort()
            time.sleep(0.3)
        self.Destroy()


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame(None)
    frame.Show(True)
    app.MainLoop()
