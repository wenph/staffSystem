#coding=utf-8
__author__ = 'admin'

from sqlalchemy.orm import sessionmaker
from db_engin import engine

Session = sessionmaker(bind=engine)
session = Session()
