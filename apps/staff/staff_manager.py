#coding=cp936
__author__ = 'admin'

import copy
from apps.db.db_models import User, UserProject, Project
from apps.db.db_session import session
from apps.utils.tools import ToolsManager
from sqlalchemy import and_, or_, except_

class StaffManager(object):
    @staticmethod
    def add_staff(user_obj):
        items = session.query(User).filter(User.name == user_obj.name).all()
        if len(items) == 0:     # 数据库中没有重名的存在，则添加
            session.add(user_obj)
            session.commit()
        else:
            # 弹出警告
            ToolsManager.information_box(u"注意", u"\"%s\"已经存在数据库中!" % unicode(user_obj.name))

    @staticmethod
    def delete_staff(ids_list):
        session.query(User).filter(User.id.in_(ids_list)).delete(synchronize_session=False)
        session.commit()

    @staticmethod
    def search_staff():
        query = StaffManager.get_all_staff()
        search_datas = []
        i = 0
        for query_meta in query:
            search_datas.append([])
            search_datas[i].append(query_meta.id)
            search_datas[i].append(query_meta.name)
            search_datas[i].append(query_meta.employee_id)
            search_datas[i].append(query_meta.phone_number)
            search_datas[i].append(query_meta.tel_number)
            search_datas[i].append(query_meta.birth_date)
            search_datas[i].append(query_meta.title)
            search_datas[i].append(query_meta.position)
            search_datas[i].append(query_meta.education)
            i += 1
        return search_datas

    @staticmethod
    def get_all_staff():
        query_result = session.query(User).all()
        return query_result

    @staticmethod
    def updata_staff(dic):
        item = session.query(User).filter(User.id == dic.get('id')).one()
        item.name = dic.get('name')
        item.employee_id = dic.get('employee_id')
        item.phone_number = dic.get('phone_number')
        item.tel_number = dic.get('tel_number')
        item.birth_date = dic.get('birth_date')
        item.title = dic.get('title')
        item.position = dic.get('position')
        item.education = dic.get('education')
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
        if attendee_ids_str not in (None, ''):
            attendee_ids_list = attendee_ids_str.split(',')
            for id in attendee_ids_list:
                item = UserProject(user_id=id, project_id=project_id)
                session.add(item)
            session.commit()

    @staticmethod
    def delete_staff_project_by_project_ids(project_ids):
        session.query(UserProject).filter(UserProject.project_id.in_(project_ids)).delete(synchronize_session=False)
        session.commit()

    @staticmethod
    def delete_staff_project_by_staff_ids(user_ids):
        session.query(UserProject).filter(UserProject.user_id.in_(user_ids)).delete(synchronize_session=False)
        session.commit()

    @staticmethod
    def delete_staff_project_by_staff_project_id(user_id, project_id):
        session.query(UserProject).filter(and_(UserProject.user_id == user_id, UserProject.project_id == project_id)).delete()

    @staticmethod
    def search_staff_project_by_staff_name_and_data(**kwargs):
        search_datas = []
        i = 0
        staff_id = StaffManager.get_one_item_by_name(kwargs.get('name')).id
        query_result = session.query(UserProject).filter(UserProject.user_id == staff_id).all()
        for query_meta in query_result:
            if query_meta.project.start_time > kwargs.get('end_time') or query_meta.project.end_time < kwargs.get('start_time'):
                pass
            else:
                search_datas.append([])
                search_datas[i].append(query_meta.user.name)
                search_datas[i].append(query_meta.project.name)
                search_datas[i].append(query_meta.project.start_time)
                search_datas[i].append(query_meta.project.end_time)
                search_datas[i].append(query_meta.project.attendee)
                i += 1
        return search_datas