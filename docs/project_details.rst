Detailed Project Description
============================

Scalable Python Framework
-------------------------

* What do you mean by 'scalable' framework?
    Workbench is a client/server architecture. The 'scalability' of the architecture is determined by the
    put/get performance of the data storage backend (currently MongoDB). So the workbench framework is focused
    on bringing the work to the data. Meaning all the heavy lifting happens on the server side with workers
    *streaming over the data*. **Super Important:** No data is copied or moved, the only thing that happens is a
    sample is pulled from the data store **once** and than all of the workers in the current worker-chain
    operate on that sample. Afterward the sample is released from memory. 
* What do you mean by 'medium' data?
    Although Workbench can scale up with the datastore. During development and testing we're using it on 'medium'
    data. The developers of Workbench feel like Medium-Data is a sweet spot, large enough to be meaningful for model
    generation, statistics and predictive performance but small enough to allow for low latency, fast interaction
    and streaming 'hyperslabs' from server to client.
* What do you mean by hyperslabs?
    Many of our examples (notebooks) illustrate the streaming generator chains that allow a client (python script, IPython
    notebook, Node.js, CLI) to stream a filtered subset of the data over to the client.
* Why do you have exploding heads every time you talk about streaming data into a DataFrame?
    Once you efficiently (streaming with zero-copy) populate a Pandas dataframe you have access to a very large set of statistics, analysis,
    and machine learning Python modules (statsmodel, Pandas, Scikit-Learn).
* What kind of hardware do you recommend for the Workbench server?
    Workbench server will run great on a laptop but when you're working with a group of researchers the most 
    effective model is a shared group server. A beefy Dell server with 192Gig of Memory and a 100 TeraByte disk array
    will allow the workbench server to effectively process in the neighborhood of a million samples (PE Files, PDFs,
    PCAPs, SWF, etc.)

Client/Server
-------------

* Philosophy on local Workbench server.
    As you've noticed from many of the documents and notebooks,
    Workbench often defaults to using a local server. There are several
    reasons for this approach:
    
    * We love the concept of git, with a local server (sandbox) for quickness and agility and a remote server for when your ready to share your changes with the world.
    * Workbench embraces this approach: Developers can quickly develop new fuctionality on their local server and when they are ready to share the awesome they can 'push' their new worker to the 'group server'.

* How do I push my worker to a 'group server'?
    * development box: $ git push
    * server box: $ git pull

* How do I have my workbench clients hit a remote server?
    * All clients have a -s, --server argument::

        $ python pcap_bro_indexer.py   # Hit local server
        $ python pcap_bro_indexer.py -s = my_server  # Hit remote server
    
    * All clients read from the config.ini in the clients directory
        If you always hit a remote server simply change the config.ini in the clients directory 
        to point to the groupserver.::
    
            server_uri = localhost  (change this to whatever)
    
* How do I setup a development server and a production server?
    In general workbench should be treated like any other python module and it shouldn't add any complexity to existing development/QA/deployment models. One suggestion (to be taken with a grain of salt) is simply to use git braches.::
    
        $ git checkout develop (on develop server)
        $ git checkout master (on prod server)


Cow Points
----------

* Are Cow Points worth anything? : No
* Will Cow Points ever be worth anything? : Maybe
* Are Cow Points officially tracked? : Yes
* Will I receive good Karma for Cow Points? : Yes


Some more stuff about Workbench
-------------------------------
The workbench project takes the workbench metaphore seriously. It’s a
platform that allows you to do work; it provides a flat work surface
that supports your ability to combine tools (python modules) together.
In general a workbench never constrains you (oh no! you can’t use those
3 tools together!) on the flip side it doesn’t hold your hand either.
Using the workbench software is a bit like using a Lego set, you can put
the pieces together however you want AND adding your own pieces is super
easy!.

Loosely coupled
~~~~~~~~~~~~~~~

-  No inheritance relationships
-  No knowledge of data structures
-  Just take some input and barf some output (no format requirements)

Flat
~~~~
-  Workers (that’s it… everything is a worker)
-  Server dynamically loads workers from a directory called ‘workers’

Robust
~~~~~~
-  Worker fails to load (that’s fine)
-  Worker crashes (no sweat, that request fails but system chugs on)

Transparency
~~~~~~~~~~~~
-  All worker output is reflected in the data store (currently Mongo)
-  Use RoboMongo (see below) to inspect exactly what workers are
   outputting.

Small Granularity
~~~~~~~~~~~~~~~~~
-  The system works by passing references from one worker to another so
   there is NO benefit to large granularity workers.
-  It’s super easy to have a worker that aggregates information from a
   set of workers, the opposite (breaking apart a large code chunk into
   smaller units) is almost never easy.
-  Pull just what you want, workers and views (which are just workers)
   can be selectve about exactly which fields get pulled from which
   workers. 
