#coding=utf-8
__author__ = 'admin'

from staff_models import User
from apps.db.db_session import session
from apps.utils.tools import ToolsManager

class StaffManager(object):
    @staticmethod
    def add_staff(user_obj):
        items = session.query(User).filter(User.name == user_obj.name).all()
        if len(items) == 0:     # 数据库中没有重名的存在，则添加
            session.add(user_obj)
            session.commit()
        else:
            # 弹出警告
            ToolsManager.information_box("注意", "\"%s\"已经存在数据库中!" % str(user_obj.name))

    @staticmethod
    def delete_staff(ids_list):
        items = session.query(User).filter(User.id.in_(ids_list))
        for item in items:
            session.delete(item)
        session.commit()

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

    @staticmethod
    def updata_staff(dic):
        item = session.query(User).filter(User.id == dic.get('id')).one()
        item.name = dic.get('name')
        item.employee_id=dic.get('employee_id')
        item.phone_number=dic.get('phone_number')
        item.birth_date=dic.get('birth_date')
        item.title=dic.get('title')
        item.education=dic.get('education')
        session.add(item)
        session.commit()

    @staticmethod
    def get_one_item_by_id(item_id):
        item = session.query(User).filter(User.id == item_id).one()
        return item



