Installing Workbench
====================


Workbench Command Line Interface (CLI)
--------------------------------------

::

    $ pip install workbench_cli
    $ workbench (this runs the Workbench CLI)

That's it! 

If you have a workbench server setup (somewhere) you can start using the workbench CLI client,
or any of the existing clients (in workbench/clients) or even start writing your own clients
against that server (see :ref:`MakingClient`)

Workbench CLI (on Windozes)
---------------------------

- Visual Studio Express 2008: (yes 2008 python 2.7 requires those libs)
    - http://go.microsoft.com/?linkid=7729279
- Python: https://www.python.org/download/releases/2.7.8/
- Pip: http://pip.readthedocs.org/en/latest/installing.html
- Install Greenlet: http://www.lfd.uci.edu/~gohlke/pythonlibs/#greenlet
- Install Gevent: http://www.lfd.uci.edu/~gohlke/pythonlibs/#gevent
- pip install workbench_cli

::

    > cd c:\python27\lib\site-packages\workbench_cli
    > python workbench   (use -s to specify alternative server if you want)

This should spin up the workbench CLI interface, the colors will be messed up (we’re working on that)


Workbench Server (Minimum Install)
----------------------------------
The workbench server is extremely robust to worker failure. In fact it can run without many of the dependencies
so you can setup a server quickly with 'Minimum Install' and than later do a 'Full Install'.

Mac/OSX
~~~~~~~

::

    $ brew install mongodb

Ubuntu (14.04 and 12.04)
~~~~~~~~~~~~~~~~~~~~~~~~

::

    $ sudo apt-get install mongodb
    $ sudo apt-get install python-dev
    $ sudo apt-get install g++

Workbench Python Modules
~~~~~~~~~~~~~~~~~~~~~~~~

::

    $ pip install workbench --pre
    $ workbench_server

That's it, the workbench server will come up and is ready to start servicing requests.
Note: Some workers will fail to load but that is fine, to have all workers run see 'Full Install'.


Workbench Server (Full Install)
-------------------------------

Mac/OSX
~~~~~~~

    ::
    
        $ brew install mongodb
        $ brew install yara
        $ brew install libmagic
        $ brew install bro
    
    .. important:: Put the bro executable in your PATH (/usr/local/bin or wherever bro is)

Ubuntu (14.04 and 12.04)
~~~~~~~~~~~~~~~~~~~~~~~~

    ::
    
        $ sudo apt-get install mongodb
        $ sudo apt-get install python-dev
        $ sudo apt-get install g++
        $ sudo apt-get install libssl0.9.8
    
    - Bro IDS: In general the Bro debian package files are WAY too locked down with dependencies on exact versions of libc6 and python2.6. We have a more 'flexible' version `Bro-2.2-Linux-x86\_64\_flex.deb <https://s3-us-west-2.amazonaws.com/workbench-data/packages/Bro-2.2-Linux-x86_64_flex.deb>`_.
        - sudo dpkg -i Bro-2.2-Linux-x86\_64\_flex.deb
        - If using the Debian package above doesn't work out: 
            - Check out the Installation tutorial `bro_install <https://www.digitalocean.com/community/tutorials/how-to-install-bro-ids-2-2-on-ubuntu-12-04>`_
            - or this one `bro_starting <http://www.justbeck.com/getting-started-with-bro-ids/>`_ 
            - or go to offical Bro Downloads `www.bro.org/download/ <http://www.bro.org/download>`_
    
    .. important:: Put the bro executable in your PATH (/opt/bro/bin or wherever bro is)

Install Indexers
~~~~~~~~~~~~~~~~
The indexers 'Neo4j' and 'ElasticSearch' are optional. We strongly
suggest you install both of them but we also appreciate that there are
cases where that's not possible or feasible.

Mac/OSX
^^^^^^^

    ::
    
        $ brew install elasticsearch
        $ pip install -U elasticsearch
        $ brew install neo4j
    
    -  Note: You may need to install Java JDK 1.7 `Oracle JDK 1.7 DMG <http://download.oracle.com/otn-pub/java/jdk/7u51-b13/jdk-7u51-macosx-x64.dmg>`_ for macs.

Ubuntu (14.04 and 12.04)
^^^^^^^^^^^^^^^^^^^^^^^^

    -  Neo4j: See official instructions for Neo4j `here <http://www.neo4j.org/download/linux>`_

    -  Note: You may need to install Java JDK 1.7. If you have Java 1.7 installed and error says otherwise, run 
    
    ::
    
        $ update-alternatives --config java and select Java 1.7

    -  ElasticSearch:

        -  wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.2.1.deb
        -  sudo dpkg -i elasticsearch-1.2.1.deb
        -  sudo update-rc.d elasticsearch defaults 95 10
        -  sudo /etc/init.d/elasticsearch start
        -  Any issues see `elasticsearch\_webpage <http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/setup-service.html>`_



Workbench Python Modules
~~~~~~~~~~~~~~~~~~~~~~~~

    Note: Workbench is continuously tested with python 2.7. We're currently
    working on Python 3 support (`Issue 92 <https://github.com/SuperCowPowers/workbench/issues/92>`_).
    
    For quick spinup just pull Workbench down from pip. If you're going to do development
    
    ::
    
        $ pip install workbench --pre
        $ workbench_server
    
    **OR**
    
    ::
    
        $ cd workbench
        $ python setup.py develop
        $ workbench_server

Optional Tools
~~~~~~~~~~~~~~

    **Robomongo**
    
    Robomongo is a shell-centric cross-platform MongoDB management tool.
    Simply, it is a handy GUI to inspect your mongodb.
    
    -  http://robomongo.org/
    -  download and follow install instructions
    -  create a new connection to localhost (default settings fine). Name it as you wish.

Dependency Installation Errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Python Modules**
    
    Note: If you get a bunch of clang errors about unknown arguments or
    'cannot link a simple C program' add the following FLAGs:
    
    ::
    
        $ export CFLAGS=-Qunused-arguments
        $ export CPPFLAGS=-Qunused-arguments
    
        **Errors when running Tests**
    
    If when running the worker tests you get some errors like 'MagicError:
    regexec error 17, (illegal byte sequence)' it's an issue with libmagic
    5.17, revert to libmagic 5.16. Using brew on Mac:
    
    ::
    
        $ cd /usr/local
        $ brew versions libmagic # Copy the line for version 5.16, then paste (for me it looked like the following line)
        $ git checkout bfb6589 Library/Formula/libmagic.rb
        $ brew uninstall libmagic
        $ brew install libmagic
