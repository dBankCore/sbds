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

from ...import Base
from ....enums import operation_types_enum
from ....field_handlers import json_string_field
from ....field_handlers import amount_field
from ....field_handlers import amount_symbol_field
from ....field_handlers import comment_body_field


class CurationRewardVirtualOperation(Base):
    """

    dPay Blockchain Example
    ======================


    """

    __tablename__ = 'dpds_op_virtual_curation_rewards'
    __table_args__ = (

        ForeignKeyConstraint(['curator'], ['dpds_meta_accounts.name'],
            deferrable=True, initially='DEFERRED', use_alter=True),
        ForeignKeyConstraint(['comment_author'], ['dpds_meta_accounts.name'],
            deferrable=True, initially='DEFERRED', use_alter=True),)

    id = Column(Integer, primary_key=True)

    block_num = Column(Integer, nullable=False, index=True)
    transaction_num = Column(SmallInteger, nullable=False, index=True)
    operation_num = Column(SmallInteger, nullable=False, index=True)
    trx_id = Column(String(40),nullable=False)
    timestamp = Column(DateTime(timezone=False))
    curator = Column(String(16)) # dpay_type:account_name_type
    reward = Column(Numeric(20,6), nullable=False) # dpay_type:asset
    reward_symbol = Column(String(5)) # dpay_type:asset
    comment_author = Column(String(16)) # dpay_type:account_name_type
    comment_permlink = Column(Unicode(256), index=True) # name:comment_permlink,curation_reward_operation
    operation_type = Column(operation_types_enum,nullable=False,index=True,default='curation_reward')


    _fields = dict(
        reward=lambda x: amount_field(x.get('reward'), num_func=float), # dpay_type:asset
        reward_symbol=lambda x: amount_symbol_field(x.get('reward')), # dpay_type:asset

    )

    _account_fields = frozenset(['curator','comment_author',])

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
