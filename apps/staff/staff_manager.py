#coding=cp936
__author__ = 'admin'

from staff_models import User, UserPorject
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
            ToolsManager.information_box(u"注意", u"\"%s\"已经存在数据库中!" % str(user_obj.name))

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

    @staticmethod
    def get_one_item_by_name(item_name):
        item = session.query(User).filter(User.name == item_name).one()
        return item

    @staticmethod
    def add_staff_project(project_id, attendee_ids_str):
        attendee_ids_list = attendee_ids_str.split(',')
        for id in attendee_ids_list:
            item = UserPorject(user_id=id, project_id=project_id)
            session.add(item)
        session.commit()

    @staticmethod
    def search_staff_project(staff_name):
        staff_id = StaffManager.get_one_item_by_name(staff_name).id
        items= session.query(UserPorject).filter(UserPorject.user_id == staff_id)
        for item in items:
            print item.user_id, item.project_id
