# -*- coding: utf-8 -*-

import json

import boto3
import click

import sbds.logging
from sbds.utils import block_num_from_previous

logger = sbds.logging.getLogger(__name__)


@click.group(name='s3')
@click.argument('bucket', type=click.STRING)
@click.pass_context
def s3(ctx, bucket):
    """This command provides AWS S3 block storage."""
    ctx.obj = dict(
        bucket=bucket,
        s3_resource=boto3.resource('s3'),
        s3_client=boto3.client('s3'),
        region='us-east-1')


@s3.command('create-bucket')
@click.pass_context
def create_bucket(ctx):
    region = ctx.obj['region']
    bucket = ctx.obj['bucket']
    s3_client = ctx.obj['s3_client']
    s3_client.create_bucket(
        Bucket=bucket,
        CreateBucketConfiguration={'LocationConstraint': region})


def put_json_block(s3_resource, block, bucket):
    blocknum = str(block['block_num'])
    key = '/'.join([blocknum, 'block.json'])
    data = bytes(json.dumps(block), 'utf8')
    result = s3_resource.Object(bucket, key).put(
        Body=data, ContentEncoding='UTF-8', ContentType='application/json')
    return block, bucket, blocknum, key, result


@s3.command(name='put-blocks')
@click.argument('blocks', type=click.File('r'))
@click.pass_context
def put_json_blocks(ctx, blocks, bucket):
    for block in blocks:
        block = json.loads(block)
        res_block, res_bucket, res_blocknum, res_key, s3_result = put_json_block(
            block, bucket)


def get_top_level_keys(bucket):
    paginator = client.get_paginator('list_objects_v2')
    result = paginator.paginate(
        Bucket=bucket, Delimiter='/', Prefix='blocknum')
    '''
    nums = [int(p['Prefix'][8:].strip('/')) for p in results[0]['CommonPrefixes']]
    '''
