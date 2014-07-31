Frequently Asked Questions
==========================


Scalable Python Framework
-------------------------

* What do you mean by 'scalable' framework?
    Workbench is a client/server architecture. The 'scalability' of the architecture is determined by the 
    put/get performance of the data storage backend (currently MongoDB). So the workbench framework is focused
    on bringing the work to the data. Meaning all the heavy lifting happens on the server side with worker
    streaming over the data no data is copied or moved, the only thing that happens is a sample is pulled from
    the data store ^once^ and than all of the workers in the current worker-chain operate on that sample. Afterward
    the sample is released from memory. 
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

* Okay I've changed my config.ini file, and now it shows up when I do a '$ git status'. How do I have git ignore it?::

    git update-index --assume-unchanged workbench/clients/config.ini
    git update-index --assume-unchanged workbench/server/config.ini
    
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
