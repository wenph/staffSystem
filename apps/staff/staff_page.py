#coding=cp936
__author__ = 'admin'

from PyQt4 import QtGui, QtCore
from apps.db.db_models import User, UserProject
from staff_manager import StaffManager
from apps.utils.tools import ToolsManager
from apps.utils import constant


class staff_tab(QtGui.QWidget):
    def __init__(self, parent=None):
        super(staff_tab, self).__init__(parent)

        # 查询区域的按钮
        self.addButton = QtGui.QPushButton(u"添加人员")
        self.deleteButton = QtGui.QPushButton(u"删除人员")
        self.updateButton = QtGui.QPushButton(u"更新人员")
        self.allStaffButton = QtGui.QPushButton(u"所有人员")
        self.idleStaffButton = QtGui.QPushButton(u"此刻闲置人员")
        name_label = QtGui.QLabel(u'姓名')
        self.name_edit = QtGui.QLineEdit()
        name_list = [unicode(query.name) for query in StaffManager.get_all_staff()]
        name_str = QtCore.QStringList(name_list)             #预先设置字典
        self.name_edit.setCompleter(QtGui.QCompleter(name_str))          # 将字典添加到lineEdit中
        start_time_label = QtGui.QLabel(u'起始日期')
        self.start_time_edit = QtGui.QDateEdit(self)
        self.start_time_edit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.start_time_edit.setDisplayFormat("yyyy-MM-dd")
        self.start_time_edit.setCalendarPopup(True)
        self.end_time_edit = QtGui.QDateEdit(self)
        self.end_time_edit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.end_time_edit.setDisplayFormat("yyyy-MM-dd")
        self.end_time_edit.setCalendarPopup(True)
        end_time_label = QtGui.QLabel(u'终止日期')
        searchButton = QtGui.QPushButton(u"搜索")

        searchVbox = QtGui.QVBoxLayout()
        searchHbox1 = QtGui.QHBoxLayout()
        searchHbox1.addWidget(name_label)
        searchHbox1.addWidget(self.name_edit)
        searchHbox1.addWidget(start_time_label)
        searchHbox1.addWidget(self.start_time_edit)
        searchHbox1.addWidget(end_time_label)
        searchHbox1.addWidget(self.end_time_edit)
        searchHbox1.addWidget(searchButton)
        searchHbox1.addStretch(1)
        searchHbox1.addWidget(self.addButton)
        searchHbox1.addWidget(self.deleteButton)
        searchHbox1.addWidget(self.updateButton)

        searchHbox1.addWidget(self.allStaffButton)
        searchHbox1.addWidget(self.idleStaffButton)
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
        self.connect(self.addButton, QtCore.SIGNAL('clicked()'), self.my_table.add_staff)
        self.connect(self.deleteButton, QtCore.SIGNAL('clicked()'), self.my_table.delete_staff)
        self.connect(self.allStaffButton, QtCore.SIGNAL('clicked()'), self.show_all_staff)
        self.connect(self.updateButton, QtCore.SIGNAL('clicked()'), self.my_table.update_staff)
        self.connect(self.idleStaffButton, QtCore.SIGNAL('clicked()'), self.show_all_staff)
        searchButton.clicked.connect(lambda: self.collect_data())

    def collect_data(self):
        para = {
            'name': unicode(self.name_edit.text()),
            'start_time': self.start_time_edit.date().toPyDate(),
            'end_time': self.end_time_edit.date().toPyDate()
        }
        if para['name'] in (None, '') or para['end_time'] < para['start_time']:
            if para['name'] in (None, ''):
                ToolsManager.information_box(u'注意', u'请填写姓名再搜索！')
            if para['end_time'] < para['start_time']:
                ToolsManager.information_box(u'注意', u'起始日期应该小于终止日期！')
        else:
            self.addButton.setVisible(False)
            self.deleteButton.setVisible(False)
            self.updateButton.setVisible(False)
            self.my_table.search_staff_by_name_and_date(**para)

    def show_all_staff(self):
        self.addButton.setVisible(True)
        self.deleteButton.setVisible(True)
        self.updateButton.setVisible(True)
        self.my_table.get_and_show_all_staff()



