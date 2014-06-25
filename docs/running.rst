Running WorkBench
=================

Configuration File Information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you first run workbench it copies default.ini to config.ini within
the workbench/server directory, you can make local changes to this file
without worrying about it getting overwritten on the next 'git pull'.
Also you can store API keys in it because it never gets pushed back to
the repository.

::

    # Example/default configuration for the workbench server
    [workbench]

    # Server URI (server machine ip or name)
    # Example: mybigserver or 12.34.56.789
    server_uri = localhost

    # DataStore URI (datastore machine ip or name)
    # Example: mybigserver or 12.34.56.789
    datastore_uri = localhost

    # Neo4j URI (Neo4j Graph DB machine ip or name)
    # Example: mybigserver or 12.34.56.789
    neo4j_uri = localhost

    # ElasticSearch URI (ELS machine ip or name)
    # Example: mybigserver or 12.34.56.789
    els_uri = localhost

    # DataStore Database
    # Example: customer123, ml_talk, pdf_deep
    database = workbench

    # Storage Limits (in MegaBytes, 0 for no limit)
    worker_cap = 10
    samples_cap = 200

    # VT API Key
    # Example: 93748163412341234v123947
    vt_apikey = 123

Workbench Examples
------------------

Please note that all of these notebooks are 'clients' hitting the
workbench server. Making your own client is super easy! See `Making a
Client <README_more.md###%20Making%20your%20own%20Client>`_

-  **PCAP to Graph** (A short teaser)
-  **Workbench Demo**
-  **Adding a new Worker** (super hawt)
-  **PCAP to Dataframe**
-  **PCAP DriveBy Analysis**
-  **Using Neo4j for PE File Sim Graph**
-  **Generator Pipelines Notebook**
-  WIP Notebooks

   -  **Network Stream Analysis Notebook**
   -  **PE File Static Analysis Notebook**

Making your own Worker
~~~~~~~~~~~~~~~~~~~~~~

Fill in info

Making your own Client
~~~~~~~~~~~~~~~~~~~~~~

Although the Workbench repository has dozens of clients (see
workbench/clients)there is NO official client to workbench. Clients are
examples of how YOU can just use ZeroRPC from the Python, Node.js, or
CLI interfaces. See `ZeroRPC <http://zerorpc.dotcloud.com/>`_.

::

    import zerorpc
    c = zerorpc.Client()
    c.connect("tcp://127.0.0.1:4242")
    with open('evil.pcap','rb') as f:
        md5 = c.store_sample('evil.pcap', f.read())
    print c.work_request('pcap_meta', md5)

**Output from above 'client':**
``python {'pcap_meta': {'encoding': 'binary',   'file_size': 54339570,   'file_type': 'tcpdump (little-endian) - version 2.4 (Ethernet, 65535)',   'filename': 'evil.pcap',   'import_time': '2014-02-08T22:15:50.282000Z',   'md5': 'bba97e16d7f92240196dc0caef9c457a',   'mime_type': 'application/vnd.tcpdump.pcap'}}``
### Running the IPython Notebooks \* brew install freetype \* brew
install gfortran \* pip install -r requirements\_notebooks.txt \* Go to
Starbucks..

Workbench Conventions
~~~~~~~~~~~~~~~~~~~~~

Workers should adhere to the following naming conventions (not enforced)

-  If you work on a specific type of sample than start the name with
   that
-  Examples: pcap\_bro.py, pe\_features.py, log\_meta.py
-  A worker that is new/experimental should start with 'x\_'
   (x\_pcap\_razor.py)
-  A 'view'(worker that handles 'presentation') should start with
   'view\_'
-  Examples: view\_log\_meta.py, view\_pdf.py, view\_pe.py

Test Coverage
~~~~~~~~~~~~~

If you want to run the test code coverage properly you'll need to create
a ~/.noserc file with these options:

::

    [nosetests]
    with-coverage=1
    cover-erase=1
    cover-inclusive=1
    cover-min-percentage=90
    cover-package=.

