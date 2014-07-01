''' This client pulls PCAP 'views' (view summarize what's in a sample) '''
import zerorpc
import os
import pprint
import ConfigParser

def main():
    ''' This client pulls PCAP 'views' (view summarize what's in a sample) '''
    
    # Grab server info from configuration file
    workbench_conf = ConfigParser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.ini')
    workbench_conf.read(config_path)
    server = workbench_conf.get('workbench', 'server_uri') 
    port = workbench_conf.get('workbench', 'server_port')

    # Start up workbench connection
    workbench = zerorpc.Client(timeout=300)
    workbench.connect('tcp://'+server+':'+port)

    # Test out getting the raw Bro logs from a PCAP file
    # Note: you can get a super nice 'generator' python list of dict by using
    #       'stream_sample' instead of 'get_sample'.
    data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'../data/pcap')
    file_list = [os.path.join(data_path, child) for child in os.listdir(data_path)]
    for filename in file_list:

        # Skip OS generated files
        if '.DS_Store' in filename: continue

        # Process the pcap file
        with open(filename,'rb') as f:
            md5 = workbench.store_sample(filename, f.read(), 'pcap')
            results = workbench.work_request('view_pcap', md5)
            print '\n<<< %s >>>' % filename
            pprint.pprint(results)

def test():
    ''' pcap_bro_view test '''
    main()

if __name__ == '__main__':
    main()

