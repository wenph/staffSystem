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

        # ��ѯ����İ�ť
        addButton = QtGui.QPushButton(u"�����Ŀ")
        deleteButton = QtGui.QPushButton(u"ɾ����Ŀ")
        updateButton = QtGui.QPushButton(u"������Ŀ")
        allProjectButton = QtGui.QPushButton(u"������Ŀ")
        name_label = QtGui.QLabel(u'��Ŀ����')
        self.name_edit = QtGui.QLineEdit()
        name_list = [unicode(query.name) for query in ProjectManager.get_all_project()]
        name_str = QtCore.QStringList(name_list)             #Ԥ�������ֵ�
        self.name_edit.setCompleter(QtGui.QCompleter(name_str))          # ���ֵ���ӵ�lineEdit��
        start_time_label = QtGui.QLabel(u'��ʼ����')
        self.start_time_edit = QtGui.QDateEdit(self)
        self.start_time_edit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.start_time_edit.setDisplayFormat("yyyy-MM-dd")
        self.start_time_edit.setCalendarPopup(True)
        self.end_time_edit = QtGui.QDateEdit(self)
        self.end_time_edit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.end_time_edit.setDisplayFormat("yyyy-MM-dd")
        self.end_time_edit.setCalendarPopup(True)
        end_time_label = QtGui.QLabel(u'��ֹ����')
        searchNameButton = QtGui.QPushButton(u"����������")
        searchDateButton = QtGui.QPushButton(u"����������")

        searchVbox = QtGui.QVBoxLayout()
        searchHbox1 = QtGui.QHBoxLayout()
        searchHbox1.addWidget(name_label)
        searchHbox1.addWidget(self.name_edit)
        searchHbox1.addWidget(searchNameButton)
        searchHbox1.addWidget(start_time_label)
        searchHbox1.addWidget(self.start_time_edit)
        searchHbox1.addWidget(end_time_label)
        searchHbox1.addWidget(self.end_time_edit)
        searchHbox1.addWidget(searchDateButton)
        searchHbox1.addStretch(1)
        searchHbox1.addWidget(addButton)
        searchHbox1.addWidget(deleteButton)
        searchHbox1.addWidget(updateButton)
        searchHbox1.addWidget(allProjectButton)
        searchVbox.addLayout(searchHbox1)

        editAreaHbox = QtGui.QHBoxLayout()
        editAreaHbox.addLayout(searchVbox)
        # editAreaHbox.addStretch(1)

        vbox = QtGui.QVBoxLayout()
        self.my_table = MyTable()
        self.my_table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.my_table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        vbox.addLayout(editAreaHbox)
        vbox.addWidget(self.my_table)

        self.setLayout(vbox)

        self.setWindowTitle('box layout')
        self.connect(addButton, QtCore.SIGNAL('clicked()'), self.my_table.add_project)
        self.connect(deleteButton, QtCore.SIGNAL('clicked()'), self.my_table.delete_project)
        self.connect(updateButton, QtCore.SIGNAL('clicked()'), self.my_table.update_project)
        self.connect(allProjectButton, QtCore.SIGNAL('clicked()'), self.my_table.all_project)
        self.connect(searchNameButton, QtCore.SIGNAL('clicked()'), self.search_project_by_name)
        self.connect(searchDateButton, QtCore.SIGNAL('clicked()'), self.search_project_by_date)

    def search_project_by_name(self):
        project_name = unicode(self.name_edit.text())
        if project_name not in (None, ''):
            search_datas = ProjectManager.search_project_by_name(project_name)
            self.my_table.refresh_project(search_datas)
        else:
            ToolsManager.information_box(u'ע��', u'����д��Ŀ����������')

    def search_project_by_date(self):
        para = {
            'start_time': self.start_time_edit.date().toPyDate(),
            'end_time': self.end_time_edit.date().toPyDate()
        }
        if para['end_time'] < para['start_time']:
            ToolsManager.information_box(u'ע��', u'��ʼ����Ӧ��С����ֹ���ڣ�')
        else:
            search_datas = ProjectManager.search_project_by_date(**para)
            self.my_table.refresh_project(search_datas)


