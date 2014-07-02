"""This client pushes PCAPs -> MetaDaa -> ELS Indexer."""

import zerorpc
import os
import ConfigParser

def main():
    """This client pushes PCAPs -> MetaDaa -> ELS Indexer."""
    
    # Grab server info from configuration file
    workbench_conf = ConfigParser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.ini')
    workbench_conf.read(config_path)
    server = workbench_conf.get('workbench', 'server_uri') 
    port = workbench_conf.get('workbench', 'server_port')

    # Start up workbench connection
    workbench = zerorpc.Client()
    workbench.connect('tcp://'+server+':'+port)

    # Test out PCAP data
    data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'../data/pcap')
    file_list = [os.path.join(data_path, child) for child in os.listdir(data_path)]
    for filename in file_list:

        # Skip OS generated files
        if '.DS_Store' in filename: continue

        with open(filename,'rb') as pcap_file:
            md5 = workbench.store_sample(filename, pcap_file.read(), 'pcap')

            # Index the view_pcap output (notice we can ask for any worker output)
            # Also (super important) it all happens on the server side.
            workbench.index_worker_output('view_pcap', md5, 'view_pcap', None)
            print '\n\n<<< PCAP Data: %s Indexed>>>' % (filename)

def test():
    """Executes pcap_meta_indexer test."""
    main()

if __name__ == '__main__':
    main()

