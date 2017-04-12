"""
Useful classes and methods for GUI with events, timers and threaded tasks.
"""
import threading
import wx
import random
import time

class DataGen(object):
    """ A class that generates pseudo-random data for
        display in the plot.  Taken from
        Eli Bendersky (eliben@gmail.com), Last modified: 31.07.2008
    """
    def __init__(self, init=109):
        self.data = self.init = init
        
    def next(self):
        self._recalc_data()
        return self.data
    
    def _recalc_data(self):
        delta = random.uniform(-0.5, 0.5)
        r = random.random()

        if r > 0.9:
            self.data += delta * 15
        elif r > 0.8: 
            # attraction to the initial value
            delta += (0.5 if self.init > self.data else -0.5)
            self.data += delta
        else:
            self.data += delta

class SharedList(object):
    """
    This structure should work for something more complicated. Not necessary for
    just a list?
    """
    def __init__(self, item):
        self.lock = threading.Lock()
        self.item = item
        self.value = [] # this initialisation makes it a list
        
    def add_to_list(self,item): # this method is list specific
        self.lock.acquire()
        self.value.append(item)
        self.lock.release()
        
    def copy_list(self): # need a copy to avoid changes during plotting
        self.lock.acquire()
        a = self.value[:]
        self.lock.release()
        return a
        
    def reset_list(self):
        self.lock.acquire()
        self.value = []
        self.lock.release()

def EVT_RESULT(win, func, EVT):
    """Define Result Event."""
    win.Connect(-1, -1, EVT, func)

class ResultEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self, EVT, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.EVT = EVT
        self.SetEventType(self.EVT)
        self.data = data

# Thread class that executes processing
class WorkerThread(threading.Thread):
    """Worker Thread Class."""
    def __init__(self,**kwargs):
        """Init Worker Thread Class."""
        threading.Thread.__init__(self)
        self._want_abort = 0
        # This starts the thread running on creation, but you could
        # also make the GUI thread responsible for calling this
##         self.start()

    def run(self):
        """Run Worker Thread."""
        # This is the code executing in the new thread. Simulation of
        # a long process (well, 10s here) as a simple loop - you will
        # need to structure your processing so that you periodically
        # peek at the abort variable.
        # Just override this version of run in a derived class.
       
        for i in range(self.param):
            #self.data.append(i)
            self.data.add_to_list(i)
            time.sleep(1)
            if self._want_abort:
                # Use a result of None to acknowledge the abort (of
                # course you can use whatever you'd like or even
                # a separate event type)
                wx.PostEvent(self._notify_window, ResultEvent(self.EVT, None))
                return
        # Here's where the result would be returned (this is an
        # example fixed result of the number 10, but it could be
        # any Python object)
        wx.PostEvent(self._notify_window, ResultEvent(self.EVT, self.param))

    def abort(self):
        """abort worker thread."""
        # Method for use by main thread to signal an abort
        self._want_abort = 1
        
class RedirectText(object):
    """
    A thread-safe class for redirecting stdout/stderr.
    """
    def __init__(self, aWxTextCtrl):
        self.out = aWxTextCtrl
        
    def write(self, string):
        wx.CallAfter(self.out.WriteText, string) #remove CallAfter for no threads.
