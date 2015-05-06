#coding=cp936
__author__ = 'admin'

from PyQt4 import QtGui

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