===============================================
DPDS (dPay Blockchain Data Service)
===============================================

Notice
======

This is prerelease software, not yet suitable for production use.  Proceed at your own risk.


Quickstart
==========

***dpds*** is available on Docker Hub as `dpays/dpds`.

e.g.

``docker run -d dpays/dpds``

Overview
========

Stack: Python 3, SQLAlchemy, bottle.

**dpds** is a set of tool for querying the data of the dPay Blockchain.

While providing direct interfaces to several pluggable storage architectures that may be used for querying the blockchain, **dpds** may also be used as a lower level API upon which other applications can be built.

Architecture
============

The system has three conceptual functions:

1. Interfacing with a `dpayd` instance to provide access to blocks, ranges of blocks, or the continual stream of
blocks as they are published on the blockchain.

2. Ingest, prepare, store, and index blocks in one of two storage backends (S3, SQL Database, and/or Elasticsearch).

3. Querying indexed blocks.

Install
=======

**dpds** is an installable python 3 package, though it is currently not published on pipy, and must be installed using git:

``pip3 install -e git+git@github.com:dpays/dpds.git#egg=dpds``

Installation will (during early development) require mysql and postgres development sources in order to build
correctly. As an alternative to installing those libraries, a `Dockerfile` is available.

Usage
=====

On initial use, blocks can be quickly loaded from "checkpoints" which are gzipped text files that are 1M
blocks in length and currently hosted on S3 at   ``s3://dpay-dpds-checkpoints``.

Once the storage is synced with all previous blocks, blocks can be streamed to storage backends as they are confirmed.

These blocks are not cryptographically assured in any way (and **dpds** does not provide any cryptographic guarantees
or verify blockchain consensus state), so you may wish to regenerate these checkpoints.

**dpds** is designed to always be used in conjunction with a trusted instance of `dpayd` to validate all block data before
**dpds** ever receives it.  This daemon **does not** implement any consensus rules.

CLI
===
The **dpds** package installs the ``dpds`` CLI.

More information

.. command-output:: dpds --help
