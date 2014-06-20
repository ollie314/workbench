''' PE peid worker. Uses the peid_userdb.txt database of signatures.
'''
import peutils
import pefile
import pkg_resources

# Fixme: We want to load this once per module load
g_peid_sigs = pkg_resources.resource_string(__name__, 'peid_userdb.txt')

class PEIDWorker(object):
    ''' This worker looks up pe_id signatures for a PE file. '''
    dependencies = ['sample']

    def __init__(self):
        self.peid_sigs = g_peid_sigs

    def execute(self, input_data):
        raw_bytes = input_data['sample']['raw_bytes']

        # Have the PE File module process the file
        try:
            pefile_handle = pefile.PE(data=raw_bytes,fast_load=False)
        except Exception, error:
            return {'error':  str(error), 'match_list': []}

        # Now get information from PEID module
        peid_match = self.peid_features(pefile_handle)
        return {'match_list': peid_match}

    def peid_features(self, pefile_handle):
        ''' Get features from PEid signature database'''
        signatures = peutils.SignatureDatabase(data = self.peid_sigs)
        peid_match = signatures.match(pefile_handle)
        return peid_match if peid_match else []

# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' pe_peid.py: Unit test'''

    # This worker test requires a local server running
    import zerorpc
    c = zerorpc.Client()
    c.connect("tcp://127.0.0.1:4242")

    # Generate input for the worker
    md5 = c.store_sample('bad_pe', open('../../data/pe/bad/033d91aae8ad29ed9fbb858179271232', 'rb').read(), 'log')
    input_data = c.get_sample(md5)
    input_data.update(c.work_request('meta', md5))

    # Execute the worker (unit test)
    worker = PEIDWorker()
    output = worker.execute(input_data)
    print '\n<<< Unit Test >>>'
    import pprint
    pprint.pprint(output)

    # Execute the worker (server test)
    output = c.work_request('pe_peid', md5)
    print '\n<<< Server Test >>>'
    import pprint
    pprint.pprint(output)

if __name__ == "__main__":
    test()
