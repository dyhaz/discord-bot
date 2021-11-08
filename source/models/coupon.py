# coding: utf-8
from sqlalchemy import Column, DateTime, String, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Coupon(Base):
    __tablename__ = 'coupon'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(200))
    url = Column(String(100))
    voucher_id = Column(INTEGER(11))
    created_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    is_deleted = Column(TINYINT(1))
