About Workbench
===============

A medium-data framework for security research and development teams.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Workbench focuses on simplicity, transparency, and easy on-site
customization. As an open source python project it provides light-weight
task management, execution and pipelining for a loosely-coupled set of
python classes. Please see our set of IPython notebooks below for
examples.

Detailed Project Description
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The workbench project takes the workbench metaphore seriously. It’s a
platform that allows you to do work; it provides a flat work surface
that supports your ability to combine tools (python modules) together.
In general a workbench never constrains you (oh no! you can’t use those
3 tools together!) on the flip side it doesn’t hold your hand either.
Using the workbench software is a bit like using a Lego set, you can put
the pieces together however you want AND adding your own pieces is super
easy!.

-  **Loosely coupled**
-  No inheritance relationships
-  No knowledge of data structures
-  Just take some input and barf some output (no format requirements)
-  **Flat**
-  Workers (that’s it… everything is a worker)
-  Server dynamically loads workers from a directory called ‘workers’
-  **Robust**
-  Worker fails to load (that’s fine)
-  Worker crashes (no sweat, that request fails but system chugs on)
-  **Transparency**
-  All worker output is reflected in the data store (currently Mongo)
-  Use RoboMongo (see below) to inspect exactly what workers are
   outputting.
-  **Small Granularity:**
-  The system works by passing references from one worker to another so
   there is NO benefit to large granularity workers.
-  It’s super easy to have a worker that aggregates information from a
   set of workers, the opposite (breaking apart a large code chunk into
   smaller units) is almost never easy.
-  Pull just what you want, workers and views (which are just workers)
   can be selectve about exactly which fields get pulled from which
   workers.

Bounties (Rewards for contributing to Workbench)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Top Bounties**

-  `Bro Scripts for OWASP Top 10 (1000 Cow Points)`_
-  `Python based SWF Decompiler/Decompression (500 Cow Points)`_
-  `Deep PDF Static Analysis (500 Cow Points)`_
-  `Worker for Cab File extraction (100 Cow Points)`_

**FAQ about Cow Points**

-  Are Cow Points worth anything? : No
-  Will Cow Points ever be worth anything? : Maybe
-  Are Cow Points officially tracked? : Yes
-  Will I receive good Karma for Cow Points? : Yes

.. _Bro Scripts for OWASP Top 10 (1000 Cow Points): /../../issues/27
.. _Python based SWF Decompiler/Decompression (500 Cow Points): /../../issues/28
.. _Deep PDF Static Analysis (500 Cow Points): /../../issues/29
.. _Worker for Cab File extraction (100 Cow Points): /../../issues/30
© 2013–2014 John MacFarlane