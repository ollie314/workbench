''' This client gets extracts URLs from PCAP files (via Bro logs) '''
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

    # Loop through all the pcaps and collect a set of urls(hosts) from the http_log files
    urls = set()
    file_list = [os.path.join('../data/pcap', child) for child in os.listdir('../data/pcap')]
    for filename in file_list:

        # Skip OS generated files
        if '.DS_Store' in filename: continue

        with open(filename,'rb') as file:
            pcap_md5 = workbench.store_sample(filename, file.read(), 'pcap')
            results = workbench.work_request('pcap_bro', pcap_md5)

            # Just grab the http log
            if 'http_log' in results['pcap_bro']:
                log_md5 = results['pcap_bro']['http_log']
                http_data = workbench.stream_sample(log_md5, None)  # None Means all data
                urls = set( row['host'] for row in http_data)
                print '<<< %s >>>' % filename
                pprint.pprint(list(urls))
                print


def test():
    ''' pcap_bro_urls test '''
    main()

if __name__ == '__main__':
    main()

