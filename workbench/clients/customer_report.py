"""This client generates customer reports on all the samples in workbench."""

import zerorpc
import pprint
import os
import ConfigParser

def main():
    """This client generates customer reports on all the samples in workbench."""
    
    # Grab server info from configuration file
    workbench_conf = ConfigParser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.ini')
    workbench_conf.read(config_path)
    server = workbench_conf.get('workbench', 'server_uri') 
    port = workbench_conf.get('workbench', 'server_port')

    # Start up workbench connection
    workbench = zerorpc.Client()
    workbench.connect('tcp://'+server+':'+port)

    results = workbench.batch_work_request('view_customer', {})
    pprint.pprint(list(results))

def test():
    """Executes test for customer_report."""
    main()

if __name__ == '__main__':
    main()

