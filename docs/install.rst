## Installing Workbench:

### Workbench Client:
    $ pip install zerorpc; echo 'Done!'

### Workbench Server:
The indexers 'Neo4j' and 'ElasticSearch' are optional. We strongly suggest you install both of them but we also appreciate that there are cases where that's not possible or feasible.

#### Mac/OSX
- brew install mongodb
- brew install yara
- brew install libmagic
- brew install bro
   - Put the bro executable in your PATH (/usr/local/bin or wherever bro is)

#### Ubuntu (14.04 and 12.04)
- sudo apt-get install mongodb
- sudo apt-get install python-dev
- sudo apt-get install g++
- sudo apt-get install libssl0.9.8
- Bro IDS: 
   - Put the bro executable in your PATH (/opt/bro/bin or wherever bro is)

    In general the Bro debian package files are WAY too locked down with dependencies on exact versions of libc6 and python2.6. We have a more 'flexible' version [Bro-2.2-Linux-x86_64_flex.deb](https://s3-us-west-2.amazonaws.com/workbench-data/packages/Bro-2.2-Linux-x86_64_flex.deb). 
    - sudo dpkg -i Bro-2.2-Linux-x86_64_flex.deb
 
   If using the Debian package above doesn't work out:
   - Check out the Installation tutorial [here](https://www.digitalocean.com/community/articles/how-to-install-bro-ids-2-2-on-ubuntu-12-04)
   - or this one [here](http://www.justbeck.com/getting-started-with-bro-ids/)
   - or go to offical Bro Downloads [www.bro.org/download/](http://www.bro.org/download)

    
###Install Indexers:

#### Mac/OSX
- brew install elasticsearch
- pip install -U elasticsearch
- brew install neo4j
    - Note: You may need to install Java JDK 1.7 [Oracle JDK 1.7 DMG](http://download.oracle.com/otn-pub/java/jdk/7u51-b13/jdk-7u51-macosx-x64.dmg) for macs.

#### Ubuntu (14.04 and 12.04)
- Neo4j: See official instructions for Neo4j [here](http://www.neo4j.org/download/linux)
    - Note: You may need to install Java JDK 1.7. If you have Java 1.7 installed , and error says otherwise, run update-alternatives --config java and select Java 1.7

- ElasticSearch:
    - wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.2.1.deb
    - sudo dpkg -i elasticsearch-1.2.1.deb
    - sudo update-rc.d elasticsearch defaults 95 10
    - sudo /etc/init.d/elasticsearch start
    - Any issues see [elasticsearch_webpage](http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/setup-service.html)

<br>
<img src="http://raw.github.com/supercowpowers/workbench/master/images/warning.jpg" width=90 align="left">
- Pull the repository
<pre>
git clone https://github.com/supercowpowers/workbench.git
</pre>
**Warning!: The repository contains malcious data samples, be careful, exclude the workbench directory from AV, etc...**
<br><br>

#### Python Modules:
Note: Workbench is continuously tested with python 2.7. We're currently working on Python 3 support ([Issue 92](https://github.com/SuperCowPowers/workbench/issues/92)).

* cd workbench
* pip install -r requirements.txt
* Go have a large cup of coffee...


## Running It:
#### Server (localhost or server machine)
<pre>
$ cd workbench
$ ./workbench
</pre>
#### Example Clients (use -s for remote server)
There are about a dozen example clients showing how to use workbench on pcaps, PEfiles, pdfs, and log files. We even has a simple nodes.js client (looking for node devs to pop some pull requests :).
<pre>
$ cd workbench/clients
$ python simple_workbench_client.py [-s tcp://mega.server.com]
</pre>

## Testing:
Unit testing and sub-pipeline tests
<pre>
$ cd workbench/server/workers
$ ./runtests
</pre>
      
Full pipeline tests (clients exercise a larger set of components)
<pre>
$ cd workbench/clients
$ ./runtests
</pre>

### Benign Error
We have no idea why occasionaly you see this pop up in the server output. To our knowledge it literally has no impact on any functionality or robustness. If you know anything about this please help us out by opening an issue and pull request. :)
<pre>
ERROR:zerorpc.channel:zerorpc.ChannelMultiplexer, unable to route event:
_zpc_more {'response_to': '67d7df3f-1f3e-45f4-b2e6-352260fa1507', 'zmqid':
['\x00\x82*\x01\xea'], 'message_id': '67d7df42-1f3e-45f4-b2e6-352260fa1507',
'v': 3} [...]
</pre>
### VirusTotal Warning
The vt_query.py worker uses a shared 'low-volume' API key provided by SuperCowPowers LLC. When running the vt_query worker the following warning happens quite often:

    "VirusTotal Query Error, no valid response... past per min quota?"
If you'd like to use the vt_query worker on a regular basis, you'll have to put your own VirusTotal API key in the workbench/server/config.ini file.
<br>

### Optional Tools
**Robomongo**

Robomongo is a shell-centric cross-platform MongoDB management tool. Simply, it is a handy GUI to inspect your mongodb.

- http://robomongo.org/
- download and follow install instructions
- create a new connection to localhost (default settings fine). Name it as you wish.

### Dependency Installation Errors
**Python Modules**

Note: If you get a bunch of clang errors about unknown arguments or 'cannot link a simple C program' add the following FLAGs:
    
    ```
    $ export CFLAGS=-Qunused-arguments
    $ export CPPFLAGS=-Qunused-arguments
    ```

**Errors when running Tests**

If when running the worker tests you get some errors like 'MagicError: regexec error 17, (illegal byte sequence)' it's an issue with libmagic 5.17, revert to libmagic 5.16. Using brew on Mac:

    $ cd /usr/local
    $ brew versions libmagic # Copy the line for version 5.16, then paste (for me it looked like the following line)
    $ git checkout bfb6589 Library/Formula/libmagic.rb
    $ brew uninstall libmagic
    $ brew install libmagic
### Deprecated Stuff

**Scapy Install**

- brew tap Homebrew/python
- brew install scapy
- brew install pypcap
  - If you get error about pyrex.distutils:
    - pip install pyrex (or if this doesn't work do easy_install pyrex)
    - and then retry the 'brew install pypcap' 
  - Still not working try pyrex from scatch [pyrex](http://www.cosc.canterbury.ac.nz/greg.ewing/python/Pyrex/)
<br><br>

  (2-5-14): For scapy python binding you have to manually install the latest release from
[secdev.org](http://www.secdev.org/projects/scapy/doc/installation.html#latest-release) and follow the instructions (like first 5 lines)
  <pre>
$ wget http://www.secdev.org/projects/scapy/files/scapy-latest.zip
$ unzip scapy-latest.zip
$ cd scapy-2.*
$ sudo python setup.py install
</pre>

### Deprecated Instructions for Ubuntu 12.04
#### Ubuntu (tested on 12.04)
- Mongo: Go through the steps given at [MongoDB Installation Tutorial](http://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/)
- Bro IDS: Check out the Installation tutorial [here](https://www.digitalocean.com/community/articles/how-to-install-bro-ids-2-2-on-ubuntu-12-04)
- Yara: Read the installation instructions [here](https://github.com/plusvic/yara/releases/latest)
- sudo apt-get install libmagic-dev
- sudo apt-get install libxml2-dev
- sudo apt-get install libxslt-dev
- sudo apt-get install libevent-dev