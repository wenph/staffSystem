#coding=cp936
__author__ = 'admin'

from PyQt4 import QtGui
import re

class ToolsManager(object):
    @staticmethod
    def information_box(title, content):
        # ��������
        msgBox = QtGui.QMessageBox()
        msgBox.setIcon(QtGui.QMessageBox.Information)
        msgBox.setText(title)
        msgBox.setInformativeText(content)
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
        msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
        msgBox.exec_()

    @staticmethod
    def question_box(title, content):
        # �����Ի���
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
            ToolsManager.validate_data_not_null(u'����', kwargs_dic.get('name'))
            ToolsManager.validate_data_not_null(u'����', kwargs_dic.get('employee_id'))
            ToolsManager.validate_data_not_null(u'�ֻ�', kwargs_dic.get('phone_number'))
            ToolsManager.validate_data_is_number(u'�ֻ�', kwargs_dic.get('phone_number'))
            ToolsManager.validate_data_not_null(u'�绰', kwargs_dic.get('name'))
            ToolsManager.validate_data_not_null(u'��������', kwargs_dic.get('birth_date'))
            ToolsManager.validate_data_not_null(u'ְ��', kwargs_dic.get('title'))
            ToolsManager.validate_data_not_null(u'ѧ��', kwargs_dic.get('education'))
        elif obj == 'project':
            pass

    @staticmethod
    def validate_data_not_null(name, value):
        content = u'��������ȷ��%sֵ��' % name
        if value in (None, ''):
            ToolsManager.information_box(u'ע�⣡', content)

    @staticmethod
    def validate_data_is_number(name, value):
        content = u'��������ȷ��%sֵ��' % name
        if not re.match("^[0-9]+$", value):
            ToolsManager.information_box(u'ע�⣡', content)
