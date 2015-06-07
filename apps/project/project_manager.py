#coding=cp936
__author__ = 'admin'

from apps.db.db_models import Project
from apps.db.db_session import session
from apps.utils.tools import ToolsManager
from apps.staff.staff_manager import StaffManager
from sqlalchemy import and_, or_, except_, desc

class ProjectManager(object):
    @staticmethod
    def add_project(user_obj):
        items = session.query(Project).filter(Project.name == user_obj.name).all()
        if len(items) == 0:     # ���ݿ���û�������Ĵ��ڣ������
            session.add(user_obj)
            session.commit()
        else:
            # ��������
            ToolsManager.information_box(u"ע��", u"\"%s\"�Ѿ��������ݿ���!" % unicode(user_obj.name))
        return user_obj

    @staticmethod
    def delete_project(ids_list):
        session.query(Project).filter(Project.id.in_(ids_list)).delete(synchronize_session=False)
        session.commit()

    @staticmethod
    def project_data_format(query_result):
        '''
        �������������װ�ɱ���������ݸ�ʽ
        '''
        search_datas = []
        for query_meta in query_result:
            query_meta_list = []
            query_meta_list.append(query_meta.id)
            query_meta_list.append(query_meta.name)
            query_meta_list.append(query_meta.search_id)
            query_meta_list.append(query_meta.source_place)
            query_meta_list.append(query_meta.main_designer)
            query_meta_list.append(query_meta.design_all)
            query_meta_list.append(query_meta.responsible_man)
            query_meta_list.append(query_meta.start_time)
            query_meta_list.append(query_meta.end_time)
            staff_str = StaffManager.search_staff_by_project_id(query_meta.id)
            query_meta_list.append(staff_str)
            query_meta_list.append(query_meta.description)
            search_datas.append(query_meta_list)
        return search_datas

    @staticmethod
    def get_all_project_and_format():
        query = ProjectManager.get_all_project()
        search_datas = ProjectManager.project_data_format(query)
        return search_datas


    @staticmethod
    def get_all_project():
        query = session.query(Project).order_by(desc(Project.id)).all()
        return query

    @staticmethod
    def updata_project(dic):
        item = session.query(Project).filter(Project.id == dic.get('id')).one()
        item.name = dic.get('name')
        item.search_id = dic.get('search_id')
        item.source_place = dic.get('source_place')
        item.main_designer = dic.get('main_designer')
        item.design_all = dic.get('design_all')
        item.responsible_man = dic.get('responsible_man')
        item.start_time = dic.get('start_time')
        item.end_time = dic.get('end_time')
        item.description = dic.get('description')
        session.add(item)
        session.commit()
        StaffManager.delete_staff_project_by_project_ids([item.id])
        StaffManager.add_staff_project(item.id, dic.get('attendee_ids'))

    @staticmethod
    def get_one_item_by_project_id(item_id):
        item = session.query(Project).filter(Project.id == item_id).one()
        return item

    @staticmethod
    def search_project_by_name(project_name):
        query_result = session.query(Project).filter(Project.name.like('%%%%%s%%%%' % project_name)).order_by(desc(Project.id)).all()
        search_datas = ProjectManager.project_data_format(query_result)
        return search_datas

    @staticmethod
    def search_project_by_date(**kwargs):
        except_q = session.query(Project).filter(
            or_(Project.start_time > kwargs.get('end_time'), Project.end_time < kwargs.get('start_time'))
        )
        query_result = session.query(Project).except_(except_q).order_by(desc(Project.id)).all()
        search_datas = ProjectManager.project_data_format(query_result)
        return search_datas


