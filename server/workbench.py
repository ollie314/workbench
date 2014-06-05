
''' Workbench: Open Source Security Framework '''

from gevent import monkey; monkey.patch_all(thread=False) # Monkey!
import os
import argparse
import shutil
import configparser
import zerorpc
import zmq
import logging
logging.basicConfig()
import datetime
import StringIO
import json
import hashlib
import inspect
import urllib3

''' Add bro to path for bro_log_reader '''
import sys
sys.path.extend(['workers','workers/bro'])

# Local modules
try:
    from . import data_store
    from . import els_indexer
    from . import neo_db
    from . import plugin_manager
    from . import bro_log_reader
    from . import workbench_keys
except ValueError:
    import data_store
    import els_indexer
    import neo_db
    import plugin_manager
    import bro_log_reader
    import workbench_keys


class WorkBench():
    ''' Workbench: Open Source Security Framework '''
    def __init__(self, store_args=None, els_hosts=None, neo_uri=None):

        # Open DataStore
        self.data_store = data_store.DataStore(**store_args)

        # ELS Indexer
        try:
            self.indexer = els_indexer.ELS_Indexer(**{'hosts': els_hosts} if els_hosts else {})
        except SystemExit:
            print 'Could not connect to ELS. Is it running?'
            self.indexer = els_indexer.ELS_StubIndexer(**{'uri': neo_uri} if neo_uri else {})

        # Neo4j DB
        try:
            self.neo_db = neo_db.NeoDB(**{'uri': neo_uri} if neo_uri else {})
        except RuntimeError:
            print 'Could not connect to Neo4j DB. Is it running?  $ neo4j start'
            self.neo_db = neo_db.NeoDBStub(**{'uri': neo_uri} if neo_uri else {})

        # Create Plugin Grabber
        self.plugin_meta = {}
        plugin_manager.PluginManager(self._new_plugin)

    # Data storage methods
    def store_sample(self, filename, input_bytes, type_tag):
        ''' Store a sample into the DataStore.
            Args:
                filename: name of the file (used purely as meta data not for lookup)
                input_bytes: the actual bytes of the sample e.g. f.read()
                type_tag: ('pe','pcap','pdf','json','swf', or ...)
            Returns:
                the md5 of the sample
        '''
        return self.data_store.store_sample(filename, input_bytes, type_tag)

    def get_sample(self, md5):
        ''' Get a sample from the DataStore.
            Args:
                md5: the md5 of the sample
            Returns:
                A dictionary of meta data about the sample which includes
                a ['raw_bytes'] key that contains the raw bytes.
        '''
        sample = self.data_store.get_sample(md5)
        return {'sample': sample}

    def get_sample_window(self, type_tag, size):
        ''' Get a sample from the DataStore.
            Args:
                type_tag: the type of samples ('pcap','pe','pdf')
                size: the size of the window in MegaBytes (10 = 10MB)
            Returns:
                A list of md5s representing the newest samples within the size window
        '''
        return self.data_store.get_sample_window(type_tag, size)

    def have_sample(self, md5):
        ''' Do we have this sample in the DataStore.
            Args:
                md5: the md5 of the sample
            Returns:
                True or False
        '''
        return self.data_store.have_sample(md5)

    @zerorpc.stream
    def stream_sample(self, md5, max_rows):
        ''' Stream the sample by giving back a generator '''

        # Grab the sample and it's raw bytes
        sample = self.data_store.get_sample(md5)
        raw_bytes = sample['raw_bytes']

        # Figure out the type of file to be streamed
        type_tag = sample['type_tag']
        if type_tag == 'bro':
            bro_log = bro_log_reader.BroLogReader(convert_datetimes=False)
            mem_file = StringIO.StringIO(raw_bytes)
            generator = bro_log.read_log(mem_file, max_rows=max_rows)
            return generator
        elif type_tag == 'els_query':
            els_log = json.loads(raw_bytes)
            # Try to determine a couple of different types of ELS query results
            if 'fields' in els_log['hits']['hits'][0]:
                generator = (row['fields'] for row in els_log['hits']['hits'][:max_rows])
            else:
                generator = (row['_source'] for row in els_log['hits']['hits'][:max_rows])
            return generator
        elif type_tag == 'log':
            generator = ({'row':row} for row in raw_bytes.split('\n')[:max_rows])
            return generator
        elif type_tag == 'json':
            generator = (row for row in json.loads(raw_bytes)[:max_rows])
            return generator
        else:
            raise Exception('Cannot stream file %s with type_tag:%s' % (md5, type_tag))

    # Index methods
    def index_sample(self, md5, index_name):
        ''' Index a stored sample with the Indexer '''
        generator = self.stream_sample(md5, None)
        for row in generator:
            self.indexer.index_data(row, index_name)

    def index_worker_output(self, worker_class, md5, index_name):
        ''' Index worker output with Indexer'''

        # Grab the data
        data = self.work_request(worker_class, md5)[worker_class]

        # Okay now index the data
        self.indexer.index_data(data, index_name=index_name, doc_type='unknown')

    def search(self, index_name, query):
        ''' Search an index'''
        return self.indexer.search(index_name, query)

    # Graph methods
    def add_node(self, md5, name, labels):
        ''' Add the node with name and labels '''
        self.neo_db.add_node(md5, name, labels)

    def has_node(self, md5):
        ''' Does the DB have this node '''
        return self.neo_db.has_node(md5)

    def add_rel(self, source_md5, target_md5, rel):
        ''' Add a relationship: source, target must already exist (see add_node)
            'rel' is the name of the relationship 'contains' or whatever. '''
        self.neo_db.add_rel(source_md5, target_md5, rel)

    def clear_graph_db(self):
        ''' Clear the Graph Database of all nodes and edges '''
        self.neo_db.clear_db()

    def clear_db(self):
        ''' Clear the database of all samples and worker output '''
        self.data_store.clear_db()

    # Make a work request for an existing stored sample
    def work_request(self, worker_class, md5, subkeys=None):
        ''' Make a work request for an existing stored sample '''

        # Check valid
        if worker_class not in self.plugin_meta.keys():
            raise RuntimeError('Invalid work request for class %s (not found)' % (worker_class))

        # Get results (even if we have to wait for them)
        # Note: Yes, we're going to wait. Gevent concurrent execution will mean this
        #       code gets spawned off and new requests can be handled without issue.
        work_results = self._recursive_work_resolver(worker_class, md5)

        # Subkeys? (Fixme this is super klutzy)
        if subkeys:
            try:
                sub_results = {}
                for subkey in subkeys:
                    tmp = work_results[worker_class]
                    for key in subkey.split('.'):
                        tmp = tmp[key]
                    sub_results[key] = tmp
                work_results = sub_results
            except KeyError:
                raise KeyError('Could not get one or more subkeys for: %s' % (work_results))

        # Clean it and ship it
        work_results = self.data_store.clean_for_serialization(work_results)
        return work_results

    @zerorpc.stream
    def batch_work_request(self, worker_class, kwargs):
        ''' Make a batch work request for an existing set of stored samples.
            A subset of sample can be specified either with type_tag (e.g. type_tag='pe')
            or the md5_list arg can be set to a list of md5s if neither of these are
            set then all of the samples will receive this work request. 
            Note: This method returns a generator. '''
        type_tag = kwargs.get('type_tag',None)
        md5_list = kwargs.get('md5_list',None)
        subkeys = kwargs.get('subkeys',None)

        # If no md5_list specified put all samples (of type type_tag if not None)
        if not md5_list:
            md5_list = self.data_store.all_sample_md5s(type_tag) 

        # Loop through all the md5s and return a generator with yield
        for md5 in md5_list:
            try:
                if subkeys:
                    yield self.work_request(worker_class, md5, subkeys)
                else:
                    yield self.work_request(worker_class, md5)[worker_class]
            except KeyError:
                continue

    def store_sample_set(self, md5_list):
        ''' Store a sample set (which is just a list of md5s).
            Note: All md5s must already be in the data store. '''
        for md5 in md5_list:
            if not self.have_sample(md5):
                raise RuntimeError('Sample not found all items in sample_set must be in the datastore: %s (not found)' % (md5))
        set_md5 = hashlib.md5(str(md5_list)).hexdigest()
        self._store_work_results({'md5_list':md5_list}, 'sample_set', set_md5)
        return set_md5

    def get_sample_set(self, md5):
        return self._get_work_results('sample_set', md5)

    @zerorpc.stream
    def stream_sample_set(self, md5):
        for md5 in self._get_work_results('sample_set', md5)['md5_list']:
            yield md5

    def get_datastore_uri(self):
        ''' Gives you the current datastore URL '''
        return self.data_store.get_uri()

    def _new_plugin(self, plugin, mod_time):
        ''' The method handles the mechanics around new plugins. '''
        print '< %s: loaded >' % (plugin['name'])
        plugin['time_stamp'] = mod_time # datetime.datetime.utcnow()
        self.plugin_meta[plugin['name']] = plugin

    def _store_work_results(self, results, collection, md5):
        self.data_store.store_work_results(results, collection, md5)
    def _get_work_results(self, collection, md5):
        results = self.data_store.get_work_results(collection, md5)
        return {collection: results} if results else None


    # So the trick here is that since each worker just stores it's input dependencies
    # we can resursively backtrack and all the needed work gets done.
    def _recursive_work_resolver(self, worker_class, md5):

        # Looking for the sample or sample_set?
        if (worker_class == 'sample'):
            try:
                return self.get_sample(md5)
            except RuntimeError:
                return self.get_sample_set(md5)

        # Do I actually have this plugin? (might have failed, etc)
        if (worker_class not in self.plugin_meta):
            print 'Request for non-existing or failed plugin: %s' % (worker_class)
            return {}

        # If the results exist and the time_stamp is newer than the plugin's, I'm done
        collection = self.plugin_meta[worker_class]['name']
        work_results = self._get_work_results(collection, md5)
        if work_results:
            if self.plugin_meta[worker_class]['time_stamp'] < work_results[collection]['__time_stamp']:
                print 'Returning cached work results for plugin: %s' % (worker_class)
                return work_results
            else:
                print 'Updating work results for new plugin: %s' % (worker_class)

        dependencies = self.plugin_meta[worker_class]['dependencies']
        dependant_results = {}
        for dependency in dependencies:
            dependant_results.update(self._recursive_work_resolver(dependency, md5))
        print 'New work for plugin: %s' % (worker_class)
        work_results = self.plugin_meta[worker_class]['class']().execute(dependant_results)

        # Store the results and return
        self._store_work_results(work_results, collection, md5)
        return self._get_work_results(collection, md5)

    def _find_element(self,d,k):
        if k in d: return d[k]
        submatch = [d[_k][k] for _k in d if k in d[_k]]
        return submatch[0] if submatch else None

    def help(self):
        ''' Returns help commands '''

        help_str =  '\nWelcome to Workbench: Here\'s a list of help commands:'
        help_str += '\n\t - Run c.help_basic() for beginner help'
        help_str += '\n\t - Run c.help_commands() for command help'
        help_str += '\n\t - Run c.help_workers() for a list of workers'
        help_str += '\n\t - Run c.help_advanced() for advanced help'
        help_str += '\n\nSee https://github.com/SuperCowPowers/workbench for more information'
        return help_str

    def help_basic(self):
        ''' Returns basic help commands '''
        help_str =  '\nWorkbench: Getting started...'
        help_str += '\n\t - 1) $ c.help_commands() for a list of commands'
        help_str += '\n\t - 2) $ print c.help_commands()[\'store_sample\']'
        help_str += '\n\t - 3) $ c.help_workers() for a list a workers'
        help_str += '\n\t - 4) $ print c.help_commands()[\'meta\']'
        help_str += '\n\t - 5) $ my_md5 = c.store_sample(...)'
        help_str += '\n\t - 6) $ output = c.work_request(\'meta\', my_md5)'
        return help_str

    def help_commands(self):
        ''' Returns Workbench commands and docstrings '''
        return {name:meth.__doc__ for name, meth in inspect.getmembers(self, predicate=inspect.ismethod) if not name.startswith('_')}

    def help_workers(self):
            ''' List the current worker plugins '''
            return {plugin['name']:plugin['class'].__doc__ for name, plugin in self.plugin_meta.iteritems()}

    def help_advanced(self):
        help_str =  '\nWoo! Advanced... <fixme: add documentation for advanced> :)'
        help_str += '\n\nSee https://github.com/SuperCowPowers/workbench for more information'
        return help_str


