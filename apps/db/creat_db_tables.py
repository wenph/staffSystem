#coding=utf-8
__author__ = 'admin'

from apps.project.project_models import ProjectBase
from apps.staff.staff_models import UserBase
from sqlalchemy import create_engine


engine = create_engine("sqlite:////Users/admin/PycharmProjects/staffSystem/tutorial.db", echo=False)

#见表打开以下代码
#UserBase.metadata.create_all(engine)
#ProjectBase.metadata.create_all(engine)
