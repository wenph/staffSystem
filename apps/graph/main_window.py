#coding=utf-8
__author__ = 'admin'

import sys
from PyQt4 import QtGui
from apps.staff.staff_page import staff_tab
from apps.project.project_page import project_tab
from apps.device.device_page import device_tab

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.centralWidget = QtGui.QWidget()
        screen = QtGui.QDesktopWidget().screenGeometry()
        self.resize(screen.width(), screen.height())            # 窗口最大化
        #self.resize(800, 500)
        self.setWindowTitle('人员项目管理系统')
        self.statusBar().showMessage('Ready')

        vbox = QtGui.QVBoxLayout()

        self.tabs_widget = QtGui.QTabWidget()
        self.tabs_widget.blockSignals(True)            # just for not showing the initial message
        self.tabs_widget.currentChanged.connect(self.onChange)      # changed!
        vbox.addWidget(self.tabs_widget, 1)

        qwidget1 = staff_tab()
        qwidget2 = project_tab()
        qwidget3 = device_tab()
        self.tabs_widget.addTab(qwidget1, "人员管理")
        self.tabs_widget.addTab(qwidget2, "工程管理")
        self.tabs_widget.addTab(qwidget3, "仪器管理")

        #qwidget1.
        self.centralWidget.setLayout(vbox)
        self.setCentralWidget(self.centralWidget)

        self.tabs_widget.blockSignals(False)           # now listen the currentChanged signal

    def onChange(self, i):
        print i

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())