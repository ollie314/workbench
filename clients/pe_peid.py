import zerorpc
import argparse
import os
import pprint
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

    # Test out PEFile -> peid
    file_list = [os.path.join('../data/pe/bad', child) for child in os.listdir('../data/pe/bad')]
    file_list += [os.path.join('../data/pe/good', child) for child in os.listdir('../data/pe/good')]
    for filename in file_list:

        # Skip OS generated files
        if '.DS_Store' in filename: continue

        with open(filename,'rb') as file:
            md5 = c.store_sample(filename, file.read(), 'pe')
            results = c.work_request('pe_peid', md5)
            pprint.pprint(results)


def test():
    ''' pe_peid test '''
    main()

if __name__ == '__main__':
    main()
