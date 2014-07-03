Running WorkBench
=================

Server (localhost or server machine)
------------------------------------

::

   $ python setup.py install
   $ workbench

Example Clients (use -s for remote server)
------------------------------------------

There are about a dozen example clients showing how to use workbench on
pcaps, PEfiles, pdfs, and log files. We even have a simple nodes.js
client (looking for node devs to pop some pull requests :).

::

   $ cd workbench/clients
   $ python simple_workbench_client.py [-s tcp://mega.server.com]

Workbench Examples
------------------

-  `PCAP to Graph <http://nbviewer.ipython.org/url/raw.github.com/SuperCowPowers/workbench/master/notebooks/PCAP_to_Graph.ipynb/>`_ (A short teaser)
-  `Workbench Demo <http://nbviewer.ipython.org/url/raw.github.com/SuperCowPowers/workbench/master/notebooks/Workbench_Demo.ipynb/>`_
-  `Adding a new Worker <http://nbviewer.ipython.org/url/raw.github.com/SuperCowPowers/workbench/master/notebooks/Adding_Worker.ipynb/>`_ (super hawt)
-  `PCAP to Dataframe <http://nbviewer.ipython.org/url/raw.github.com/SuperCowPowers/workbench/master/notebooks/PCAP_to_Dataframe.ipynb/>`_
-  `PCAP DriveBy Analysis <http://nbviewer.ipython.org/url/raw.github.com/SuperCowPowers/workbench/master/notebooks/PCAP_DriveBy.ipynb>`_
-  `Using Neo4j for PE File Sim Graph <http://nbviewer.ipython.org/url/raw.github.com/SuperCowPowers/workbench/master/notebooks/PE_SimGraph.ipynb>`_
-  `Generator Pipelines Notebook <http://nbviewer.ipython.org/url/raw.github.com/SuperCowPowers/workbench/master/notebooks/Generator_Pipelines.ipynb>`_
-  WIP Notebooks

   -  `Network Stream Analysis Notebook <http://nbviewer.ipython.org/url/raw.github.com/SuperCowPowers/workbench/master/notebooks/Network_Stream.ipynb>`_
   -  `PE File Static Analysis Notebook <http://nbviewer.ipython.org/url/raw.github.com/SuperCowPowers/workbench/master/notebooks/PE_Static_Analysis.ipynb>`_


Making your own Worker
----------------------

Fill in info

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


.. _MakingClient:

Making your own Client
----------------------

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

Output from above 'client':

.. code-block:: python

    {'pcap_meta': {
        'encoding': 'binary',
        'file_size': 54339570,
        'file_type': 'tcpdump (little-endian) - version 2.4 (Ethernet, 65535)',
        'filename': 'evil.pcap',
        'import_time': '2014-02-08T22:15:50.282000Z',
        'md5': 'bba97e16d7f92240196dc0caef9c457a',
        'mime_type': 'application/vnd.tcpdump.pcap'
    }}``

Running the IPython Notebooks
-----------------------------

::

    brew install freetype
    brew install gfortran
    pip install -r requirements\_notebooks.txt
    Go to Starbucks..


Running Tests
-------------

Unit testing, sub-pipeline tests, and full pipeline tests

::

   $ tox

Benign Error
~~~~~~~~~~~~

We have no idea why occasionaly you see this pop up in the server
output. To our knowledge it literally has no impact on any functionality
or robustness. If you know anything about this please help us out by
opening an issue and pull request. :)

::

   ERROR:zerorpc.channel:zerorpc.ChannelMultiplexer, unable to route event:
   _zpc_more {'response_to': '67d7df3f-1f3e-45f4-b2e6-352260fa1507', 'zmqid':
   ['\x00\x82*\x01\xea'], 'message_id': '67d7df42-1f3e-45f4-b2e6-352260fa1507',
   'v': 3} [...]

VirusTotal Warning
~~~~~~~~~~~~~~~~~~

The vt\_query.py worker uses a shared 'low-volume' API key provided by
SuperCowPowers LLC. When running the vt\_query worker the following
warning happens quite often:

::

    "VirusTotal Query Error, no valid response... past per min quota?"

If you'd like to use the vt\_query worker on a regular basis, you'll
have to put your own VirusTotal API key in the
workbench/server/config.ini file.

Configuration File Information
------------------------------

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
