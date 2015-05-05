#coding=utf-8
__author__ = 'admin'


from sqlalchemy import Table, MetaData, Column, ForeignKey, Integer, String, Unicode, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


UserBase = declarative_base()
class User(UserBase):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    employee_id = Column(String)
    phone_number = Column(String)
    birth_date = Column(String)
    title = Column(String)
    position = Column(String)
    education = Column(String)
    #user_project = relationship('UserPorject')
    #is_busy = Column(String)

class UserPorject(UserBase):
    __tablename__ = 'users_projects'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    project_id = Column(Integer, nullable=False)