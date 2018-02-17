
# coding=utf-8
import os.path

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

from sqlalchemy.dialects.mysql import JSON

from toolz import get_in

from ... import Base
from ....enums import operation_types_enum
from ....field_handlers import amount_field
from ....field_handlers import amount_symbol_field
from ....field_handlers import comment_body_field
from ..base import BaseOperation

class Pow2Input(Base, BaseOperation):
    """
    
    
    Steem Blockchain Example
    ======================

    

    """
    
    __tablename__ = 'sbds_op_pow2_inputs'
    __operation_type__ = 'pow2_input'
    
    worker_account = Column(String(50), index=True) # steem_type:account_name_type
    prev_block = Column(Integer) # steem_type:block_id_type
    nonce = Column(BigInteger) # steem_type:uint64_t
    operation_type = Column(
        operation_types_enum,
        nullable=False,
        index=True,
        default='pow2_input')
    
    _fields = dict(
        worker_account=lambda x: x.get('worker_account'),
        prev_block=lambda x: x.get('prev_block'),
        nonce=lambda x: x.get('nonce'),
    )
