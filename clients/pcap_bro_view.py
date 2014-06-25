''' This client pulls PCAP 'views' (view summarize what's in a sample) '''
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
    workbench = zerorpc.Client(timeout=300)
    workbench.connect('tcp://'+server+':'+port)

    # Test out getting the raw Bro logs from a PCAP file
    # Note: you can get a super nice 'generator' python list of dict by using
    #       'stream_sample' instead of 'get_sample'.
    file_list = [os.path.join('../data/pcap', child) for child in os.listdir('../data/pcap')]
    for filename in file_list:

        # Skip OS generated files
        if '.DS_Store' in filename: continue

        # Process the pcap file
        with open(filename,'rb') as file:
            md5 = workbench.store_sample(filename, file.read(), 'pcap')
            results = workbench.work_request('view_pcap', md5)
            print '\n<<< %s >>>' % filename
            pprint.pprint(results)

def test():
    ''' pcap_bro_view test '''
    main()

if __name__ == '__main__':
    main()

