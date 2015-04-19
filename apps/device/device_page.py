#coding=utf-8
__author__ = 'admin'

import sys
from PyQt4 import QtGui, QtCore, QtWebKit


class device_tab(QtGui.QWidget):
    def __init__(self, parent=None):
        super(device_tab, self).__init__(parent)

        okButton = QtGui.QPushButton("OK")
        self.connect(okButton, QtCore.SIGNAL('clicked()'), self.insert_data_into_tab)
        cancelButton = QtGui.QPushButton("Cancel")

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)

        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        self.my_table = MyTable()
        vbox.addWidget(self.my_table)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.setWindowTitle('box layout')

    def insert_data_into_tab(self):
        self.my_table.insert_data_into_table()


class MyTable(QtGui.QTableWidget):
    def __init__(self,parent=None):
        super(MyTable,self).__init__(parent)
        column_num = 7
        row_num = 2
        self.setColumnCount(column_num)
        self.setRowCount(row_num)
        self.setHorizontalHeaderLabels(['SUN','MON','TUE','WED','THU','FIR','SAT'])
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                cnt = '(%d,%d)谁谁谁水水水水谁谁谁'% (i,j)
                newItem = QtGui.QTableWidgetItem(cnt)
                self.setItem(i,j,newItem)
        #self.setItem(0,0,QtGui.QTableWidgetItem(self.tr("性别")))
        #self.setItem(0,1,QtGui.QTableWidgetItem(self.tr("姓名")))
        #self.setItem(0,2,QtGui.QTableWidgetItem(self.tr("出生日期")))
        #self.setItem(0,3,QtGui.QTableWidgetItem(self.tr("职业")))
        #self.setItem(0,4,QtGui.QTableWidgetItem(self.tr("收入")))
        #lbp1=QtGui.QLabel()
        #lbp1.setPixmap(QtGui.QPixmap("image/4.gif"))
        #self.setCellWidget(1,0,lbp1)
        #twi1=QtGui.QTableWidgetItem("Tom")
        #self.setItem(1,1,twi1)
        #dte1=QtGui.QDateTimeEdit()
        #dte1.setDateTime(QtCore.QDateTime.currentDateTime())
        #dte1.setDisplayFormat("yyyy/mm/dd")
        #dte1.setCalendarPopup(True)
        #self.setCellWidget(1,2,dte1)
        #cbw=QtGui.QComboBox()
        #cbw.addItem("Worker")
        #cbw.addItem("Famer")
        #cbw.addItem("Doctor")
        #cbw.addItem("Lawyer")
        #cbw.addItem("Soldier")
        #self.setCellWidget(1,3,cbw)
        #sb1=QtGui.QSpinBox()
        #sb1.setRange(1000,10000)
        #self.setCellWidget(1,4,sb1)
    def insert_data_into_table(self):
        lastrow = self.rowCount()
        self.insertRow(lastrow+1)