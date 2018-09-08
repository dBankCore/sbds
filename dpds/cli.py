# -*- coding: utf-8 -*-
import os
import logging
import sys

import click
import structlog


from dpds.chain.cli import chain
from dpds.server.cli import server
from dpds.storages.db.cli import db
from dpds.storages.s3.cli import s3
from dpds.storages.fs.cli import fs

from dpds.codegen.cli import codegen

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.dev.ConsoleRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)


logging.basicConfig(
    format="%(message)s",
    stream=sys.stderr,
    level=os.environ.get('LOG_LEVEL', 'INFO'),
)

@click.group(
    short_help='manages storage, retrieval, and querying of the dPay blockchain')
def dpds():
    """The *dpds* CLI manages storage, retrieval, and querying of the dPay
    blockchain.

    dpds has several commands, each of which has additional subcommands.

    \b
    For more detailed information on a command and its flags, run:
        dpds COMMAND --help
    """


dpds.add_command(chain)
dpds.add_command(db)
dpds.add_command(s3)
dpds.add_command(fs)
dpds.add_command(server)
dpds.add_command(codegen)

if __name__ == '__main__':
    dpds()
