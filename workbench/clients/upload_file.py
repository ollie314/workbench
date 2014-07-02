''' This client pushes a file into Workbench '''
import zerorpc
import os
import pprint
import ConfigParser

# We're not using this but it might be handy to someone
'''
def md5_for_file(path, block_size=256*128):
    md5 = hashlib.md5()
    with open(path,'rb') as f:
        for chunk in iter(lambda: f.read(block_size), b''):
            md5.update(chunk)
    return md5.hexdigest()
'''

def main():
    ''' This client pushes a file into Workbench '''
    
    # Grab server info from configuration file
    workbench_conf = ConfigParser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.ini')
    workbench_conf.read(config_path)
    server = workbench_conf.get('workbench', 'server_uri') 
    port = workbench_conf.get('workbench', 'server_port')

    # Start up workbench connection
    workbench = zerorpc.Client()
    workbench.connect('tcp://'+server+':'+port)

    # Upload the files into workbench
    my_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                           '../data/pe/bad/033d91aae8ad29ed9fbb858179271232')
    with open(my_file,'rb') as f:

        # Check to see if workbench already has the file
        filename = os.path.basename(my_file)
        raw_bytes = f.read()
        md5 = workbench.store_sample(filename, raw_bytes, 'log')
        results = workbench.work_request('view', md5)
        print 'Filename: %s' % filename
        pprint.pprint(results)

    # You can also download a sample (commented out)
    '''
    sample = workbench.get_sample(md5)
    raw_bytes = sample['sample']['raw_bytes']
    with open('mysample.log','wb') as f:
        f.write(raw_bytes)
    '''

def test():
    ''' file_upload test '''
    main()

if __name__ == '__main__':
    main()

