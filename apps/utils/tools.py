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
    def validate_data(obj, kwargs_dic):
        if obj == 'staff':
            ToolsManager.validate_data_not_null(u'姓名', kwargs_dic.get('name'))
            ToolsManager.validate_data_not_null(u'工号', kwargs_dic.get('employee_id'))
            ToolsManager.validate_data_not_null(u'手机', kwargs_dic.get('phone_number'))
            ToolsManager.validate_data_is_number(u'手机', kwargs_dic.get('phone_number'))
            ToolsManager.validate_data_not_null(u'电话', kwargs_dic.get('name'))
            ToolsManager.validate_data_not_null(u'出生日期', kwargs_dic.get('birth_date'))
            ToolsManager.validate_data_not_null(u'职称', kwargs_dic.get('title'))
            ToolsManager.validate_data_not_null(u'学历', kwargs_dic.get('education'))
        elif obj == 'project':
            pass

    @staticmethod
    def validate_data_not_null(name, value):
        content = u'请输入正确的%s值！' % name
        if value in (None, ''):
            ToolsManager.information_box(u'注意！', content)

    @staticmethod
    def validate_data_is_number(name, value):
        content = u'请输入正确的%s值！' % name
        if not re.match("^[0-9]+$", value):
            ToolsManager.information_box(u'注意！', content)
