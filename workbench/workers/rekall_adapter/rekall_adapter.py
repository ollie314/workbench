
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

    def __init__(self, raw_bytes):
        """Initialization."""

        # Spin up the logging
        logging.getLogger().setLevel(logging.ERROR)
        self.session = MemSession(raw_bytes)
        self.renderer = WorkbenchRenderer(session=self.session)

    def get_session(self):
        ''' Return the Rekall session object '''
        return self.session

    def get_renderer(self):
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
        
        # Ensure the action's Progress() method is called when Rekall reports progress.
        # self.progress.Register(id(self), lambda *_, **__: self.progress())


class WorkbenchRenderer(DataExportRenderer):
    """Workbench Renderer: Extends DataExportRenderer and simply populates local python
        data structures, not meant to be serialized or sent over the network."""

    def __init__(self, session):
        self.__class__.__name__ = 'DataExportRenderer'  # Errr.. this is a fixme
        self.output_data = None
        self.session = session
        super(WorkbenchRenderer, self).__init__(session=session)

    def start(self, plugin_name=None, kwargs=None):
        """Start method: initial data structures and store some meta data."""
        super(WorkbenchRenderer, self).start(plugin_name=plugin_name)
        self.output_data = {'plugin_name': plugin_name}
        return self

    '''
    def table_row(self, *args, **options):
        result = {}
        for i, arg in enumerate(args):
            column_spec = self.table.column_specs[i]
            object_renderer = self.object_renderers[i]

            column_name = column_spec.get("cname", column_spec.get("name"))
            if column_name:
                result[column_name] = arg

        self.SendMessage(["r", result])
    '''

    def SendMessage(self, statement):
        print statement

# Unit test: Create the class, the proper input and run the execute() method for a test
import pytest
@pytest.mark.rekall
def test():
    """rekall_adapter.py: Test."""

    # Do we have the memory forensics file?
    data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../data/memory_images/exemplar4.vmem')
    if not os.path.isfile(data_path):
        print 'Not finding exemplar4.mem... Downloading now...'
        import urllib
        urllib.urlretrieve('http://s3-us-west-2.amazonaws.com/workbench-data/memory_images/exemplar4.vmem', data_path)

    # Did we properly download the memory file?
    if not os.path.isfile(data_path):
        print 'Could not open exemplar4.vmem'
        sys.exit(1)

    # Got the file, now process it
    raw_bytes = open(data_path, 'rb').read()

    adapter = RekallAdapter(raw_bytes)
    session = adapter.get_session()
    renderer = adapter.get_renderer()

    # Create any kind of plugin supported by this session
    output = session.RunPlugin('imageinfo', renderer=renderer)
    pprint.pprint(output)
    assert 'Error' not in output

    output = session.RunPlugin('pslist', renderer=renderer)
    pprint.pprint(output)
    assert 'Error' not in output

    output = session.RunPlugin('dlllist', renderer=renderer)
    pprint.pprint(output)
    assert 'Error' not in output


if __name__ == "__main__":
    test()
