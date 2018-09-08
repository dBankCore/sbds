# -*- coding: utf-8 -*-
import dateutil.parser


from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import Column
from sqlalchemy import Numeric
from sqlalchemy import Unicode
from sqlalchemy import UnicodeText
from sqlalchemy import Boolean
from sqlalchemy import SmallInteger
from sqlalchemy import Integer
from sqlalchemy import BigInteger
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy import Index
from sqlalchemy.dialects.postgresql import JSONB
from toolz.dicttoolz import dissoc

import dpds.dpds_json

from ..import Base
from ...enums import operation_types_enum
from ...field_handlers import json_string_field
from ...field_handlers import amount_field
from ...field_handlers import amount_symbol_field
from ...field_handlers import comment_body_field


class EscrowTransferOperation(Base):
    """

    dPay Blockchain Example
    ======================
    {
      "agent": "jared",
      "bbd_amount": "1.000 BBD",
      "json_meta": "{}",
      "dpay_amount": "0.000 BEX",
      "escrow_expiration": "2017-02-28T11:22:39",
      "fee": "0.100 BBD",
      "to": "stan",
      "ratification_deadline": "2017-02-26T11:22:39",
      "escrow_id": 23456789,
      "from": "siol"
    }

    """

    __tablename__ = 'dpds_op_escrow_transfers'
    __table_args__ = (
        PrimaryKeyConstraint('block_num', 'transaction_num', 'operation_num'),
        ForeignKeyConstraint(['from'], ['dpds_meta_accounts.name'],
            deferrable=True, initially='DEFERRED', use_alter=True),
        ForeignKeyConstraint(['to'], ['dpds_meta_accounts.name'],
            deferrable=True, initially='DEFERRED', use_alter=True),
        ForeignKeyConstraint(['agent'], ['dpds_meta_accounts.name'],
            deferrable=True, initially='DEFERRED', use_alter=True),)


    block_num = Column(Integer, nullable=False, index=True)
    transaction_num = Column(SmallInteger, nullable=False, index=True)
    operation_num = Column(SmallInteger, nullable=False, index=True)
    trx_id = Column(String(40),nullable=False)
    timestamp = Column(DateTime(timezone=False))
    _from = Column('from',String(16)) # name:from
    to = Column(String(16)) # dpay_type:account_name_type
    agent = Column(String(16)) # dpay_type:account_name_type
    escrow_id = Column(Numeric) # dpay_type:uint32_t
    bbd_amount = Column(Numeric(20,6), nullable=False) # dpay_type:asset
    bbd_amount_symbol = Column(String(5)) # dpay_type:asset
    dpay_amount = Column(Numeric(20,6), nullable=False) # dpay_type:asset
    dpay_amount_symbol = Column(String(5)) # dpay_type:asset
    fee = Column(Numeric(20,6), nullable=False) # dpay_type:asset
    fee_symbol = Column(String(5)) # dpay_type:asset
    ratification_deadline = Column(DateTime) # dpay_type:time_point_sec
    escrow_expiration = Column(DateTime) # dpay_type:time_point_sec
    json_meta = Column(JSONB) # name:json_meta
    operation_type = Column(operation_types_enum,nullable=False,index=True,default='escrow_transfer')


    _fields = dict(
        bbd_amount=lambda x: amount_field(x.get('bbd_amount'), num_func=float), # dpay_type:asset
        bbd_amount_symbol=lambda x: amount_symbol_field(x.get('bbd_amount')), # dpay_type:asset
        dpay_amount=lambda x: amount_field(x.get('dpay_amount'), num_func=float), # dpay_type:asset
        dpay_amount_symbol=lambda x: amount_symbol_field(x.get('dpay_amount')), # dpay_type:asset
        fee=lambda x: amount_field(x.get('fee'), num_func=float), # dpay_type:asset
        fee_symbol=lambda x: amount_symbol_field(x.get('fee')), # dpay_type:asset
        ratification_deadline=lambda x: dateutil.parser.parse(x.get('ratification_deadline')), # dpay_type:time_point_sec
        escrow_expiration=lambda x: dateutil.parser.parse(x.get('escrow_expiration')), # dpay_type:time_point_sec
        json_meta=lambda x: json_string_field(x.get('json_meta')), # name:json_meta

    )

    _account_fields = frozenset(['from','to','agent',])

    def dump(self):
        return dissoc(self.__dict__, '_sa_instance_state')

    def to_dict(self, decode_json=True):
        data_dict = self.dump()
        if isinstance(data_dict.get('json_metadata'), str) and decode_json:
            data_dict['json_metadata'] = dpds.dpds_json.loads(
                data_dict['json_metadata'])
        return data_dict

    def to_json(self):
        data_dict = self.to_dict()
        return dpds.dpds_json.dumps(data_dict)

    def __repr__(self):
        return "<%s (block_num:%s transaction_num: %s operation_num: %s keys: %s)>" % (
            self.__class__.__name__, self.block_num, self.transaction_num,
            self.operation_num, tuple(self.dump().keys()))

    def __str__(self):
        return str(self.dump())
