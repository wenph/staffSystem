#coding=utf-8
__author__ = 'admin'

from sqlalchemy import create_engine
import platform
import os

SYSTEM_TYPE = platform.architecture()
if "windows" in str(SYSTEM_TYPE).lower():
    #数据库地址
    DB_PATH = "D:\\staff_system"
else:
    DB_PATH = "/Users/admin/staff_system"
if not os.path.exists(DB_PATH):
    os.makedirs(DB_PATH)

# 路径一定要存在才行
# engine = create_engine("sqlite:////Users/admin/PycharmProjects/staff_system/staff.db", echo=False)

engine = create_engine("sqlite:///%s/staff.db" % DB_PATH, echo=False)
