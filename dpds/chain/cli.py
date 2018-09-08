# -*- coding: utf-8 -*-
import concurrent.futures
import json

import click

import structlog
from dpds.http_client import SimpleDPayAPIClient
from dpds.utils import chunkify

logger = structlog.get_logger(__name__)


@click.group()
def chain():
    """Query the dPay blockchain"""


@chain.command(name='stream-blocks')
@click.option(
    '--url',
    metavar='DPAYD_HTTP_URL',
    envvar='DPAYD_HTTP_URL',
    default='https://greatchain.dpays.io',
    help='DPayd HTTP server URL')
@click.option('--block_nums', type=click.File('r'))
@click.option(
    '--start',
    help='Starting block_num, default is 1',
    default=1,
    envvar='STARTING_BLOCK_NUM',
    type=click.IntRange(min=1))
@click.option(
    '--end',
    help='Ending block_num, default is infinity',
    metavar="INTEGER BLOCK_NUM",
    type=click.IntRange(min=0),
    default=None)
def stream_blocks(url, block_nums, start, end):
    """Stream blocks from dpayd in JSON format

    \b
    Which DPayd:
    \b
    1. CLI "--url" option if provided
    2. ENV var "DPAYD_HTTP_URL" if provided
    3. Default: "https://greatchain.dpays.io"

    \b
    Which Blocks To Output:
    \b
    - Stream blocks beginning with current block by omitting --start, --end, and BLOCKS
    - Fetch a range of blocks using --start and/or --end
    - Fetch list of blocks by passing BLOCKS a JSON array of block numbers (either filename or "-" for STDIN)

    Where To Output Blocks:

    \b
    2. ENV var "BLOCKS_OUT" if provided
    3. Default: STDOUT
    """
    # Setup dpayd source
    rpc = SimpleDPayAPIClient(url)
    with click.open_file('-', 'w', encoding='utf8') as f:
        if block_nums:
            block_nums = json.load(block_nums)
            blocks = _stream_blocks(rpc, block_nums)
        elif start and end:
            blocks = _stream_blocks(rpc, range(start, end))
        else:
            blocks = rpc.stream(start)

        json_blocks = map(json.dumps, blocks)

        for block in json_blocks:
            click.echo(block, file=f)


def _stream_blocks(rpc, block_nums):
    for block in map(rpc.get_block, block_nums):
        yield block


@chain.command()
@click.option(
    '--url',
    metavar='DPAYD_HTTP_URL',
    envvar='DPAYD_HTTP_URL',
    help='DPayd HTTP server URL')
def block_height(url):
    rpc = SimpleDPayAPIClient(url)
    click.echo(rpc.last_irreversible_block_num())


@chain.command(name='get-blocks')
@click.option('--start', type=click.INT, default=1)
@click.option('--end', type=click.INT, default=0)
@click.option('--chunksize', type=click.INT, default=100)
@click.option('--max_workers', type=click.INT, default=None)
@click.option(
    '--url',
    metavar='DPAYD_HTTP_URL',
    envvar='DPAYD_HTTP_URL',
    help='DPayd HTTP server URL')
def get_blocks_fast(start, end, chunksize, max_workers, url):
    """Request blocks from dpayd in JSON format"""

    rpc = SimpleDPayAPIClient(url)
    if end == 0:
        end = rpc.last_irreversible_block_num()

    with click.open_file('-', 'w', encoding='utf8') as f:
        blocks = _get_blocks_fast(
            start=start,
            end=end,
            chunksize=chunksize,
            max_workers=max_workers,
            rpc=rpc,
            url=url)
        json_blocks = map(json.dumps, blocks)
        for block in json_blocks:
            click.echo(block.encode('utf8'), file=f)


# pylint: disable=too-many-arguments
def _get_blocks_fast(start=None,
                     end=None,
                     chunksize=None,
                     max_workers=None,
                     rpc=None,
                     url=None):
    extra = dict(
        start=start,
        end=end,
        chunksize=chunksize,
        max_workers=max_workers,
        rpc=rpc,
        url=url)
    logger.debug('get_blocks_fast', extra=extra)
    rpc = rpc or SimpleDPayAPIClient(url)
    with concurrent.futures.ThreadPoolExecutor(
            max_workers=max_workers) as executor:
        for i, chunk in enumerate(
                chunkify(range(start, end), chunksize=chunksize), 1):
            logger.debug('get_block_fast loop', extra=dict(chunk_count=i))
            for b in executor.map(rpc.get_block, chunk):
                # dont yield anything when we encounter a null output
                # from an HTTP 503 error
                if b:
                    yield b