def main():

    # Load the configuration file (might not exist, so copy the default over)
    if not os.path.exists('config.ini'):
        shutil.copyfile('default.ini', 'config.ini')
    config = configparser.ConfigParser()
    config.read('config.ini')

    workbench_conf = config['workbench']

    # Pull configuration settings (or set defaults if don't exist)
    server_uri = workbench_conf.get('server_uri', 'localhost')
    datastore_uri = workbench_conf.get('datastore_uri', 'localhost')
    database = workbench_conf.get('database', 'workbench')
    worker_cap = int(workbench_conf.get('worker_cap', 10))
    samples_cap = int(workbench_conf.get('samples_cap', 100))

    # API keys just get tossed into API_KEYS dict
    workbench_keys.API_KEYS['vt_apikey'] = workbench_conf.get('vt_apikey', '123')

    # Parse the arguments (args overwrite configuration file settings)
    parser = argparse.ArgumentParser()
    parser.add_argument('-ds_uri', '--datastore_uri', type=str, default=None, help='machine used by workbench datastore')
    parser.add_argument('-db', '--database', type=str, default=None, help='database used by workbench server')
    args = parser.parse_args()

    # Overwrite if specified
    datastore_uri = args.datastore_uri if (args.datastore_uri) else datastore_uri
    database = args.database if (args.database) else database

    # Spin up Workbench ZeroRPC
    try:
        store_args = {'uri': datastore_uri, 'database': database, 'worker_cap':worker_cap, 'samples_cap':samples_cap}
        s = zerorpc.Server(WorkBench(store_args=store_args), name='workbench')
        s.bind('tcp://0.0.0.0:4242')
        s.run()
        print 'ZeroRPC %s' % ('tcp://0.0.0.0:4242')
    except zmq.error.ZMQError:
        print '\nInfo: Could not start ZMQ server (no worries, probably already running...)\n'
    except KeyboardInterrupt:
        print '\nWorbench Server Exiting...'
        exit()

# Test that just calls main
def test():
    main()

if __name__ == '__main__':
    main()
