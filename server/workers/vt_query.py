
''' VTQuery worker '''
import requests
import collections
import workbench_keys

class VTQuery(object):
    ''' This worker query Virus Total, an apikey needs to be provided '''
    dependencies = ['meta']
    
    def __init__(self, apikey=None):
        ''' VTQuery Init'''

        # Grab our API key
        if apikey:
            self.apikey = apikey
        else:
            self.apikey = workbench_keys.API_KEYS['vt_apikey']

        # Make sure key isn't the dummy value
        if self.apikey == '123':
            raise RuntimeError('VTQuery: Invalid api_key, put your VT api key in the config.ini file.')
        
        # Change this if you want these fields
        self.exclude = ['scan_id', 'md5', 'sha1', 'sha256', 'resource', 'response_code', 'permalink',
                        'verbose_msg', 'scans']

    def execute(self, input_data):
        md5 = input_data['meta']['md5']
        response = requests.get('https://www.virustotal.com/vtapi/v2/file/report', 
                                params={'apikey':self.apikey,'resource':md5, 'allinfo':1})

        # Make sure we got a json blob back
        try:
            vt_output = response.json()
        except ValueError:
            return {'vt_error': 'VirusTotal Query Error, no valid response... past per min quota?'}
        
        # Just pull some of the fields
        output = {field:vt_output[field] for field in vt_output.keys() if field not in self.exclude}
        
        # Check for not-found
        not_found = False if output else True        

        # Add in file_type
        output['file_type'] = input_data['meta']['file_type']
        
        # Toss back a not found
        if not_found:
            output['not_found'] = True
            return output

        # Organize the scans fields
        scan_results = collections.Counter()
        for scan in vt_output['scans'].values():
            if 'result' in scan:
                if scan['result']:
                    scan_results[scan['result']] += 1
        output['scan_results'] = scan_results.most_common(5)
        return output


# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' vt_query.py: Unit test'''

    try:
        import configparser
    except ImportError:
        import ConfigParser as configparser

    # Grab API key from configuration file
    workbench_conf = configparser.ConfigParser()
    workbench_conf.read('../config.ini')
    vt_api = workbench_conf.get('workbench', 'vt_apikey', fallback='123')

    # This worker test requires a local server running
    import zerorpc
    c = zerorpc.Client()
    c.connect("tcp://127.0.0.1:4242")

    # Generate input for the worker
    md5 = c.store_sample('bad_pdf', open('../../data/pdf/bad/067b3929f096768e864f6a04f04d4e54', 'rb').read(), 'pdf')
    input_data = c.get_sample(md5)
    input_data.update(c.work_request('meta', md5))

    # Execute the worker (unit test)
    worker = VTQuery(vt_api)
    output = worker.execute(input_data)
    print '\n<<< Unit Test >>>'
    import pprint
    pprint.pprint(output)

    # Execute the worker (server test)
    output = c.work_request('vt_query', md5)
    print '\n<<< Server Test >>>'
    import pprint
    pprint.pprint(output)

if __name__ == "__main__":
    test()
