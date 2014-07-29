"""This client pushes a file into Workbench."""

import zerorpc
import os
import pprint
import client_helper
import hashlib

def chunks(data, chunk_size):
    """ Yield chunk_size chunks from data."""
    for i in xrange(0, len(data), chunk_size):
        yield data[i:i+chunk_size] 

def run():
    """This client pushes a file into Workbench."""
    
    # Grab server args
    args = client_helper.grab_server_args()

    # Start up workbench connection
    workbench = zerorpc.Client(timeout=300, heartbeat=60)
    workbench.connect('tcp://'+args['server']+':'+args['port'])

    # Upload the files into workbench
    my_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                           '../data/pcap/gold_xxx.pcap')
    with open(my_file,'rb') as f:

        # We're going to upload the file in chunks to workbench 
        filename = os.path.basename(my_file)
        raw_bytes = f.read()        
        md5 = hashlib.md5(raw_bytes).hexdigest()
        for chunk in chunks(raw_bytes, 1024*1024):
            workbench.store_sample_chunk(filename, chunk, 'exe', md5)

def test():
    """Executes file_upload test."""
    run()

if __name__ == '__main__':
    run()

