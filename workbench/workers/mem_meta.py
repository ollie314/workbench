
''' Memory Image Meta worker. This worker utilizes the Rekall Memory Forensic Framework.
    See Google Github: http://github.com/google/rekall
    All credit for good stuff goes to them, all credit for bad stuff goes to us. :)
'''
import os
import hashlib
import mem_base

class MemoryImageMeta(mem_base.MemoryImageBase):
    ''' This worker computes meta-data for memory image files. '''
    dependencies = ['sample']

    def __init__(self):
        ''' Initialization '''
        super(MemoryImageMeta, self).__init__()
        self.set_plugin_name('imageinfo')

# Unit test: Create the class, the proper input and run the execute() method for a test
import pytest
@pytest.mark.xfail
def test():
    ''' mem_meta.py: Test '''

    # This worker test requires a local server running
    import zerorpc
    workbench = zerorpc.Client(timeout=120)
    workbench.connect("tcp://127.0.0.1:4242")

    # Store the sample
    data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../data/memory_images/exemplar4.vmem')
    with open(data_path, 'rb') as mem_file:
        raw_bytes = mem_file.read()
        md5 = hashlib.md5(raw_bytes).hexdigest()
        if not workbench.has_sample(md5):
            md5 = workbenchstore_sample('exemplar4.vmem', open(data_path, 'rb').read(), 'mem')

    # Execute the worker (unit test)
    worker = MemoryImageMeta()
    output = worker.execute({'sample':{'raw_bytes':raw_bytes}})
    print '\n<<< Unit Test >>>'
    import pprint
    pprint.pprint(output)
    assert 'Error' not in output

    # Execute the worker (server test)
    output = workbench.work_request('mem_meta', md5)
    print '\n<<< Server Test >>>'
    import pprint
    pprint.pprint(output)
    assert 'Error' not in output


if __name__ == "__main__":
    test()
