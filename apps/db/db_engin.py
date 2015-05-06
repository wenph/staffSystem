#coding=cp936
__author__ = 'admin'

from sqlalchemy import create_engine
import platform
import os
from apps.project.project_models import ProjectBase
from apps.staff.staff_models import UserBase, UserPorject

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
    UserBase.metadata.create_all(engine)
    ProjectBase.metadata.create_all(engine)
    UserPorject.metadata.create_all(engine)
