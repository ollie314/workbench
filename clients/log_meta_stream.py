
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
    c = zerorpc.Client()
    c.connect('tcp://'+server+':'+port)

    # Test out some log files
    file_list = [os.path.join('../data/log', child) for child in os.listdir('../data/log')]
    for filename in file_list:
        with open(filename,'rb') as file:

            # Skip OS generated files
            if '.DS_Store' in filename: continue

            md5 = c.store_sample(filename, file.read(), 'log')
            results = c.work_request('view_log_meta', md5)
            print 'Filename: %s\n' % (filename)
            pprint.pprint(results)
            stream_log = c.stream_sample(md5, 20)
            for row in stream_log:
                print row

def test():
    ''' log_meta_stream test '''
    main()

if __name__ == '__main__':
    main()

