#coding=cp936
__author__ = 'admin'

from apps.db.db_models import Project
from apps.db.db_session import session
from apps.utils.tools import ToolsManager
from apps.staff.staff_manager import StaffManager

class ProjectManager(object):
    @staticmethod
    def add_project(user_obj):
        items = session.query(Project).filter(Project.name == user_obj.name).all()
        if len(items) == 0:     # 数据库中没有重名的存在，则添加
            session.add(user_obj)
            session.commit()
        else:
            # 弹出警告
            ToolsManager.information_box(u"注意", u"\"%s\"已经存在数据库中!" % str(user_obj.name))
        return user_obj

    @staticmethod
    def delete_project(ids_list):
        session.query(Project).filter(Project.id.in_(ids_list)).delete(synchronize_session=False)
        session.commit()

    @staticmethod
    def search_project():
        search_datas = []
        i = 0
        query = session.query(Project).all()
        for query_meta in query:
            search_datas.append([])
            search_datas[i].append(query_meta.id)
            search_datas[i].append(query_meta.name)
            search_datas[i].append(query_meta.search_id)
            search_datas[i].append(query_meta.source_place)
            search_datas[i].append(query_meta.main_designer)
            search_datas[i].append(query_meta.design_all)
            search_datas[i].append(query_meta.responsible_man)
            search_datas[i].append(query_meta.attendee)
            search_datas[i].append(query_meta.start_time)
            search_datas[i].append(query_meta.end_time)
            i = i + 1
        return search_datas

    @staticmethod
    def updata_project(dic):
        item = session.query(Project).filter(Project.id == dic.get('id')).one()
        item.name = dic.get('name')
        item.search_id = dic.get('search_id')
        item.source_place = dic.get('source_place')
        item.main_designer = dic.get('main_designer')
        item.design_all = dic.get('design_all')
        item.responsible_man = dic.get('responsible_man')
        item.attendee = dic.get('attendee')
        item.start_time = dic.get('start_time')
        item.end_time = dic.get('end_time')
        session.add(item)
        session.commit()
        StaffManager.delete_staff_project_by_project_ids([item.id])
        StaffManager.add_staff_project(item.id, dic.get('attendee_ids'))

    @staticmethod
    def get_one_item_by_id(item_id):
        item = session.query(Project).filter(Project.id == item_id).one()
        return item
