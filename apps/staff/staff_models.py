#coding=utf-8
__author__ = 'admin'


from sqlalchemy import Table, MetaData, Column, ForeignKey, Integer, String, Unicode, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base


UserBase = declarative_base()
class User(UserBase):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    employee_id = Column(String)
    phone_number = Column(String)
    birth_date = Column(String)
    title = Column(String)
    education = Column(String)
    is_busy = Column(String)