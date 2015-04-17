#coding=utf-8
__author__ = 'admin'

from staff_models import User
from apps.db.db_session import session

class StaffManager(object):
    @staticmethod
    def add_staff(user_obj):
        session.add(user_obj)
        session.commit()

    @staticmethod
    def delete_staff():
        pass

    @staticmethod
    def search_staff():
        pass