class MyTable(QtGui.QTableWidget):
    def __init__(self,parent=None):
        super(MyTable,self).__init__(parent)

        head_labels = constant.PROJECT_COLUMN
        self.setColumnCount(len(head_labels))
        self.setRowCount(0)
        self.setHorizontalHeaderLabels(head_labels)
        search_datas = ProjectManager.get_all_project_and_format()
        self.refresh_project(search_datas)

    def add_project(self):
        dialog = Dialog()
        staff_data_list = StaffManager.search_idle_staff()
        for staff in staff_data_list:
            dialog.listWidgetA.addItem(QtGui.QListWidgetItem(staff[1]))
        if dialog.exec_():
            dic = dialog.get_add_datas()
            attendee_ids = copy.deepcopy(dic['attendee_ids'])
            del dic['attendee_ids']
            project = Project(**dic)
            project = ProjectManager.add_project(project)
            StaffManager.add_staff_project(project.id, attendee_ids)
            search_datas = ProjectManager.get_all_project_and_format()
            self.refresh_project(search_datas)
            dialog.destroy()

    def refresh_project(self, search_datas):
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
            ToolsManager.information_box(u"ע��", u"��ѡ��һ�л���н���ɾ��!")
        else:
            button = ToolsManager.question_box(u"����", u"�Ƿ�ɾ��ѡ���У�")
            if button == QtGui.QMessageBox.Ok:
                ids_list = []
                for index in sorted(indexes):
                    id_text = self.item(index.row(), 0).text()
                    ids_list.append(int(id_text))
                ProjectManager.delete_project(ids_list)
                StaffManager.delete_staff_project_by_project_ids(ids_list)
                search_datas = ProjectManager.get_all_project_and_format()
                self.refresh_project(search_datas)
            else:
                pass


    def update_project(self):
        indexes = self.selectionModel().selectedRows()
        if(len(indexes)) == 1:
            dialog = Dialog()
            id_text = self.item(indexes[0].row(), 0).text()
            project_item = ProjectManager.get_one_item_by_project_id(int(id_text))

            dialog.name_edit.setText(project_item.name)
            dialog.search_id_edit.setText(project_item.search_id)
            dialog.source_place_edit.setCurrentIndex(dialog.source_place_edit.findText(project_item.source_place))
            dialog.main_designer_edit.setText(project_item.main_designer)
            dialog.design_all_edit.setText(project_item.design_all)
            dialog.responsible_man_edit.setText(project_item.responsible_man)
            dialog.start_time_edit.setDate(project_item.start_time)
            dialog.end_time_edit.setDate(project_item.end_time)
            dialog.description_edit.setText(project_item.description)
            dialog.name_edit.setReadOnly(True)
            staff_str = StaffManager.search_staff_by_project_id(project_item.id)
            if staff_str == '':         # ��Ŀ��û��
                staff_data_list = StaffManager.search_idle_staff()
                for staff in staff_data_list:
                    dialog.listWidgetA.addItem(staff[1])            # "1"���б�ĵ������ֶ�
            else:
                staff_name_list = staff_str.split(',')
                for staff_name in staff_name_list:
                    dialog.listWidgetB.addItem(staff_name)
                staff_data_list = StaffManager.search_idle_staff()
                for staff in staff_data_list:
                    if staff[1] not in staff_name_list:
                        dialog.listWidgetA.addItem(staff[1])

            if dialog.exec_():
                dic = dialog.get_add_datas()
                dic['id'] = int(id_text)
                ProjectManager.updata_project(dic)
                search_datas = ProjectManager.get_all_project_and_format()
                self.refresh_project(search_datas)
                dialog.destroy()
        else:
            # ��������
            ToolsManager.information_box(u"ע��", u"��ѡ��һ�н��и���!")

    def all_project(self):
        search_datas = ProjectManager.get_all_project_and_format()
        self.refresh_project(search_datas)


class Dialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        #self.resize(240, 200)

        id_label = QtGui.QLabel(u'ID')
        name_label = QtGui.QLabel(u'��������')
        self.is_name_correct_label = QtGui.QLabel(u'����д��ȷ�Ĺ������ƣ�')
        self.is_name_correct_label.setVisible(False)
        search_id_label = QtGui.QLabel(u'������')
        self.is_search_id_correct_label = QtGui.QLabel(u'����д��ȷ�ļ����ţ�')
        self.is_search_id_correct_label.setVisible(False)
        source_place_label = QtGui.QLabel(u'��Դ')
        main_designer_label = QtGui.QLabel(u'������')
        self.is_main_designer_correct_label = QtGui.QLabel(u'����д��ȷ�������ˣ�')
        self.is_main_designer_correct_label.setVisible(False)
        design_all_label = QtGui.QLabel(u'����')
        self.is_design_all_correct_label = QtGui.QLabel(u'����д��ȷ�����ܣ�')
        self.is_design_all_correct_label.setVisible(False)
        responsible_man_label = QtGui.QLabel(u'��������')
        self.is_responsible_man_correct_label = QtGui.QLabel(u'����д��ȷ�ĸ���������')
        self.is_responsible_man_correct_label.setVisible(False)
        start_time_label = QtGui.QLabel(u'��ʼʱ��')
        end_time_label = QtGui.QLabel(u'����ʱ��')
        self.is_end_time_correct_label = QtGui.QLabel(u'����ʱ�䲻��С�ڿ�ʼʱ�䣡')
        self.is_end_time_correct_label.setVisible(False)
        description_label = QtGui.QLabel(u'��ע')
        candidate_label = QtGui.QLabel(u'��ѡ��Ա')
        attendee_label = QtGui.QLabel(u'�μ���Ա')

        self.id_edit = QtGui.QLineEdit()
        self.name_edit = QtGui.QLineEdit()
        self.search_id_edit = QtGui.QLineEdit()
        self.source_place_edit = QtGui.QComboBox()
        for source_place in constant.SOURCE_PLACE_NAME_LIST:
            self.source_place_edit.addItem(source_place)
        self.main_designer_edit = QtGui.QLineEdit()
        self.design_all_edit = QtGui.QLineEdit()
        self.responsible_man_edit = QtGui.QLineEdit()
        self.attendee_edit = QtGui.QLineEdit()
        self.start_time_edit = QtGui.QDateEdit()
        self.start_time_edit.setDate(QtCore.QDate.currentDate())
        self.start_time_edit.setDisplayFormat("yyyy-MM-dd")
        self.start_time_edit.setCalendarPopup(True)
        self.end_time_edit = QtGui.QDateEdit()
        self.end_time_edit.setDate(QtCore.QDate.currentDate())
        self.end_time_edit.setDisplayFormat("yyyy-MM-dd")
        self.end_time_edit.setCalendarPopup(True)
        self.description_edit = QtGui.QLineEdit()

        grid = QtGui.QGridLayout()
        #grid.setSpacing(10)
        count = 1
        grid.addWidget(name_label, count, 0)
        grid.addWidget(self.name_edit, count, 1)
        grid.addWidget(self.is_name_correct_label, count, 2)
        count += 1
        grid.addWidget(search_id_label, count, 0)
        grid.addWidget(self.search_id_edit, count, 1)
        grid.addWidget(self.is_search_id_correct_label, count, 2)
        count += 1
        grid.addWidget(source_place_label, count, 0)
        grid.addWidget(self.source_place_edit, count, 1)
        count += 1
        grid.addWidget(main_designer_label, count, 0)
        grid.addWidget(self.main_designer_edit, count, 1)
        grid.addWidget(self.is_main_designer_correct_label, count, 2)
        count += 1
        grid.addWidget(design_all_label, count, 0)
        grid.addWidget(self.design_all_edit, count, 1)
        grid.addWidget(self.is_design_all_correct_label, count, 2)
        count += 1
        grid.addWidget(responsible_man_label, count, 0)
        grid.addWidget(self.responsible_man_edit, count, 1)
        grid.addWidget(self.is_responsible_man_correct_label, count, 2)
        count += 1
        grid.addWidget(start_time_label, count, 0)
        grid.addWidget(self.start_time_edit, count, 1)
        count += 1
        grid.addWidget(end_time_label, count, 0)
        grid.addWidget(self.end_time_edit, count, 1)
        grid.addWidget(self.is_end_time_correct_label, count, 2)
        count += 1
        grid.addWidget(description_label, count, 0)
        grid.addWidget(self.description_edit, count, 1)


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

        listWidgetALayout.addWidget(candidate_label)
        listWidgetALayout.addWidget(self.listWidgetA)
        listWidgetBLayout.addWidget(attendee_label)
        listWidgetBLayout.addWidget(self.listWidgetB)
        myBoxLayout.addLayout(listWidgetALayout)
        myBoxLayout.addLayout(buttonLayout)
        myBoxLayout.addLayout(listWidgetBLayout)

        self.connect(self.addButton, QtCore.SIGNAL('clicked()'), self.add_fun)
        self.connect(self.removeButton, QtCore.SIGNAL('clicked()'), self.remove_fun)

        self.setWindowTitle(u'���')

        # ����ButtonBox���û�ȷ����ȡ��
        buttonBox = QtGui.QDialogButtonBox()
        buttonBox.setOrientation(QtCore.Qt.Horizontal) # ����Ϊˮƽ����
        buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok) # ȷ����ȡ��������ť
        # �����źźͲ�
        #buttonBox.accepted.connect(self.accept) # ȷ��
        buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.accept_fun)
        buttonBox.rejected.connect(self.reject) # ȡ��

        # ��ֱ���֣����ֱ�񼰰�ť
        layout = QtGui.QVBoxLayout()

        # ����ǰ�洴���ı�񲼾�
        layout.addLayout(grid)
        layout.addLayout(myBoxLayout)

        # ��һ�����������������
        #spacerItem = QtGui.QSpacerItem(20, 48, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        #layout.addItem(spacerItem)

        # ButtonBox
        layout.addWidget(buttonBox)

        self.setLayout(layout)


    def get_add_datas(self):
        datas_dic = {}
        datas_dic['name'] = unicode(self.name_edit.text())
        datas_dic['search_id'] = unicode(self.search_id_edit.text())
        datas_dic['source_place'] = unicode(self.source_place_edit.currentText())
        datas_dic['main_designer'] = unicode(self.main_designer_edit.text())
        datas_dic['design_all'] = unicode(self.design_all_edit.text())
        datas_dic['responsible_man'] = unicode(self.responsible_man_edit.text())
        datas_dic['start_time'] = self.start_time_edit.date().toPyDate()
        datas_dic['end_time'] = self.end_time_edit.date().toPyDate()
        datas_dic['description'] = unicode(self.description_edit.text())
        attendee_ids = ''
        attendee_names = ''
        for row_num in range(self.listWidgetB.count()):
            row_text = unicode(self.listWidgetB.item(row_num).text())
            staff = StaffManager.get_one_item_by_user_name(row_text)
            staff_id = staff.id
            staff_name = staff.name
            attendee_ids += str(staff_id) + ","
            attendee_names += staff_name + ","

        datas_dic['attendee_ids'] = attendee_ids.rstrip(',')
        return datas_dic

    def add_fun(self):
        if len(self.listWidgetA.selectedItems()) == 1:
            row_num = self.listWidgetA.row(self.listWidgetA.currentItem())
            currentItem = self.listWidgetA.item(row_num).text()
            self.listWidgetB.addItem(currentItem)
            self.listWidgetA.takeItem(row_num)
        else:
            ToolsManager.information_box(u"ע��", u"��ѡ��һ����ѡ��Ա!")

    def remove_fun(self):
        if len(self.listWidgetB.selectedItems()) == 1:
            row_num = self.listWidgetB.row(self.listWidgetB.currentItem())
            currentItem = self.listWidgetB.item(row_num).text()
            self.listWidgetA.addItem(currentItem)
            self.listWidgetB.takeItem(row_num)
        else:
            ToolsManager.information_box(u"ע��", u"��ѡ��һ���μ���Ա!")

    def accept_fun(self):
        dic = self.get_add_datas()
        success = ToolsManager.validate_data('project', self, dic)
        if success:
            self.accept()