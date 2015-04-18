#coding=utf-8
__author__ = 'admin'

from staff_models import User
from apps.db.db_session import session

class StaffManager(object):
    @staticmethod
    def add_staff(user_obj):
        user_obj = User(name="pinghua", fullname=u'温平华', password="123")
        session.add(user_obj)
        session.commit()

    @staticmethod
    def delete_staff():
        pass

    @staticmethod
    def search_staff():
        query = session.query(User).all()
        for query_meta in query:
            print query_meta.id, query_meta.name, query_meta.fullname, query_meta.password


if __name__ == '__main__':
    StaffManager.add_staff('xx')
    StaffManager.search_staff()
