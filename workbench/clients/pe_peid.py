"""This client looks for PEid signatures in PE Files."""

import zerorpc
import os
import pprint
import ConfigParser

def main():
    """This client looks for PEid signatures in PE Files."""
    
    # Grab server info from configuration file
    workbench_conf = ConfigParser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.ini')
    workbench_conf.read(config_path)
    server = workbench_conf.get('workbench', 'server_uri') 
    port = workbench_conf.get('workbench', 'server_port')

    # Start up workbench connection
    workbench = zerorpc.Client()
    workbench.connect('tcp://'+server+':'+port)

    # Test out PEFile -> peid
    data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'../data/pe/bad')
    file_list = [os.path.join(data_path, child) for child in os.listdir(data_path)][:10]
    data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'../data/pe/good')
    file_list += [os.path.join(data_path, child) for child in os.listdir(data_path)][:10]
    for filename in file_list:

        # Skip OS generated files
        if '.DS_Store' in filename: continue

        with open(filename,'rb') as f:
            md5 = workbench.store_sample(filename, f.read(), 'pe')
            results = workbench.work_request('pe_peid', md5)
            pprint.pprint(results)


def test():
    """Executes pe_peid test."""
    main()

if __name__ == '__main__':
    main()
