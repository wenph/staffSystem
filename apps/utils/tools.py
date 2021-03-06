#coding=cp936
__author__ = 'admin'

from PyQt4 import QtGui
import re

class ToolsManager(object):
    @staticmethod
    def information_box(title, content):
        # 弹出警告
        msgBox = QtGui.QMessageBox()
        msgBox.setIcon(QtGui.QMessageBox.Information)
        msgBox.setText(title)
        msgBox.setInformativeText(content)
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
        msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
        msgBox.exec_()

    @staticmethod
    def question_box(title, content):
        # 弹出对话框
        msgBox = QtGui.QMessageBox()
        msgBox.setIcon(QtGui.QMessageBox.Question)
        msgBox.setText(title)
        msgBox.setInformativeText(content)
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
        return msgBox.exec_()

    @staticmethod
    def validate_data(which, obj, kwargs_dic):
        result = True
        if which == 'staff':
            obj.is_name_correct_label.setVisible(False)
            obj.is_employee_id_correct_label.setVisible(False)
            obj.is_phone_number_correct_label.setVisible(False)
            obj.is_tel_number_correct_label.setVisible(False)
            if ToolsManager.validate_data_is_null(kwargs_dic.get('name')):
                obj.is_name_correct_label.setVisible(True)
                result = False
            if ToolsManager.validate_data_is_null(kwargs_dic.get('employee_id')):
                obj.is_employee_id_correct_label.setVisible(True)
                result = False
            if ToolsManager.validate_data_is_null(kwargs_dic.get('phone_number')):
                obj.is_phone_number_correct_label.setVisible(True)
                result = False
            if ToolsManager.validate_data_is_not_number(kwargs_dic.get('phone_number')):
                obj.is_phone_number_correct_label.setVisible(True)
                result = False
            if ToolsManager.validate_data_is_null(kwargs_dic.get('tel_number')):
                obj.is_tel_number_correct_label.setVisible(True)
                result = False
        elif which == 'project':
            obj.is_name_correct_label.setVisible(False)
            obj.is_search_id_correct_label.setVisible(False)
            obj.is_main_designer_correct_label.setVisible(False)
            obj.is_design_all_correct_label.setVisible(False)
            obj.is_responsible_man_correct_label.setVisible(False)
            obj.is_end_time_correct_label.setVisible(False)
            if ToolsManager.validate_data_is_null(kwargs_dic.get('name')):
                obj.is_name_correct_label.setVisible(True)
                result = False
            if ToolsManager.validate_data_is_null(kwargs_dic.get('search_id')):
                obj.is_search_id_correct_label.setVisible(True)
                result = False
            if ToolsManager.validate_data_is_null(kwargs_dic.get('main_designer')):
                obj.is_main_designer_correct_label.setVisible(True)
                result = False
            if ToolsManager.validate_data_is_null(kwargs_dic.get('design_all')):
                obj.is_design_all_correct_label.setVisible(True)
                result = False
            if ToolsManager.validate_data_is_null(kwargs_dic.get('responsible_man')):
                obj.is_responsible_man_correct_label.setVisible(True)
                result = False
            if kwargs_dic.get('end_time') < kwargs_dic.get('start_time'):
                obj.is_end_time_correct_label.setVisible(True)
                result = False
        return result

    @staticmethod
    def validate_data_is_null(value):
        if value in (None, ''):
            return True

    @staticmethod
    def validate_data_is_not_number(value):
        if not re.match("^[0-9]+$", value):
            return True
