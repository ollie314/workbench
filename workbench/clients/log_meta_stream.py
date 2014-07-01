''' This client get meta data about log files '''
import zerorpc
import os
import pprint
import ConfigParser

def main():
    ''' This client get meta data about log files '''
    
    # Grab server info from configuration file
    workbench_conf = ConfigParser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.ini')
    workbench_conf.read(config_path)
    server = workbench_conf.get('workbench', 'server_uri') 
    port = workbench_conf.get('workbench', 'server_port')

    # Start up workbench connection
    workbench = zerorpc.Client()
    workbench.connect('tcp://'+server+':'+port)

    # Test out some log files
    data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'../data/log')
    file_list = [os.path.join(data_path, child) for child in os.listdir(data_path)]
    for filename in file_list:
        with open(filename,'rb') as f:

            # Skip OS generated files
            if '.DS_Store' in filename: continue

            md5 = workbench.store_sample(filename, f.read(), 'log')
            results = workbench.work_request('view_log_meta', md5)
            print 'Filename: %s\n' % (filename)
            pprint.pprint(results)
            stream_log = workbench.stream_sample(md5, 20)
            for row in stream_log:
                print row

def test():
    ''' log_meta_stream test '''
    main()

if __name__ == '__main__':
    main()

