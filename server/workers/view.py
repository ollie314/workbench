
''' view worker '''
import zerorpc

def plugin_info():
    return {'name':'view', 'class':'View', 'dependencies': ['meta'],
            'description': 'This worker generates a view for any type of file. Output keys: [this view calls sub-views, see the concrete class (view_pdf for instance)]'}

class View():
    ''' View: Generates a view for any file type '''
    def __init__(self):
        self.c = zerorpc.Client()
        self.c.connect("tcp://127.0.0.1:4242")

    def execute(self, input_data):

        # Grab the mime_type from the input and switch view types
        md5 = input_data['meta']['md5']
        mime_type = input_data['meta']['mime_type']
        if mime_type == 'application/x-dosexec':
            return self.c.work_request('view_pefile', md5)
        elif mime_type == 'application/pdf':
            return self.c.work_request('view_pdf', md5)
        elif mime_type == 'application/zip':
            return self.c.work_request('view_zip', md5)
        elif mime_type == 'application/vnd.tcpdump.pcap':
            return self.c.work_request('view_pcap_meta', md5)
        else:
            # In the case of an unsupported MIME type just return the meta data
            return input_data


# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' view.py: Unit test'''
    import pprint

    # This worker test requires a local server as it relies heavily on the recursive dependencies
    c = zerorpc.Client()
    c.connect("tcp://127.0.0.1:4242")
    md5 = c.store_sample('bad_067b39', open('../../test_files/pdf/bad/067b3929f096768e864f6a04f04d4e54', 'rb').read(), 'pdf')
    output = c.work_request('view', md5)
    print '\nView: '
    pprint.pprint(output)
    md5 = c.store_sample('bad_033d91', open('../../test_files/pe/bad/033d91aae8ad29ed9fbb858179271232', 'rb').read(), 'pe')
    output = c.work_request('view', md5)
    print '\nView: '
    pprint.pprint(output)
    md5 = c.store_sample('good.zip', open('../../test_files/zip/good.zip', 'rb').read(), 'zip')
    output = c.work_request('view', md5)
    print '\nView: '
    pprint.pprint(output)
    md5 = c.store_sample('workbench.py', open('../../server/workbench.py', 'rb').read(), 'python')
    output = c.work_request('view', md5)
    print '\nView: '
    pprint.pprint(output)

if __name__ == "__main__":
    test()