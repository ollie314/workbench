
''' Unzip worker '''
import StringIO
import zipfile
import zerorpc

class Unzip(object):
    ''' This worker unzips a zipped file '''
    dependencies = ['sample']

    def __init__(self):
        self.c = zerorpc.Client()
        self.c.connect("tcp://127.0.0.1:4242")

    def execute(self, input_data):
        raw_bytes = input_data['sample']['raw_bytes']
        zipfile_output = zipfile.ZipFile(StringIO.StringIO(raw_bytes))
        payload_md5s = []
        for name in zipfile_output.namelist():
            payload_md5s.append(self.c.store_sample(name,zipfile_output.read(name), 'unknown'))
        return {'payload_md5s': payload_md5s}

    def __del__(self):
        ''' Class Cleanup '''
        # Close zeroRPC client
        self.c.close()

# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' unzip.py: Unit test'''

    # This worker test requires a local server running
    import zerorpc
    c = zerorpc.Client()
    c.connect("tcp://127.0.0.1:4242")

    # Generate input for the worker
    md5 = c.store_sample('bad.zip', open('../../data/zip/bad.zip', 'rb').read(), 'zip')
    md5_2 = c.store_sample('good.zip', open('../../data/zip/good.zip', 'rb').read(), 'zip')
    input_data = c.get_sample(md5)
    input_data_2 = c.get_sample(md5_2)    

    # Execute the worker (unit test)
    worker = Unzip()
    output = worker.execute(input_data)
    print '\n<<< Unit Test >>>'
    import pprint
    pprint.pprint(output)

    # For coverage
    output = worker.execute(input_data_2)

    # Execute the worker (server test)
    output = c.work_request('unzip', md5)
    print '\n<<< Server Test >>>'
    import pprint
    pprint.pprint(output)

if __name__ == "__main__":
    test()
