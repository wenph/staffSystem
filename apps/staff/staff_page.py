#coding=utf-8
__author__ = 'admin'

from PyQt4 import QtGui, QtCore
from staff_models import User
from staff_manager import StaffManager
from apps.utils.tools import ToolsManager


class staff_tab(QtGui.QWidget):
    def __init__(self, parent=None):
        super(staff_tab, self).__init__(parent)

        # 查询区域的按钮
        addButton = QtGui.QPushButton("添加")
        deleteButton = QtGui.QPushButton("删除")
        updateButton = QtGui.QPushButton("更新")
        refreshButton = QtGui.QPushButton("刷新")
        allStaffButton = QtGui.QPushButton("所有人员")
        idleStaffButton = QtGui.QPushButton("闲置人员")

        grid = QtGui.QGridLayout()
        grid.addWidget(addButton, 1, 0)
        grid.addWidget(deleteButton, 1, 1)
        grid.addWidget(updateButton, 2, 0)
        grid.addWidget(refreshButton, 2, 1)

        searchHbox = QtGui.QHBoxLayout()
        searchHbox.addWidget(allStaffButton)
        searchHbox.addWidget(idleStaffButton)

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
        self.connect(addButton, QtCore.SIGNAL('clicked()'), self.my_table.add_staff)
        self.connect(refreshButton, QtCore.SIGNAL('clicked()'), self.my_table.refresh_staff)
        self.connect(deleteButton, QtCore.SIGNAL('clicked()'), self.my_table.delete_staff)
        self.connect(allStaffButton, QtCore.SIGNAL('clicked()'), self.my_table.refresh_staff)
        self.connect(updateButton, QtCore.SIGNAL('clicked()'), self.my_table.update_staff)

class MyTable(QtGui.QTableWidget):
    def __init__(self,parent=None):
        super(MyTable,self).__init__(parent)

        head_labels = ['ID', '姓名','工号','手机','出生年月','职称','学历','忙否','正在进行的项目','手里仪器','本月出差天数']
        self.setColumnCount(len(head_labels))
        self.setRowCount(0)
        self.setHorizontalHeaderLabels(head_labels)
        self.refresh_staff()

    def add_staff(self):
        dialog = Dialog()
        if dialog.exec_():
            dic = dialog.get_add_datas()
            user = User(**dic)
            StaffManager.add_staff(user)
            self.refresh_staff()
        dialog.destroy()

    def refresh_staff(self):
        search_datas = StaffManager.search_staff()
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
                j = j + 1
            i = i + 1

    def delete_staff(self):
        indexes = self.selectionModel().selectedRows()
        if len(indexes) == 0:
            ToolsManager.information_box("注意", "请选择一行或多行进行删除!")
        else:
            button = ToolsManager.question_box("提醒", "是否删除选中行？")
            if button == QtGui.QMessageBox.Ok:
                ids_list = []
                for index in sorted(indexes):
                    id_text = self.item(index.row(), 0).text()
                    ids_list.append(int(id_text))
                StaffManager.delete_staff(ids_list)
                self.refresh_staff()
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
            #dialog.birth_date_edit.setDateTime()
            dialog.title_edit.setText(staff_item.title)
            dialog.education_edit.setText(staff_item.education)
            if dialog.exec_():
                dic = dialog.get_add_datas()
                dic['id'] = int(id_text)
                StaffManager.updata_staff(dic)
                self.refresh_staff()
            dialog.destroy()
        else:
            # 弹出警告
            ToolsManager.information_box("注意", "请选择一行进行更新!")


class Dialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        #self.resize(240, 200)

        id_label = QtGui.QLabel('ID')
        name_label = QtGui.QLabel('姓名')
        employee_id_label = QtGui.QLabel('工号')
        phone_number_label = QtGui.QLabel('电话')
        birth_date_label = QtGui.QLabel('出生日期')
        title_label = QtGui.QLabel('职称')
        education_label = QtGui.QLabel('学历')
        is_busy_label = QtGui.QLabel('忙否')

        self.id_edit = QtGui.QLineEdit()
        self.name_edit = QtGui.QLineEdit()
        self.employee_id_edit = QtGui.QLineEdit()
        self.phone_number_edit = QtGui.QLineEdit()
        self.birth_date_edit = QtGui.QDateEdit(self)
        self.birth_date_edit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.birth_date_edit.setDisplayFormat("yyyy-MM-dd")
        self.birth_date_edit.setCalendarPopup(True)
        self.title_edit = QtGui.QLineEdit()
        self.education_edit = QtGui.QLineEdit()
        self.is_busy_edit = QtGui.QLineEdit()


        grid = QtGui.QGridLayout()
        #grid.setSpacing(10)

        grid.addWidget(name_label, 1, 0)
        grid.addWidget(self.name_edit, 1, 1)

        grid.addWidget(employee_id_label, 2, 0)
        grid.addWidget(self.employee_id_edit, 2, 1)

        grid.addWidget(phone_number_label, 3, 0)
        grid.addWidget(self.phone_number_edit, 3, 1)

        grid.addWidget(birth_date_label, 4, 0)
        grid.addWidget(self.birth_date_edit, 4, 1)

        grid.addWidget(title_label, 5, 0)
        grid.addWidget(self.title_edit, 5, 1)

        grid.addWidget(education_label, 6, 0)
        grid.addWidget(self.education_edit, 6, 1)

        self.setWindowTitle('添加')

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
        datas_dic['birth_date'] = unicode(self.birth_date_edit.text())
        datas_dic['title'] = unicode(self.title_edit.text())
        datas_dic['education'] = unicode(self.education_edit.text())
        return datas_dic
