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
        search_datas = []
        i = 0
        query = session.query(User).all()
        for query_meta in query:
            search_datas.append([])
            search_datas[i].append(query_meta.id)
            search_datas[i].append(query_meta.name)
            search_datas[i].append(query_meta.employee_id)
            search_datas[i].append(query_meta.phone_number)
            search_datas[i].append(query_meta.birth_date)
            search_datas[i].append(query_meta.title)
            search_datas[i].append(query_meta.education)
            search_datas[i].append(query_meta.is_busy)
            i = i + 1
        return search_datas


if __name__ == '__main__':
    StaffManager.search_staff()
