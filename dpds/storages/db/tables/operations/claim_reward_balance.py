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


class ClaimRewardBalanceOperation(Base):
    """

    dPay Blockchain Example
    ======================
    {
      "reward_dpay": "0.017 BEX",
      "reward_vests": "185.025103 VESTS",
      "account": "ocrdu",
      "reward_bbd": "0.011 BBD"
    }

    """

    __tablename__ = 'dpds_op_claim_reward_balances'
    __table_args__ = (
        PrimaryKeyConstraint('block_num', 'transaction_num', 'operation_num'),
        ForeignKeyConstraint(['account'], ['dpds_meta_accounts.name'],
            deferrable=True, initially='DEFERRED', use_alter=True),)


    block_num = Column(Integer, nullable=False, index=True)
    transaction_num = Column(SmallInteger, nullable=False, index=True)
    operation_num = Column(SmallInteger, nullable=False, index=True)
    trx_id = Column(String(40),nullable=False)
    timestamp = Column(DateTime(timezone=False))
    account = Column(String(16)) # dpay_type:account_name_type
    reward_dpay = Column(Numeric(20,6), nullable=False) # dpay_type:asset
    reward_dpay_symbol = Column(String(5)) # dpay_type:asset
    reward_bbd = Column(Numeric(20,6), nullable=False) # dpay_type:asset
    reward_bbd_symbol = Column(String(5)) # dpay_type:asset
    reward_vests = Column(Numeric(20,6), nullable=False) # dpay_type:asset
    reward_vests_symbol = Column(String(5)) # dpay_type:asset
    operation_type = Column(operation_types_enum,nullable=False,index=True,default='claim_reward_balance')


    _fields = dict(
        reward_dpay=lambda x: amount_field(x.get('reward_dpay'), num_func=float), # dpay_type:asset
        reward_dpay_symbol=lambda x: amount_symbol_field(x.get('reward_dpay')), # dpay_type:asset
        reward_bbd=lambda x: amount_field(x.get('reward_bbd'), num_func=float), # dpay_type:asset
        reward_bbd_symbol=lambda x: amount_symbol_field(x.get('reward_bbd')), # dpay_type:asset
        reward_vests=lambda x: amount_field(x.get('reward_vests'), num_func=float), # dpay_type:asset
        reward_vests_symbol=lambda x: amount_symbol_field(x.get('reward_vests')), # dpay_type:asset

    )

    _account_fields = frozenset(['account',])

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
