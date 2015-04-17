#coding=utf-8
__author__ = 'admin'

from apps.db.db_session import session

class ProjectManager(object):
    @staticmethod
    def add_project(obj):
        session.add(obj)
        session.commit()

    @staticmethod
    def delete_project():
        pass

    @staticmethod
    def search_project():
        pass

