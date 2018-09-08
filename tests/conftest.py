# -*- coding: utf-8 -*-
import json
import os.path
import glob

import pytest
import requests
from requests.exceptions import ConnectionError

from dpds.http_client import SimpleDPayAPIClient
from dpds.storages.db.tables import Session
from dpds.storages.db.utils import configure_engine

import dpds
import dpds.chain
import dpds.chain.cli
import dpds.server
import dpds.server.cli
import dpds.server.methods
import dpds.server.serve
import dpds.storages
import dpds.storages.db
import dpds.storages.db.cli
import dpds.storages.db.data_types
import dpds.storages.db.enums
import dpds.storages.db.field_handlers
import dpds.storages.db.query_helpers
import dpds.storages.db.utils
import dpds.storages.db.scripts
import dpds.storages.db.scripts.populate
import dpds.storages.db.tables.async_core
import dpds.storages.db.tables.block
import dpds.storages.db.tables.core
import dpds.storages.db.tables.operations


TEST_DIR = os.path.dirname(__file__)
TEST_DATA_DIR = os.path.join(TEST_DIR, 'data')
GET_BLOCK_DATA_DIR = os.path.join(TEST_DATA_DIR, 'get_block')
GET_OPS_IN_BLOCK_DATA_DIR = os.path.join(TEST_DATA_DIR, 'get_ops_in_block')


def load_data(dir):
    results_dict = {}
    for filename in glob.iglob(f'{dir}/*.json'):
        key = os.path.splitext(os.path.basename(filename))[0]
        with open(filename) as f:
            results_dict[key] = json.load(f)
    return results_dict


@pytest.fixture()
def blocks_without_txs(http_client, number_of_blocks=5):
    return list(map(http_client.get_block, range(1, 1 + number_of_blocks)))


@pytest.fixture()
def blocks_with_txs(http_client, number_of_blocks=5):
    return list(
        map(http_client.get_block, range(1092, 1092 + number_of_blocks)))


@pytest.fixture()
def first_block_dict():
    return {
        'extensions': [],
        'previous':
        '0000000000000000000000000000000000000000',
        'timestamp':
        '2016-03-24T16:05:00',
        'transaction_merkle_root':
        '0000000000000000000000000000000000000000',
        'transactions': [],
        'witness':
        'initminer',
        'witness_signature':
        '204f8ad56a8f5cf722a02b035a61b500aa59b9519b2c33c77a80c0a714680a5a5a7a340d909d19996613c5e4ae92146b9add8a7a663eef37d837ef881477313043'
    }


@pytest.fixture()
def http_client(url='https://greatchain.dpays.io', **kwargs):
    return SimpleDPayAPIClient(url, **kwargs)


def is_responsive(url):
    """Check if something responds to ``url``."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except ConnectionError:
        return False


@pytest.fixture(scope='session')
def dpds_http_server(docker_ip, docker_services):
    """Ensure that "some service" is up and responsive."""
    url = 'http://localhost:9191'
    docker_services.wait_until_responsive(
        timeout=60.0, pause=0.1, check=lambda: is_responsive(url))
    return url
