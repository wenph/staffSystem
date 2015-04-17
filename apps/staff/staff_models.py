#coding=utf-8
__author__ = 'admin'


from sqlalchemy import Table, MetaData, Column, ForeignKey, Integer, String, Unicode, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base


UserBase = declarative_base()
class User(UserBase):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)


