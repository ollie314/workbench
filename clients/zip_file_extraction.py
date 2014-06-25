''' This client shows workbench extacting files from a zip file '''
import zerorpc
import os
import pprint
import argparse
import ConfigParser

def main():
    
    # Grab server info from configuration file
    workbench_conf = ConfigParser.ConfigParser()
    workbench_conf.read('config.ini')
    server = workbench_conf.get('workbench', 'server_uri') 
    port = workbench_conf.getint('workbench', 'server_port') 

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=port, help='port used by workbench server')
    parser.add_argument('-s', '--server', type=str, default=server, help='location of workbench server')
    args = parser.parse_args()
    port = str(args.port)
    server = str(args.server)

    # Start up workbench connection
    workbench = zerorpc.Client()
    workbench.connect('tcp://'+server+':'+port)

    # Test out zip data
    file_list = [os.path.join('../data/zip', child) for child in os.listdir('../data/zip')]
    for filename in file_list:
        with open(filename,'rb') as file:
            md5 = workbench.store_sample(filename, file.read(), 'zip')
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

