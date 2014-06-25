''' This client pushes PCAPs -> Bro -> ELS Indexer '''
import zerorpc
import os
import argparse
import ConfigParser


def main():
    ''' This client pushes PCAPs -> Bro -> ELS Indexer '''

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

    # Test out getting the raw Bro logs from a PCAP file and sending results to an ELS indexer
    file_list = [os.path.join('../data/pcap', child) for child in os.listdir('../data/pcap')]
    for filename in file_list:

        # Skip OS generated files
        if '.DS_Store' in filename: 
            continue

        with open(filename, 'rb') as pcap_file:
            md5 = workbench.store_sample(filename, pcap_file.read(), 'pcap')

            # Index the view_pcap output (notice we can ask for any worker output)
            # Also (super important) it all happens on the server side.
            workbench.index_worker_output('view_pcap', md5, 'pcap_bro', None)
            print '\n\n<<< PCAP Bro log Data: %s Indexed>>>' % (filename)


def test():
    ''' pcap_bro_indexer test '''
    main()

if __name__ == '__main__':
    main()

