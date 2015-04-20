#coding=utf-8
__author__ = 'admin'

from sqlalchemy import create_engine

# 路径一定要存在才行
engine = create_engine("sqlite:////Users/admin/PycharmProjects/staff_system/staff.db", echo=False)
