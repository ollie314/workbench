import zerorpc
import os
import argparse
import ConfigParser
import hashlib

# We're not using this but it might be handy to someone
'''
def md5_for_file(path, block_size=256*128):
    md5 = hashlib.md5()
    with open(path,'rb') as f:
        for chunk in iter(lambda: f.read(block_size), b''):
            md5.update(chunk)
    return md5.hexdigest()
'''

def main():
    
    # Grab server info from configuration file
    workbench_conf = ConfigParser.ConfigParser()
    workbench_conf.read('config.ini')
    server = workbench_conf.get('workbench', 'server_uri') 
    port = workbench_conf.getint('workbench', 'server_port') 

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--data-dir', type=str, default='../data/pdf/bad', help='Directory of files to import into the workbench server')
    parser.add_argument('-t', '--tag', type=str, default='log', help='Type_tag of the files being imported')    
    parser.add_argument('-p', '--port', type=int, default=port, help='port used by workbench server')
    parser.add_argument('-s', '--server', type=str, default=server, help='location of workbench server')
    args = parser.parse_args()
    port = str(args.port)
    server = str(args.server)

    # Start up workbench connection
    workbench = zerorpc.Client()
    workbench.connect('tcp://'+server+':'+port)
    
    # Grab all the filenames from the data directory
    data_dir = args.data_dir
    file_list = [os.path.join(data_dir, child) for child in os.listdir(data_dir)]

    # Upload the files into workbench
    for path in file_list:
        with open(path,'rb') as f:
            filename = os.path.basename(path)

            # Here we're going to save network traffic by asking
            # Workbench if it already has this md5
            raw_bytes = f.read()
            md5 = hashlib.md5(raw_bytes).hexdigest()
            if workbench.has_sample(md5):
                print 'Workbench already has this sample %s' % md5
            else:
                # Store the sample into workbench
                md5 = workbench.store_sample(filename, raw_bytes, args.tag)
                print 'Filename %s uploaded: type_tag %s, md5 %s' % (filename, args.tag, md5)

def test():
    ''' file_upload test '''
    main()

if __name__ == '__main__':
    main()

