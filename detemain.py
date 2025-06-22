import sys
import os
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox, QDesktopWidget
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme,
                            NavigationAvatarWidget, SplitFluentWindow, FluentTranslator)
from qfluentwidgets import FluentIcon as FIF


from view.mainwindow import Mainwindow
from view.Ui_Mainwindow import Ui_Mainwindow


class Mainwin(SplitFluentWindow, Ui_Mainwindow):
    def __init__(self):
        super(Mainwin, self).__init__()
        self.setWindowTitle('纤维检测项目')
        self.setWindowIcon(QIcon('resource/icon/shouye.png'))

        # 添加子界面
        self.mainwindow = Mainwindow(self)
        self.init_navigation()
        self.center()  # 调用自定义的居中方法

    def init_navigation(self):
        self.addSubInterface(self.mainwindow, FIF.SCROLL, '数据清洗')
        self.navigationInterface.setExpandWidth(280)

    def center(self):
        # 获取屏幕的矩形区域
        screen_geometry = QDesktopWidget().availableGeometry()
        # 获取窗口的矩形区域
        window_geometry = self.frameGeometry()
        # 将窗口的中心点设置为屏幕的中心点
        window_geometry.moveCenter(screen_geometry.center())
        # 将窗口的位置设置为新的几何区域的左上角
        self.move(window_geometry.topLeft())
