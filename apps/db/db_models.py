#coding=cp936
__author__ = 'admin'


from sqlalchemy import Table, MetaData, Column, ForeignKey, Integer, String, Unicode, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    employee_id = Column(String)
    phone_number = Column(String)
    tel_number = Column(String)
    birth_date = Column(Date)
    title = Column(String)
    position = Column(String)
    education = Column(String)
    userproject = relationship('UserProject')

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    search_id = Column(String)
    source_place = Column(String)
    main_designer = Column(String)
    design_all = Column(String)
    responsible_man = Column(String)
    start_time = Column(Date)
    end_time = Column(Date)
    attendee = Column(String)
    userproject = relationship('UserProject')


class UserProject(Base):
    __tablename__ = 'users_projects'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    user = relationship("User", backref=backref("users_projects", order_by=id))
    project = relationship("Project", backref=backref("users_projects", order_by=id))