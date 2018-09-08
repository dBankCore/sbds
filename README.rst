
DPDS (Steem Blockchain Data Service)
************************************


Notice
======

This is prerelease software, not yet suitable for production use.
Proceed at your own risk.

Dev Quickstart
==============

`docker-compose -f contrib/docker-compose.yml up`

Quickstart
==========

***dpds*** is available on Docker Hub as *dpays/dpds*.

e.g.

``docker run -d dpays/dpds``


Overview
========

Stack: Python 3, SQLAlchemy, bottle.

**dpds** is a set of tool for querying the data of the dPay
Blockchain.

While providing direct interfaces to several pluggable storage
architectures that may be used for querying the blockchain, **dpds**
may also be used as a lower level API upon which other applications
can be built.


Architecture
============

The system has three conceptual functions:

1. Interfacing with a *dpayd* instance to provide access to blocks,
ranges of blocks, or the continual stream of blocks as they are
published on the blockchain.

1. Ingest, prepare, store, and index blocks in one of two storage
   backends (S3, SQL Database, and/or Elasticsearch).

2. Querying indexed blocks.


Install
=======

**dpds** is an installable python 3 package, though it is currently
not published on pipy, and must be installed using git:

``pip3 install -e git+git@github.com:dpays/dpds.git#egg=dpds``

Installation will (during early development) require mysql and
postgres development sources in order to build correctly. As an
alternative to installing those libraries, a *Dockerfile* is
available.


Usage
=====

On initial use, blocks can be quickly loaded from "checkpoints" which
are gzipped text files that are 1M blocks in length and currently
hosted on S3 at   ``s3://dpay-dpds-checkpoints``.

Once the storage is synced with all previous blocks, blocks can be
streamed to storage backends as they are confirmed.

These blocks are not cryptographically assured in any way (and
**dpds** does not provide any cryptographic guarantees or verify
blockchain consensus state), so you may wish to regenerate these
checkpoints.

**dpds** is designed to always be used in conjunction with a trusted
instance of *dpayd* to validate all block data before **dpds** ever
receives it.  This daemon **does not** implement any consensus rules.


CLI
===

The **dpds** package installs the ``dpds`` CLI.

More information

::

   $ dpds --help
   Usage: dpds [OPTIONS] COMMAND [ARGS]...

     The *dpds* CLI manages storage, retrieval, and querying of the Steem
     blockchain.

     dpds has several commands, each of which has additional subcommands.

     For more detailed information on a command and its flags, run:
         dpds COMMAND --help

   Options:
     --help  Show this message and exit.

   Commands:
     chain        Query the Steem blockchain
     checkpoints  retrieve blocks from blockchain checkpoints
     db           Interact with an SQL storage backend
     s3           Interact with an S3 storage backend
     server       HTTP server for answering DB queries

Checkpoints
===========

The preferred method for checkpoints interaction at the moment is using the checkpoints in the gzipped folder ``s3://dpay-dpds-checkpoints/gzipped``. The idea is to have the access to the gzipped checkpoints dir either locally or on s3, and then you can use the ``dpds checkpoints get-blocks`` command, specifying at start and end blocknum and it will figure out which files to use and spit out the blocks.

Some Examples
-------------
::

Stream blocks 1 to 3450000 from our dev S3 bucket
::
   dpds checkpoints get-blocks s3://dpay-dpds-checkpoints/gzipped --start 1 --end 3450000

Stream blocks 8000000 to the last block from your local copy of our S3 bucket
::
   dpds checkpoints get-blocks /home/ubuntu/checkpoints/gzipped --start 8000000

Stream all blocks from your local copy of our S3 bucket
::
   dpds checkpoints get-blocks /home/ubuntu/checkpoints/gzipped
=======
