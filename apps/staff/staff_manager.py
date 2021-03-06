#coding=cp936
__author__ = 'admin'

import datetime
import copy
from apps.db.db_models import User, UserProject, Project
from apps.db.db_session import session
from apps.utils.tools import ToolsManager
from sqlalchemy import and_, or_, except_, desc
from apps.utils import constant

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
    def search_all_staff():
        '''
        展示所有员工信息
        '''
        query = StaffManager.get_all_staff()
        search_datas = []
        for query_meta in query:
            query_meta_list = []
            query_meta_list.append(query_meta.id)
            query_meta_list.append(query_meta.name)
            query_meta_list.append(query_meta.employee_id)
            query_meta_list.append(query_meta.phone_number)
            query_meta_list.append(query_meta.tel_number)
            query_meta_list.append(query_meta.birth_date)
            query_meta_list.append(query_meta.title)
            query_meta_list.append(query_meta.position)
            query_meta_list.append(query_meta.education)
            project_str = StaffManager.search_project_by_user_id_and_now(query_meta.id)
            query_meta_list.append(project_str)
            para = copy.deepcopy(constant.ONE_MONTH_TIME)
            para['name'] = query_meta.name
            outing_days, staff_data = StaffManager.calculate_outing_info(**para)
            query_meta_list.append(outing_days)
            query_meta_list.append(query_meta.description)
            search_datas.append(query_meta_list)
        return search_datas

    @staticmethod
    def search_idle_staff():
        '''
        展示在位（未出差）员工信息
        '''
        query = StaffManager.get_all_staff()
        search_datas = []
        for query_meta in query:
            query_meta_list = []
            query_meta_list.append(query_meta.id)
            query_meta_list.append(query_meta.name)
            query_meta_list.append(query_meta.employee_id)
            query_meta_list.append(query_meta.phone_number)
            query_meta_list.append(query_meta.tel_number)
            query_meta_list.append(query_meta.birth_date)
            query_meta_list.append(query_meta.title)
            query_meta_list.append(query_meta.position)
            query_meta_list.append(query_meta.education)
            project_str = StaffManager.search_project_by_user_id_and_now(query_meta.id)
            query_meta_list.append(project_str)
            para = copy.deepcopy(constant.ONE_MONTH_TIME)
            para['name'] = query_meta.name
            outing_days, staff_data = StaffManager.calculate_outing_info(**para)
            query_meta_list.append(outing_days)
            query_meta_list.append(query_meta.description)
            if project_str == '':  # 闲置人员
                search_datas.append(query_meta_list)
        return search_datas


    @staticmethod
    def get_all_staff():
        query_result = session.query(User).order_by(User.id).all()
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
        item.description = dic.get('description')
        session.add(item)
        session.commit()

    @staticmethod
    def get_one_item_by_user_id(user_id):
        item = session.query(User).filter(User.id == user_id).one()
        return item

    @staticmethod
    def get_one_item_by_user_name(item_name):
        try:
            item = session.query(User).filter(User.name == item_name).one()
            return item
        except:
            return None

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
        session.query(UserProject).\
            filter(and_(UserProject.user_id == user_id, UserProject.project_id == project_id)).delete()

    @staticmethod
    def search_staff_project_by_staff_name_and_data(**kwargs):
        search_datas = []
        staff = StaffManager.get_one_item_by_user_name(kwargs.get('name'))
        if staff not in (None, ''):
            query_result = session.query(UserProject).filter(UserProject.user_id == staff.id).\
                order_by(desc(UserProject.project_id)).all()
            for query_meta in query_result:
                if query_meta.project.start_time > kwargs.get('end_time') \
                    or query_meta.project.end_time < kwargs.get('start_time'):
                    pass
                else:
                    search_data_meta = []
                    search_data_meta.append(query_meta.user.name)
                    search_data_meta.append(query_meta.project.name)
                    search_data_meta.append(query_meta.project.start_time)
                    search_data_meta.append(query_meta.project.end_time)
                    staff_str = StaffManager.search_staff_by_project_id(query_meta.project.id)
                    search_data_meta.append(staff_str)
                    search_datas.append(search_data_meta)
        return search_datas

    @staticmethod
    def search_staff_by_project_id(project_id):
        staff_str = ''
        query_result = session.query(UserProject).filter(UserProject.project_id == project_id).\
            order_by(UserProject.user_id).all()
        for query_meta in query_result:
            staff_str += query_meta.user.name + ','
        if staff_str != '':
            staff_str = staff_str[:-1]              # 去掉最后一个逗号
        return staff_str

    @staticmethod
    def search_project_by_user_id_and_now(user_id):
        project_str = ''
        today = datetime.date.today()
        para = {
            "start_time": today,
            "end_time": today
        }
        from apps.project.project_manager import ProjectManager
        project_search_datas = ProjectManager.search_project_by_date(**para)
        for project_search_data in project_search_datas:
            project_user_search_datas = session.query(UserProject).\
                filter(and_(UserProject.project_id == project_search_data[0], UserProject.user_id == user_id)).\
                order_by(desc(UserProject.project_id)).all()
            if len(project_user_search_datas) != 0:
                for project_user_search_data in project_user_search_datas:
                    project_str += project_user_search_data.project.name + ','
        if project_str != '':
            project_str = project_str[:-1]
        return project_str

    @staticmethod
    def calculate_outing_info(**kwargs):
        '''
        计算出差时间
        '''
        outing_days = 0
        start_time = kwargs.get('start_time')
        end_time = kwargs.get('end_time')
        search_datas = StaffManager.search_staff_project_by_staff_name_and_data(**kwargs)
        for data in search_datas:
            project_st = data[2]
            project_et = data[3]
            if project_st <= start_time:
                if project_et <= end_time:
                    days = (project_et - start_time).days + 1
                    outing_days += days
                elif project_et > end_time:
                    days = (end_time - start_time).days + 1
                    outing_days += days
            elif project_st > start_time:
                if project_et <= end_time:
                    days = (project_et - project_st).days + 1
                    outing_days += days
                elif project_et > end_time:
                    days = (end_time - project_st).days + 1
                    outing_days += days
        for data in search_datas:
            data.append(outing_days)
        return outing_days, search_datas