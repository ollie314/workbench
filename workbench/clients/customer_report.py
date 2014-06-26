''' This client generates customer reports on all the samples in workbench '''
import zerorpc
import pprint
import argparse
import ConfigParser

def main():
    ''' This client generates customer reports on all the samples in workbench '''
    
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

    results = workbench.batch_work_request('view_customer', {})
    pprint.pprint(list(results))

def test():
    ''' customer_report test '''
    main()

if __name__ == '__main__':
    main()

