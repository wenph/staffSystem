#coding=utf-8
__author__ = 'admin'

from apps.project.project_models import ProjectBase
from apps.staff.staff_models import UserBase
from db_engin import engine

#建表代码
def creat_db_tables():
    UserBase.metadata.create_all(engine)
    ProjectBase.metadata.create_all(engine)

if __name__ == '__main__':
    creat_db_tables()