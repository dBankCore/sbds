# -*- coding: utf-8 -*-

import json

import click

import structlog
from dpds.http_client import SimpleDPayAPIClient
from dpds.storages.db.tables import Base
from dpds.storages.db.tables import Session
from dpds.storages.db.tables import init_tables
from dpds.storages.db.tables import reset_tables
from dpds.storages.db.tables import test_connection
from dpds.storages.db.tables.block import Block
from dpds.storages.db.utils import isolated_engine_config
from dpds.utils import chunkify

logger = structlog.get_logger(__name__)


@click.group(short_help='Interact with an SQL storage backend')
@click.option(
    '--database_url',
    type=str,
    envvar='DATABASE_URL',
    required=True,
    help='Database connection URL in RFC-1738 format, read from "DATABASE_URL" ENV var by default'
)
@click.option('--echo', is_flag=True)
@click.pass_context
def db(ctx, database_url, echo):
    """Interact with an SQL storage backend
        Typical usage would be reading blocks in JSON format from STDIN
        and then storing those blocks in the database:

        \b
            dpds | db insert-blocks

        In the example above, the "dpds" command streams new blocks to STDOUT, which are piped to STDIN of
        the "db insert-blocks" command by default. The "database_url" was read from the "DATABASE_URL"
        ENV var, though it may optionally be provided on the command line:

        \b
        db --database_url 'dialect[+driver]://user:password@host/dbname[?key=value..]' tests

    """
    with isolated_engine_config(database_url, echo=echo) as engine_config:
        ctx.obj = dict(
            database_url=database_url,
            url=engine_config.url,
            engine_kwargs=engine_config.engine_kwargs,
            engine=engine_config.engine,
            base=Base,
            metadata=Base.metadata,
            Session=Session)


@db.command()
@click.pass_context
def test(ctx):
    """Test connection to database"""
    database_url = ctx.obj['database_url']
    url, table_count = test_connection(database_url)
    if url:
        click.echo('Success! Connected using %s, found %s tables' %
                   (url.__repr__(), table_count))
    else:
        click.echo('Failed to connect: %s' % url)
        ctx.exit(code=127)


@db.command(name='insert-blocks')
@click.argument('blocks', type=click.File('r', encoding='utf8'), default='-')
@click.pass_context
def insert_blocks(ctx, blocks):
    """Insert blocks into the database"""
    engine = ctx.obj['engine']
    database_url = ctx.obj['database_url']
    metadata = ctx.obj['metadata']

    # init tables first
    init_tables(database_url, metadata)

    # configure session
    Session.configure(bind=engine)
    session = Session()

    add_blocks(
        blocks, session, insert=True, merge_insert=False, insert_many=False)



@db.command(name='bulk-add')
@click.argument('blocks', type=click.File('r', encoding='utf8'), default='-')
@click.option('--chunksize', type=click.INT, default=1000)
@click.pass_context
def bulk_add_blocks(ctx, blocks, chunksize):
    """Insert many blocks in the database"""
    engine = ctx.obj['engine']
    database_url = ctx.obj['database_url']
    metadata = ctx.obj['metadata']

    # init tables first
    init_tables(database_url, metadata)

    # configure session
    Session.configure(bind=engine)
    session = Session()
    click.echo("SQL: 'SET SESSION innodb_lock_wait_timeout=150'", err=True)
    session.execute('SET SESSION innodb_lock_wait_timeout=150')

    try:
        for chunk in chunkify(blocks, chunksize):
            bulk_add(chunk, session)
    except Exception as e:
        raise e
    finally:
        session.close_all()


@db.command(name='init')
@click.pass_context
def init_db_tables(ctx):
    """Create any missing tables on the database"""
    database_url = ctx.obj['database_url']
    metadata = ctx.obj['metadata']

    init_tables(database_url, metadata)


@db.command(name='reset')
@click.confirmation_option(
    prompt='Are you sure you want to drop and then create all db tables?')
@click.pass_context
def reset_db_tables(ctx):
    """Drop and then create tables on the database"""
    database_url = ctx.obj['database_url']
    metadata = ctx.obj['metadata']
    reset_tables(database_url, metadata)


@db.command(name='last-block')
@click.pass_context
def last_block(ctx):
    """Return the highest block stored in the database"""
    engine = ctx.obj['engine']
    database_url = ctx.obj['database_url']
    metadata = ctx.obj['metadata']

    # init tables first
    init_tables(database_url, metadata)

    # configure session
    Session.configure(bind=engine)
    session = Session()

    click.echo(Block.highest_block(session))


@db.command(name='find-missing-blocks')
@click.option(
    '--url',
    metavar='DPAYD_HTTP_URL',
    envvar='DPAYD_HTTP_URL',
    required=True,
    help='DPayd HTTP server URL')
@click.pass_context
def find_missing_blocks(ctx, url):
    """Return JSON array of block_nums from missing blocks"""

    engine = ctx.obj['engine']
    database_url = ctx.obj['database_url']
    metadata = ctx.obj['metadata']
    rpc = SimpleDPayAPIClient(url)

    # init tables first
    init_tables(database_url, metadata)

    # configure session
    Session.configure(bind=engine)
    session = Session()

    last_chain_block = rpc.last_irreversible_block_num()

    click.echo(
        json.dumps(
            Block.find_missing(session, last_chain_block=last_chain_block)))


@db.command(name='raw-sql')
@click.argument('sql')
@click.pass_context
def raw_sql(ctx, sql):
    """Execute raw sql query"""
    engine = ctx.obj['engine']
    database_url = ctx.obj['database_url']
    metadata = ctx.obj['metadata']
    from sqlalchemy.sql import text
    # init tables first
    init_tables(database_url, metadata)
    stmt = text(sql)
    with engine.connect() as conn:
        results = conn.execute(stmt).fetchall()
    click.echo(json.dumps(results))
