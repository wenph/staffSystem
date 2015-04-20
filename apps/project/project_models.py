#coding=utf-8
__author__ = 'admin'


from sqlalchemy import Table, MetaData, Column, ForeignKey, Integer, String, Unicode, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base


ProjectBase = declarative_base()
class Project(ProjectBase):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    search_id = Column(String)
    source_place = Column(String)
    main_designer = Column(String)
    design_all = Column(String)
    responsible_man = Column(String)
    attendee = Column(String)
    start_time = Column(String)
    end_time = Column(String)