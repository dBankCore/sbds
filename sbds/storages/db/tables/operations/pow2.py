# coding=utf-8

import os.path

from sqlalchemy import Column
from sqlalchemy import Unicode
from toolz import get_in

from .. import Base
from ...enums import operation_types_enum
from .base import BaseOperation


class Pow2Operation(Base, BaseOperation):
    """Raw Format
    ==========

    {
        "ref_block_prefix": 2030100032,
        "expiration": "2017-01-20T17:43:24",
        "operations": [
            [
                "pow2",
                {
                    "work": [
                        1,
                        {
                            "prev_block": "0083f04940de00790a548572b5f7a09d2a9e6676",
                            "pow_summary": 3542335882,
                            "proof": {
                                "inputs": [
                                    2930666,
                                    3055534,
                                    16227194,
                                    1878724,
                                    3055534,
                                    3370375,
                                    10368718,
                                    8279292,
                                    1878724,
                                    12665269,
                                    13416647,
                                    14101780,
                                    14954112,
                                    16332900,
                                    7269530,
                                    13055417,
                                    16709657,
                                    14859041,
                                    8879475,
                                    3839300,
                                    8879475,
                                    14954112,
                                    3370375,
                                    7416112,
                                    15613499,
                                    15613499,
                                    6086878,
                                    9856240,
                                    587509,
                                    587509,
                                    6047993,
                                    10368718,
                                    6449363,
                                    7416112,
                                    15056305,
                                    8279292,
                                    13055417,
                                    6086878,
                                    16332900,
                                    14859041,
                                    308997,
                                    13416647,
                                    14101780,
                                    2930666,
                                    2552223,
                                    12665269,
                                    2552223,
                                    6047993,
                                    308997,
                                    16709657,
                                    3654688,
                                    9885009,
                                    15056305,
                                    9856240,
                                    7269530,
                                    3654688,
                                    5757028,
                                    16227194,
                                    5757028,
                                    3839300,
                                    9885009,
                                    6449363,
                                    2141293,
                                    2141293
                                ],
                                "n": 140,
                                "seed": "3dbe4a5694af55d7bccc622a7b2d41293c26d5290ca43bd9754104d99c52dd2a",
                                "k": 6
                            },
                            "input": {
                                "prev_block": "0083f04940de00790a548572b5f7a09d2a9e6676",
                                "nonce": "11247522470727134118",
                                "worker_account": "nori"
                            }
                        }
                    ],
                    "props": {
                        "account_creation_fee": "0.001 STEEM",
                        "sbd_interest_rate": 1000,
                        "maximum_block_size": 131072
                    }
                }
            ]
        ],
        "signatures": [
            "1f0e5ef13b709989d1256def83f45dd8a89b821cefdf3f5feefa380508233afb0d2c457d04e2c64937f36ff4d6a86e26303f710db1d92749ac6fc8fa8f95259e95"
        ],
        "ref_block_num": 61513,
        "extensions": []
    }


    Args:

    Returns:

    """

    __tablename__ = 'sbds_op_pow2s'
    __operation_type__ = os.path.splitext(os.path.basename(__file__))[0]

    worker_account = Column(Unicode(50), nullable=False, index=True)
    block_id = Column(Unicode(40), nullable=False)

    _fields = dict(
        worker_account=lambda x: get_in(['work', 1, 'input', 'worker_account'], x),
        block_id=lambda x: get_in(['work', 1, 'input', 'prev_block'], x))

    operation_type = Column(
        operation_types_enum,
        nullable=False,
        index=True,
        default=__operation_type__)