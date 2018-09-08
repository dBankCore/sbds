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


class RecoverAccountOperation(Base):
    """

    dPay Blockchain Example
    ======================
    {
      "new_owner_authority": {
        "key_auths": [
          [
            "DWB7j3nhkhHTpXqLEvdx2yEGhQeeorTcxSV6WDL2DZGxwUxYGrHvh",
            1
          ]
        ],
        "account_auths": [],
        "weight_threshold": 1
      },
      "recent_owner_authority": {
        "key_auths": [
          [
            "DWB78Xth94gNxp8nmByFV2vNAhg9bsSdviJ6fQXUTFikySLK3uTxC",
            1
          ]
        ],
        "account_auths": [],
        "weight_threshold": 1
      },
      "account_to_recover": "chitty",
      "extensions": []
    }

    """

    __tablename__ = 'dpds_op_recover_accounts'
    __table_args__ = (
        PrimaryKeyConstraint('block_num', 'transaction_num', 'operation_num'),
        ForeignKeyConstraint(['account_to_recover'], ['dpds_meta_accounts.name'],
            deferrable=True, initially='DEFERRED', use_alter=True),)


    block_num = Column(Integer, nullable=False, index=True)
    transaction_num = Column(SmallInteger, nullable=False, index=True)
    operation_num = Column(SmallInteger, nullable=False, index=True)
    trx_id = Column(String(40),nullable=False)
    timestamp = Column(DateTime(timezone=False))
    account_to_recover = Column(String(16)) # dpay_type:account_name_type
    new_owner_authority = Column(JSONB) # dpay_type:authority
    recent_owner_authority = Column(JSONB) # dpay_type:authority
    extensions = Column(JSONB) # dpay_type:extensions_type
    operation_type = Column(operation_types_enum,nullable=False,index=True,default='recover_account')


    _fields = dict(
        new_owner_authority=lambda x:json_string_field(x.get('new_owner_authority')), # dpay_type:authority
        recent_owner_authority=lambda x:json_string_field(x.get('recent_owner_authority')), # dpay_type:authority
        extensions=lambda x:json_string_field(x.get('extensions')), # dpay_type:extensions_type

    )

    _account_fields = frozenset(['account_to_recover',])

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
