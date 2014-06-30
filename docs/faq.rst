==============================
FAQ: Frequency Asked Questions
==============================

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
