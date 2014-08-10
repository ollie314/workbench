
"""rekall_adapter: Helps Workbench utilize the Rekall Memory Forensic Framework.
    See Google Github: http://github.com/google/rekall
    All credit for good stuff goes to them, all credit for bad stuff goes to us. :).
"""


import os, sys
import logging
from rekall import session as rekall_session
from rekall.plugins.addrspaces import standard
from rekall.plugins.renderers.data_export import DataExportRenderer
from rekall.ui.json_renderer import JsonEncoder
import collections
import datetime
import pprint
import pytz
import gevent
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

def gsleep():
    ''' Convenience method for gevent.sleep '''
    print '*** Gevent Sleep ***'
    gevent.sleep(0)

class RekallAdapter(object):
    """RekallAdapter: Helps utilize the Rekall Memory Forensic Framework."""

    def __init__(self):
        """Initialization."""

        # Spin up the logging
        logging.getLogger().setLevel(logging.ERROR)
        self.plugin_name = 'imageinfo'
        self.session = None
        self.renderer = None

    def set_plugin_name(self, name):
        ''' Set the name of the plugin to be used '''
        self.plugin_name = name

    def execute(self, input_data):
        ''' Execute method '''

        # Grab the raw bytes of the sample
        raw_bytes = input_data['sample']['raw_bytes']

        # Spin up the rekall session and render components
        self.session = MemSession(raw_bytes)
        self.renderer = WorkbenchRenderer(session=self.session)

        # Run the plugin
        self.session.RunPlugin(self.plugin_name, renderer=self.renderer)

        return self.renderer.get_output()

    def _get_session(self):
        ''' Return the Rekall session object '''
        return self.session

    def _get_renderer(self):
        ''' Return the Rekall renderer object '''
        return self.renderer


class MemSession(rekall_session.JsonSerializableSession):
    """MemSession: Helps utilize the Rekall Memory Forensic Framework."""

    def __init__(self, raw_bytes, fhandle=None): # Put in a pager later
        """Create a Rekall session for this memory image (raw_bytes)"""

        # Set up profile path
        local = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'profiles')
        remote = 'http://profiles.rekall-forensic.com'
        profile_path = [local, remote]

        # Call the parent class with the profile_path
        super(MemSession, self).__init__(profile_path=profile_path)

        # Set up a memory space for our raw memory image
        mem_file = StringIO(raw_bytes) # Change this to a pager later
        self.physical_address_space = standard.FDAddressSpace(fhandle=mem_file, session=self)
        self.GetParameter("profile")


class WorkbenchRenderer(DataExportRenderer):
    """Workbench Renderer: Extends DataExportRenderer and simply populates local python
        data structures, not meant to be serialized or sent over the network."""

    def __init__(self, session):
        """Initialize the WorkbenchRenderer class"""
        self.__class__.__name__ = 'DataExportRenderer'  # Errr.. this is a fixme
        self.output = None
        self.session = session
        self.column_map = {}
        self.current_table_name = 'unknown'
        self.verbose = False
        super(WorkbenchRenderer, self).__init__(session=session)

    def get_output(self):
        return self.output

    def start(self, plugin_name=None, kwargs=None):
        """Start method: initial data structures and store some meta data."""
        self.output = {'tables': collections.defaultdict(list)} # Start basically resets the output data
        super(WorkbenchRenderer, self).start(plugin_name=plugin_name)
        return self

    def parse_eprocess(self, eprocess_data):
        """Parse the EProcess object we get from some rekall output"""
        Name = eprocess_data['_EPROCESS']['Cybox']['Name']
        PID = eprocess_data['_EPROCESS']['Cybox']['PID']
        PPID = eprocess_data['_EPROCESS']['Cybox']['Parent_PID']
        return {'Name': Name, 'PID': PID, 'PPID': PPID}

    def SendMessage(self, statement):
        """Here we're actually capturing messages and putting them into our output"""
        
        # The way messages are 'encapsulated' by Rekall is questionable, 99% of the
        # time it's way better to have a dictionary...shrug...
        message_type = statement[0]
        message_data = statement[1]
        if message_type == 'm':  # Meta
            self.output['meta'] = message_data

        elif message_type == 's': # New Session (Table)
            # I love magic shit like this...
            self.current_table_name = message_data['name'][1] if message_data['name'] else 'unknown'

        elif message_type == 't': # New Table Headers (column names)
            self.column_map = {item['cname']: item['name'] if 'name' in item else item['cname'] for item in message_data}

        elif message_type == 'r': # Row
            # Okay do some dorky stuff based on Rekall having it's own type system
            row = {}
            for key,value in message_data.iteritems():
                # Yea.. this is fun... like toothpicks in my eyeballs...
                if not value:
                    value = '-'                
                elif isinstance(value, list):
                    value = value[1] # Yeah, cause this make sense.. holy shit...
                elif isinstance(value, dict):
                    if 'type_name' in value:
                        if 'UnixTimeStamp' in value['type_name']:
                            value = datetime.datetime.utcfromtimestamp(value['epoch'])
                            if value == datetime.datetime(1970, 1, 1, 0, 0):
                                value = '-'

                # Assume the value is somehow well formed when we get here
                row[self.column_map[key]] = value

            # _EPROCESS processing
            if '_EPROCESS' in message_data:
                row.update(self.parse_eprocess(message_data))
                del row['_EPROCESS']

            # Add the row to our current table
            self.output['tables'][self.current_table_name].append(row)
        elif self.verbose:
            print 'Verbose: Ignoring rekall message of type %s: %s' % (message_type, statement)


# Unit test: Create the class, the proper input and run the execute() method for a test
import pytest
@pytest.mark.rekall
def test():
    ''' rekall_adapter.py: Test '''

    # This worker test requires a local server running
    import zerorpc
    c = zerorpc.Client(timeout=300, heartbeat=60)
    c.connect("tcp://127.0.0.1:4242")

    # Do we have the memory forensics file?
    data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../data/memory_images/exemplar4.vmem')
    if not os.path.isfile(data_path):
        print 'Not finding exemplar4.mem... Downloading now...'
        import urllib
        urllib.urlretrieve('http://s3-us-west-2.amazonaws.com/workbench-data/memory_images/exemplar4.vmem', data_path)

    # Did we properly download the memory file?
    if not os.path.isfile(data_path):
        print 'Downloading failed, try it manually...'
        print 'wget http://s3-us-west-2.amazonaws.com/workbench-data/memory_images/exemplar4.vmem'
        exit(1)

    # Store the sample
    md5 = c.store_sample(open(data_path, 'rb').read(), 'exemplar4.vmem', 'mem')

    # Unit test stuff
    input_data = c.get_sample(md5)

    # Execute the worker (unit test)
    worker = RekallAdapter()
    print '\n<<< Unit Test >>>'
    worker.set_plugin_name('imageinfo')
    output = worker.execute(input_data)    
    pprint.pprint(output['meta'])
    for name, table in output['tables'].iteritems():
        print '\nTable: %s' % name
        pprint.pprint(table)
    worker.set_plugin_name('pslist')
    output = worker.execute(input_data)    
    pprint.pprint(output['meta'])
    for name, table in output['tables'].iteritems():
        print '\nTable: %s' % name
        pprint.pprint(table)
    worker.set_plugin_name('dlllist')
    output = worker.execute(input_data)    
    pprint.pprint(output['meta'])
    for name, table in output['tables'].iteritems():
        print '\nTable: %s' % name
        pprint.pprint(table)    


if __name__ == "__main__":
    test()
