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


class LimitOrderCreate2Operation(Base):
    """

    dPay Blockchain Example
    ======================


    """

    __tablename__ = 'dpds_op_limit_order_create2s'
    __table_args__ = (
        PrimaryKeyConstraint('block_num', 'transaction_num', 'operation_num'),
        ForeignKeyConstraint(['owner'], ['dpds_meta_accounts.name'],
            deferrable=True, initially='DEFERRED', use_alter=True),)


    block_num = Column(Integer, nullable=False, index=True)
    transaction_num = Column(SmallInteger, nullable=False, index=True)
    operation_num = Column(SmallInteger, nullable=False, index=True)
    trx_id = Column(String(40),nullable=False)
    timestamp = Column(DateTime(timezone=False))
    owner = Column(String(16)) # dpay_type:account_name_type
    orderid = Column(Numeric) # dpay_type:uint32_t
    amount_to_sell = Column(Numeric(20,6), nullable=False) # dpay_type:asset
    amount_to_sell_symbol = Column(String(5)) # dpay_type:asset
    fill_or_kill = Column(Boolean) # dpay_type:bool
    exchange_rate = Column(JSONB) # dpay_type:price
    expiration = Column(DateTime) # dpay_type:time_point_sec
    operation_type = Column(operation_types_enum,nullable=False,index=True,default='limit_order_create2')


    _fields = dict(
        amount_to_sell=lambda x: amount_field(x.get('amount_to_sell'), num_func=float), # dpay_type:asset
        amount_to_sell_symbol=lambda x: amount_symbol_field(x.get('amount_to_sell')), # dpay_type:asset
        exchange_rate=lambda x:json_string_field(x.get('exchange_rate')), # dpay_type:price
        expiration=lambda x: dateutil.parser.parse(x.get('expiration')), # dpay_type:time_point_sec

    )

    _account_fields = frozenset(['owner',])

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