class MyTable(QtGui.QTableWidget):
    def __init__(self,parent=None):
        super(MyTable,self).__init__(parent)
        head_labels = constant.STAFF_COLUMN
        self.setColumnCount(len(head_labels))
        self.setRowCount(0)
        self.setHorizontalHeaderLabels(head_labels)
        search_datas = StaffManager.search_staff()
        self.refresh_staff(search_datas)

    def add_staff(self):
        dialog = Dialog()
        if dialog.exec_():
            dic = dialog.get_add_datas()
            user = User(**dic)
            StaffManager.add_staff(user)
            search_datas = StaffManager.search_staff()
            self.refresh_staff(search_datas)
            dialog.destroy()

    def refresh_staff(self, search_datas):
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

    def delete_staff(self):
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
                StaffManager.delete_staff(ids_list)
                StaffManager.delete_staff_project_by_staff_ids(ids_list)
                search_datas = StaffManager.search_staff()
                self.refresh_staff(search_datas)
            else:
                pass


    def update_staff(self):
        indexes = self.selectionModel().selectedRows()
        if(len(indexes)) == 1:
            dialog = Dialog()
            id_text = self.item(indexes[0].row(), 0).text()
            staff_item = StaffManager.get_one_item_by_id(int(id_text))
            dialog.name_edit.setText(staff_item.name)
            dialog.employee_id_edit.setText(staff_item.employee_id)
            dialog.phone_number_edit.setText(staff_item.phone_number)
            dialog.tel_number_edit.setText(staff_item.tel_number)
            dialog.birth_date_edit.setDate(staff_item.birth_date)
            dialog.title_edit.setCurrentIndex(dialog.title_edit.findText(staff_item.title))
            dialog.position_edit.setCurrentIndex(dialog.position_edit.findText(staff_item.position))
            dialog.education_edit.setCurrentIndex(dialog.education_edit.findText(staff_item.education))
            dialog.name_edit.setReadOnly(True)
            if dialog.exec_():
                dic = dialog.get_add_datas()
                dic['id'] = int(id_text)
                StaffManager.updata_staff(dic)
                search_datas = StaffManager.search_staff()
                self.refresh_staff(search_datas)
                dialog.destroy()
        else:
            # 弹出警告
            ToolsManager.information_box(u"注意", u"请选择一行进行更新!")

    def search_staff_by_name_and_date(self, **kwargs):
        search_datas = StaffManager.search_staff_project_by_staff_name_and_data(**kwargs)
        head_labels = constant.STAFF_SEARCH_COLUMN
        self.setColumnCount(len(head_labels))
        self.setHorizontalHeaderLabels(head_labels)
        self.refresh_staff(search_datas)

    def get_and_show_all_staff(self):
        search_datas = StaffManager.search_staff()
        head_labels = constant.STAFF_COLUMN
        self.setColumnCount(len(head_labels))
        self.setHorizontalHeaderLabels(head_labels)
        self.refresh_staff(search_datas)

class Dialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        #self.resize(240, 200)

        id_label = QtGui.QLabel(u'ID')
        name_label = QtGui.QLabel(u'姓名')
        self.is_name_correct_label = QtGui.QLabel(u'请填写正确的姓名！')
        self.is_name_correct_label.setVisible(False)
        employee_id_label = QtGui.QLabel(u'工号')
        self.is_employee_id_correct_label = QtGui.QLabel(u'请填写正确的工号！')
        self.is_employee_id_correct_label.setVisible(False)
        phone_number_label = QtGui.QLabel(u'手机')
        self.is_phone_number_correct_label = QtGui.QLabel(u'请填写正确的手机！')
        self.is_phone_number_correct_label.setVisible(False)
        tel_number_label = QtGui.QLabel(u'电话')
        self.is_tel_number_correct_label = QtGui.QLabel(u'请填写正确的电话！')
        self.is_tel_number_correct_label.setVisible(False)
        birth_date_label = QtGui.QLabel(u'出生日期')
        title_label = QtGui.QLabel(u'职称')
        position_label = QtGui.QLabel(u'职位')
        education_label = QtGui.QLabel(u'学历')

        self.id_edit = QtGui.QLineEdit()
        self.name_edit = QtGui.QLineEdit()
        self.employee_id_edit = QtGui.QLineEdit()
        self.phone_number_edit = QtGui.QLineEdit()
        self.tel_number_edit = QtGui.QLineEdit()
        self.birth_date_edit = QtGui.QDateEdit()
        self.birth_date_edit.setDate(QtCore.QDate.currentDate())
        self.birth_date_edit.setDisplayFormat("yyyy-MM-dd")
        self.birth_date_edit.setCalendarPopup(True)
        self.title_edit = QtGui.QComboBox()
        for title in constant.TITLE_NAME_LIST:
            self.title_edit.addItem(title)
        self.education_edit = QtGui.QComboBox()
        self.position_edit = QtGui.QComboBox()
        for position in constant.POSITION_NAME_LIST:
            self.position_edit.addItem(position)
        self.education_edit = QtGui.QComboBox()
        for education in constant.EDUCATION_NAME_LIST:
            self.education_edit.addItem(education)
        self.is_busy_edit = QtGui.QLineEdit()


        grid = QtGui.QGridLayout()
        #grid.setSpacing(10)
        count = 1
        grid.addWidget(name_label, count, 0)
        grid.addWidget(self.name_edit, count, 1)
        grid.addWidget(self.is_name_correct_label, count, 2)
        count += 1
        grid.addWidget(employee_id_label, count, 0)
        grid.addWidget(self.employee_id_edit, count, 1)
        grid.addWidget(self.is_employee_id_correct_label, count, 2)
        count += 1
        grid.addWidget(phone_number_label, count, 0)
        grid.addWidget(self.phone_number_edit, count, 1)
        grid.addWidget(self.is_phone_number_correct_label, count, 2)
        count += 1
        grid.addWidget(tel_number_label, count, 0)
        grid.addWidget(self.tel_number_edit, count, 1)
        grid.addWidget(self.is_tel_number_correct_label, count, 2)
        count += 1
        grid.addWidget(birth_date_label, count, 0)
        grid.addWidget(self.birth_date_edit, count, 1)
        count += 1
        grid.addWidget(title_label, count, 0)
        grid.addWidget(self.title_edit, count, 1)
        count += 1
        grid.addWidget(position_label, count, 0)
        grid.addWidget(self.position_edit, count, 1)
        count += 1
        grid.addWidget(education_label, count, 0)
        grid.addWidget(self.education_edit, count, 1)

        self.setWindowTitle(u'添加')

        # 创建ButtonBox，用户确定和取消
        buttonBox = QtGui.QDialogButtonBox()
        buttonBox.setOrientation(QtCore.Qt.Horizontal) # 设置为水平方向
        buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok) # 确定和取消两个按钮
        # 连接信号和槽
        # buttonBox.accepted.connect(self.accept) # 确定
        buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.accept_fun)
        buttonBox.rejected.connect(self.reject) # 取消

        # 垂直布局，布局表格及按钮
        layout = QtGui.QVBoxLayout()

        # 加入前面创建的表格布局
        layout.addLayout(grid)

        # 放一个间隔对象美化布局
        #spacerItem = QtGui.QSpacerItem(20, 48, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        #layout.addItem(spacerItem)

        # ButtonBox
        layout.addWidget(buttonBox)

        self.setLayout(layout)


    def get_add_datas(self):
        datas_dic = {}
        datas_dic['name'] = unicode(self.name_edit.text())
        datas_dic['employee_id'] = unicode(self.employee_id_edit.text())
        datas_dic['phone_number'] = unicode(self.phone_number_edit.text())
        datas_dic['tel_number'] = unicode(self.tel_number_edit.text())
        datas_dic['birth_date'] = self.birth_date_edit.date().toPyDate()
        datas_dic['title'] = unicode(self.title_edit.currentText())
        datas_dic['position'] = unicode(self.position_edit.currentText())
        datas_dic['education'] = unicode(self.education_edit.currentText())
        return datas_dic

    def accept_fun(self):
        dic = self.get_add_datas()
        success_data = ToolsManager.validate_data('staff', self, dic)
        if success_data:
            self.accept()
