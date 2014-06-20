''' view_pcap worker '''
import zerorpc

class ViewPcap(object):
    ''' ViewPcap: Generates a view for a pcap sample (depends on Bro)'''
    dependencies = ['pcap_bro']

    def __init__(self):
        self.c = zerorpc.Client()
        self.c.connect("tcp://127.0.0.1:4242")

    def execute(self, input_data):
        ''' Execute '''
        view = {}

        # Grab logs from Bro
        view['bro_logs'] = {key: input_data['pcap_bro'][key] for key in input_data['pcap_bro'].keys() if '_log' in key}

        # Grab logs from Bro
        view['extracted_files'] = input_data['pcap_bro']['extracted_files']

        return view

    def __del__(self):
        ''' Class Cleanup '''
        # Close zeroRPC client
        self.c.close()

# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' view_pcap.py: Unit test'''

    # This worker test requires a local server running
    import zerorpc
    c = zerorpc.Client()
    c.connect("tcp://127.0.0.1:4242")

    # Generate input for the worker
    md5 = c.store_sample('winmedia.pcap', open('../../data/pcap/winmediaplayer.pcap', 'rb').read(), 'pcap')
    input_data = c.get_sample(md5)
    input_data.update(c.work_request('pcap_bro', md5))

    # Execute the worker (unit test)
    worker = ViewPcap()
    output = worker.execute(input_data)
    print '\n<<< Unit Test >>>'
    import pprint
    pprint.pprint(output)

    # Execute the worker (server test)
    output = c.work_request('view_pcap', md5)
    print '\n<<< Server Test >>>'
    import pprint
    pprint.pprint(output)

if __name__ == "__main__":
    test()
