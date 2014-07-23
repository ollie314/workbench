"""This client pulls PCAP 'views' (view summarize what's in a sample)."""

import zerorpc
import os
import pprint
import workbench_client
import flask

app = flask.Flask(__name__)

@app.route('/')
def run():
    """This client pulls PCAP 'views' (view summarize what's in a sample)."""
    
    # Grab server args
    args = workbench_client.grab_server_args()

    # Start up workbench connection
    workbench = zerorpc.Client(timeout=300, heartbeat=60)
    workbench.connect('tcp://'+args['server']+':'+args['port'])

    data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'../data/pcap')
    file_list = [os.path.join(data_path, child) for child in os.listdir(data_path)]
    for filename in file_list:

        # Skip OS generated files
        if '.DS_Store' in filename: continue

        # Process the pcap file
        with open(filename,'rb') as f:
            md5 = workbench.store_sample(filename, f.read(), 'pcap')
            results = workbench.work_request('view_pcap', md5)
    return flask.render_template('../data/templates/index.html', results=results)            

def test():
    ''' pcap_bro_view test '''
    run()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

