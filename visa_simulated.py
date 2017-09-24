"""
Simulated visa module.
"""

import stuff
import time

"""
Old pyvisa calls.
"""
def get_instruments_list():
    #specific to this setup
    return ['GPIB0::16', 'GPIB0::22']
    

class Gpib(object):
    def send_ifc(self):
        return    
 
class GpibInstrument(object):
    def __init__(self, name):
        self.name = name
        self.data = stuff.DataGen()
            
    def write(self, command):
        time.sleep(0.1)
        return
            
    def read_values(self):
        time.sleep(0.2)
        return [self.data.next()]
        
    
class VisaIOError(object):
    """Exception class for VISA I/O errors.

    Please note that all values for "error_code" are negative according to the
    specification (VPP-4.3.2, observation 3.3.2) and the NI implementation.

    """
    def __init__(self, error_code):
        abbreviation, description = _completion_and_error_messages[error_code]
        Error.__init__(self, abbreviation + ": " + description)
        self.error_code = error_code

"""
New pyVisa calls, post 1.4
"""


class SpecificItem(object):
    """
    All the dummy methods that a specific item (instrument or bus)is expected
    to have
    """
    def __init__(self, name):
        self.name = name
        self.data = stuff.DataGen()
    
    def send_ifc(self):
        return
        
    def write(self,something):
        return
        
    def read_raw(self):
        time.sleep(0.2)
        return self.data.next()
    
    def read(self):
        time.sleep(0.2)
        return self.data.next()
    
    def query(self,something):
        self.write(something)
        return self.read()

class ResourceManager(object):
    """
    Newer pyVisa approach
    """
    def list_resources(self):
        return ['GPIB0::10', 'GPIB0::16']
        
    def open_resource(self, specific_item):
        specific_item = SpecificItem(specific_item)
        return specific_item
