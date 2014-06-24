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
    parser.add_argument('-f', '--loadfile', type=str, default='../data/log/system.log', help='File to import into the workbench server')
    parser.add_argument('-p', '--port', type=int, default=port, help='port used by workbench server')
    parser.add_argument('-s', '--server', type=str, default=server, help='location of workbench server')
    args = parser.parse_args()
    port = str(args.port)
    server = str(args.server)

    # Start up workbench connection
    workbench = zerorpc.Client()
    workbench.connect('tcp://'+server+':'+port)

    # Upload the files into workbench
    my_file = args.loadfile
    with open(my_file,'rb') as f:

        # Check to see if workbench already has the file
        filename = os.path.basename(my_file)
        raw_bytes = f.read()
        md5 = workbench.store_sample(filename, raw_bytes, 'log')
        results = workbench.work_request('view', md5)
        print 'Filename: %s' % filename
        pprint.pprint(results)

    # You can also download a sample (commented out)
    '''
    sample = workbench.get_sample(md5)
    raw_bytes = sample['sample']['raw_bytes']
    with open('mysample.log','wb') as f:
        f.write(raw_bytes)
    '''

def test():
    ''' file_upload test '''
    main()

if __name__ == '__main__':
    main()

