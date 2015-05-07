#coding=cp936
__author__ = 'admin'

import copy
from PyQt4 import QtGui, QtCore
from apps.db.db_models import Project
from project_manager import ProjectManager
from apps.utils.tools import ToolsManager
from apps.staff.staff_manager import StaffManager
from apps.utils import constant


class project_tab(QtGui.QWidget):
    def __init__(self, parent=None):
        super(project_tab, self).__init__(parent)

        # 查询区域的按钮
        addButton = QtGui.QPushButton(u"添加")
        deleteButton = QtGui.QPushButton(u"删除")
        updateButton = QtGui.QPushButton(u"更新")
        refreshButton = QtGui.QPushButton(u"刷新")

        grid = QtGui.QGridLayout()
        grid.addWidget(addButton, 1, 0)
        grid.addWidget(deleteButton, 1, 1)
        grid.addWidget(updateButton, 2, 0)
        grid.addWidget(refreshButton, 2, 1)

        searchHbox = QtGui.QHBoxLayout()

        editAreaHbox = QtGui.QHBoxLayout()
        #editAreaHbox.addStretch(1)
        editAreaHbox.addLayout(grid)
        editAreaHbox.addLayout(searchHbox)
        editAreaHbox.addStretch(1)

        vbox = QtGui.QVBoxLayout()
        self.my_table = MyTable()
        self.my_table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.my_table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        vbox.addLayout(editAreaHbox)
        vbox.addWidget(self.my_table)



        self.setLayout(vbox)

        self.setWindowTitle('box layout')
        self.connect(addButton, QtCore.SIGNAL('clicked()'), self.my_table.add_project)
        self.connect(refreshButton, QtCore.SIGNAL('clicked()'), self.my_table.refresh_project)
        self.connect(deleteButton, QtCore.SIGNAL('clicked()'), self.my_table.delete_project)
        self.connect(updateButton, QtCore.SIGNAL('clicked()'), self.my_table.update_project)

class MyTable(QtGui.QTableWidget):
    def __init__(self,parent=None):
        super(MyTable,self).__init__(parent)

        head_labels = constant.PROJECT_COLUMN
        self.setColumnCount(len(head_labels))
        self.setRowCount(0)
        self.setHorizontalHeaderLabels(head_labels)
        self.refresh_project()

    def add_project(self):
        dialog = Dialog()
        if dialog.exec_():
            dic = dialog.get_add_datas()
            attendee_ids = copy.deepcopy(dic['attendee_ids'])
            del dic['attendee_ids']
            user = Project(**dic)
            project = ProjectManager.add_project(user)
            StaffManager.add_staff_project(project.id, attendee_ids)
            self.refresh_project()
        dialog.destroy()

    def refresh_project(self):
        search_datas = ProjectManager.search_project()
        if len(search_datas) == 0:
            self.setRowCount(0)
        else:
            self.setRowCount(len(search_datas))
        i = 0
        for datas_meta in search_datas:
            j = 0
            for meta in datas_meta:
                newItem = QtGui.QTableWidgetItem(unicode(meta))
                self.setItem(i,j,newItem)
                j += 1
            i += 1

    def delete_project(self):
        indexes = self.selectionModel().selectedRows()
        if len(indexes) == 0:
            ToolsManager.information_box(u"注意", u"请选择一行或多行进行删除!")
        else:
            button = ToolsManager.question_box(u"提醒", u"是否删除选中行？")
            if button == QtGui.QMessageBox.Ok:
                ids_list = []
                for index in sorted(indexes):
                    id_text = self.item(index.row(), 0).text()
                    ids_list.append(int(id_text))
                ProjectManager.delete_project(ids_list)
                StaffManager.delete_staff_project_by_project_ids(ids_list)
                self.refresh_project()
            else:
                pass


    def update_project(self):
        indexes = self.selectionModel().selectedRows()
        if(len(indexes)) == 1:
            dialog = Dialog()
            id_text = self.item(indexes[0].row(), 0).text()
            project_item = ProjectManager.get_one_item_by_id(int(id_text))

            dialog.name_edit.setText(project_item.name)
            dialog.search_id_edit.setText(project_item.search_id)
            dialog.source_place_edit.setText(project_item.source_place)
            dialog.main_designer_edit.setText(project_item.main_designer)
            dialog.design_all_edit.setText(project_item.design_all)
            dialog.responsible_man_edit.setText(project_item.responsible_man)
            dialog.attendee_edit.setText(project_item.attendee)

            if dialog.exec_():
                dic = dialog.get_add_datas()
                dic['id'] = int(id_text)
                ProjectManager.updata_project(dic)
                self.refresh_project()
            dialog.destroy()
        else:
            # 弹出警告
            ToolsManager.information_box(u"注意", u"请选择一行进行更新!")


class Dialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        #self.resize(240, 200)

        id_label = QtGui.QLabel(u'ID')
        name_label = QtGui.QLabel(u'工程名称')
        search_id_label = QtGui.QLabel(u'检索号')
        source_place_label = QtGui.QLabel(u'来源')
        main_designer_label = QtGui.QLabel(u'主设人')
        design_all_label = QtGui.QLabel(u'设总')
        responsible_man_label = QtGui.QLabel(u'负责主工')
        attendee_label = QtGui.QLabel(u'参加人员')
        start_time_label = QtGui.QLabel(u'开始时间')
        end_time_label = QtGui.QLabel(u'结束时间')
        candidate_label = QtGui.QLabel(u'待选人员')

        self.id_edit = QtGui.QLineEdit()
        self.name_edit = QtGui.QLineEdit()
        self.search_id_edit = QtGui.QLineEdit()
        self.source_place_edit = QtGui.QLineEdit()
        self.main_designer_edit = QtGui.QLineEdit()
        self.design_all_edit = QtGui.QLineEdit()
        self.responsible_man_edit = QtGui.QLineEdit()
        self.attendee_edit = QtGui.QLineEdit()
        self.start_time_edit = QtGui.QDateEdit(self)
        self.start_time_edit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.start_time_edit.setDisplayFormat("yyyy-MM-dd")
        self.start_time_edit.setCalendarPopup(True)
        self.end_time_edit = QtGui.QDateEdit(self)
        self.end_time_edit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.end_time_edit.setDisplayFormat("yyyy-MM-dd")
        self.end_time_edit.setCalendarPopup(True)

        grid = QtGui.QGridLayout()
        #grid.setSpacing(10)

        grid.addWidget(name_label, 1, 0)
        grid.addWidget(self.name_edit, 1, 1)

        grid.addWidget(search_id_label, 2, 0)
        grid.addWidget(self.search_id_edit, 2, 1)

        grid.addWidget(source_place_label, 3, 0)
        grid.addWidget(self.source_place_edit, 3, 1)

        grid.addWidget(main_designer_label, 4, 0)
        grid.addWidget(self.main_designer_edit, 4, 1)

        grid.addWidget(design_all_label, 5, 0)
        grid.addWidget(self.design_all_edit, 5, 1)

        grid.addWidget(responsible_man_label, 6, 0)
        grid.addWidget(self.responsible_man_edit, 6, 1)

        #grid.addWidget(attendee_label, 7, 0)
        #grid.addWidget(self.attendee_edit, 7, 1)

        grid.addWidget(start_time_label, 8, 0)
        grid.addWidget(self.start_time_edit, 8, 1)

        grid.addWidget(end_time_label, 9, 0)
        grid.addWidget(self.end_time_edit, 9, 1)

        myBoxLayout = QtGui.QHBoxLayout()
        listWidgetALayout = QtGui.QVBoxLayout()
        listWidgetBLayout = QtGui.QVBoxLayout()

        self.listWidgetA = QtGui.QListWidget()
        self.listWidgetB = QtGui.QListWidget()
        self.addButton = QtGui.QPushButton()
        self.addButton.setText("-->")
        self.removeButton = QtGui.QPushButton()
        self.removeButton.setText("<--")

        buttonLayout = QtGui.QVBoxLayout()
        buttonLayout.addWidget(self.addButton)
        buttonLayout.addWidget(self.removeButton)
        staff_datas = StaffManager.search_staff()
        for i in range(len(staff_datas)):
            item = QtGui.QListWidgetItem(staff_datas[i][1])
            self.listWidgetA.addItem(item)

        listWidgetALayout.addWidget(candidate_label)
        listWidgetALayout.addWidget(self.listWidgetA)
        listWidgetBLayout.addWidget(attendee_label)
        listWidgetBLayout.addWidget(self.listWidgetB)
        myBoxLayout.addLayout(listWidgetALayout)
        myBoxLayout.addLayout(buttonLayout)
        myBoxLayout.addLayout(listWidgetBLayout)

        self.connect(self.addButton, QtCore.SIGNAL('clicked()'), self.add_fun)
        self.connect(self.removeButton, QtCore.SIGNAL('clicked()'), self.remove_fun)

        self.setWindowTitle(u'添加')

        # 创建ButtonBox，用户确定和取消
        buttonBox = QtGui.QDialogButtonBox()
        buttonBox.setOrientation(QtCore.Qt.Horizontal) # 设置为水平方向
        buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok) # 确定和取消两个按钮
        # 连接信号和槽
        buttonBox.accepted.connect(self.accept) # 确定
        buttonBox.rejected.connect(self.reject) # 取消

        # 垂直布局，布局表格及按钮
        layout = QtGui.QVBoxLayout()

        # 加入前面创建的表格布局
        layout.addLayout(grid)
        layout.addLayout(myBoxLayout)

        # 放一个间隔对象美化布局
        #spacerItem = QtGui.QSpacerItem(20, 48, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        #layout.addItem(spacerItem)

        # ButtonBox
        layout.addWidget(buttonBox)

        self.setLayout(layout)


    def get_add_datas(self):
        datas_dic = {}
        datas_dic['name'] = unicode(self.name_edit.text())
        datas_dic['search_id'] = unicode(self.search_id_edit.text())
        datas_dic['source_place'] = unicode(self.source_place_edit.text())
        datas_dic['main_designer'] = unicode(self.main_designer_edit.text())
        datas_dic['design_all'] = unicode(self.design_all_edit.text())
        datas_dic['responsible_man'] = unicode(self.responsible_man_edit.text())
        datas_dic['start_time'] = unicode(self.start_time_edit.text())
        datas_dic['end_time'] = unicode(self.end_time_edit.text())
        attendee_ids = ''
        attendee_names = ''
        for row_num in range(self.listWidgetB.count()):
            row_text = unicode(self.listWidgetB.item(row_num).text())
            staff = StaffManager.get_one_item_by_name(row_text)
            staff_id = staff.id
            staff_name = staff.name
            attendee_ids += str(staff_id) + ","
            attendee_names += staff_name + ","

        datas_dic['attendee_ids'] = attendee_ids.rstrip(',')
        datas_dic['attendee'] = attendee_names.rstrip(',')
        return datas_dic

    def add_fun(self):
        if len(self.listWidgetA.selectedItems()) == 1:
            row_num = self.listWidgetA.row(self.listWidgetA.currentItem())
            currentItem = self.listWidgetA.item(row_num).text()
            self.listWidgetB.addItem(currentItem)
            self.listWidgetA.takeItem(row_num)
        else:
            ToolsManager.information_box(u"注意", u"请选择一个待选人员!")

    def remove_fun(self):
        if len(self.listWidgetB.selectedItems()) == 1:
            row_num = self.listWidgetB.row(self.listWidgetB.currentItem())
            currentItem = self.listWidgetB.item(row_num).text()
            self.listWidgetA.addItem(currentItem)
            self.listWidgetB.takeItem(row_num)
        else:
            ToolsManager.information_box(u"注意", u"请选择一个参加人员!")