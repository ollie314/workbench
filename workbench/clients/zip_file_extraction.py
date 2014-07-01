''' This client shows workbench extacting files from a zip file '''
import zerorpc
import os
import pprint
import argparse
import ConfigParser

def main():
    ''' This client shows workbench extacting files from a zip file '''
    
    # Grab server info from configuration file
    workbench_conf = ConfigParser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.ini')
    workbench_conf.read(config_path)
    server = workbench_conf.get('workbench', 'server_uri') 
    port = workbench_conf.get('workbench', 'server_port')

    # Start up workbench connection
    workbench = zerorpc.Client()
    workbench.connect('tcp://'+server+':'+port)

    # Test out zip data
    data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'../data/zip')
    file_list = [os.path.join(data_path, child) for child in os.listdir(data_path)]
    for filename in file_list:
        with open(filename,'rb') as f:
            md5 = workbench.store_sample(filename, f.read(), 'zip')
            results = workbench.work_request('view', md5)
            print 'Filename: %s ' % (filename)
            pprint.pprint(results)

            # The unzip worker gives you a list of md5s back
            # Run meta on all the unzipped files.
            results = workbench.work_request('unzip', md5)
            print '\n*** Filename: %s ***' % (filename)
            for child_md5 in results['unzip']['payload_md5s']:
                pprint.pprint(workbench.work_request('meta', child_md5))


def test():
    ''' simple_workbench_client test '''
    main()

if __name__ == '__main__':
    main()

