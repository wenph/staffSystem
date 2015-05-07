#coding=cp936
__author__ = 'admin'

from sqlalchemy import create_engine
import platform
import os
from db_models import Base

DB_NAME = "staff.db"

SYSTEM_TYPE = platform.architecture()
if "windows" in str(SYSTEM_TYPE).lower():
    #���ݿ��ַ
    DB_PATH = "D:\\staff_system"
    DB_FILE_PATH = DB_PATH + "\\" + DB_NAME
else:
    DB_PATH = "/Users/admin/staff_system"
    DB_FILE_PATH = DB_PATH + "/" + DB_NAME
if not os.path.exists(DB_PATH):
    os.makedirs(DB_PATH)

engine = create_engine("sqlite:///%s/staff.db" % DB_PATH, echo=False)
# ��������ڣ��򴴽���
if not os.path.exists(DB_FILE_PATH):
    Base.metadata.create_all(engine)