#coding=utf-8
__author__ = 'admin'

from sqlalchemy.orm import sessionmaker
from creat_db_tables import engine

Session = sessionmaker(bind=engine)
session = Session()
