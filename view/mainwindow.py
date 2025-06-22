import shutil
import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSlot
from qfluentwidgets import SplitFluentWindow, TeachingTipTailPosition, TeachingTipView, PushButton, TeachingTip, Dialog, \
    Flyout, InfoBarIcon, Slider
from view.Ui_Mainwindow import Ui_Mainwindow
from PyQt5.QtGui import QIcon, QDesktopServices, QPixmap
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PIL import Image
from PyQt5.QtCore import pyqtSignal

class Mainwindow(QWidget, Ui_Mainwindow):
    tipSingal = pyqtSignal()  # 定义弹出提示窗口的信号
    errotSingal = pyqtSignal()  # 定义弹出错误窗口的信号

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.tipSingal.connect(self.showTipDialog)
        self.errotSingal.connect(self.showErrorDialog)
        self.current_index = -1
        self.img_files = []
        self.selectmodel.setEnabled(False)
        self.PushButton.setEnabled(False)
        self.Slider.setEnabled(False)
        self.LineEdit.setEnabled(False)
        self.PrimaryPushButton.setEnabled(False)
        self.PrimaryPushButton_2.setEnabled(False)
        self.saved_images = {}
        self.selected_folder = ""
    def showTipDialog(self):
        title = '提示'
        content = """未选择任何文件夹，请重新选择"""
        w = Dialog(title, content, self)
        w.exec()

    def showErrorDialog(self):
        title = '错误'
        content = """文件夹中没有图片，请重新选择文件夹"""
        w = Dialog(title, content, self)
        w.exec()

    def showErrorDialog_exceed(self):
        Flyout.create(
            icon=InfoBarIcon.SUCCESS,
            title='提示',
            content='输入的数字超出边界',
            isClosable=True,
            parent=self,
            target=self.LineEdit
        )

    @pyqtSlot()
    def on_PushButton_2_clicked(self):
        start_path = 'I:/fiber_classfication'  # 替换为你想要的起始路径
        folder = QFileDialog.getExistingDirectory(self, "查看结果", start_path)
        if not folder:
            Flyout.create(
                icon=InfoBarIcon.SUCCESS,
                title='提示',
                content='不存在文件夹',
                isClosable=True,
                parent=self,
                target=self.PushButton_2
            )
            return

    @pyqtSlot()
    def on_selectimg_clicked(self):
        # 打开文件夹选择对话框
        # start_path = 'I:/wooldetectronV2/b7QMdiM'  # 替换为你想要的起始路径
        start_path = os.getcwd()
        folder = QFileDialog.getExistingDirectory(self, "选择图片文件夹", start_path)
        # todo:美化文件夹选择对话框 参考：FolderListDialog
        if not folder:
            self.tipSingal.emit()
            return
        self.selected_folder = folder  # 记录选择的路径
        self.image_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
        if len(self.image_files) == 0:
            self.errotSingal.emit()
            return
        else:
            self.Slider.setRange(0, len(self.image_files) - 1)
            self.current_index = 0
            self.update_slider()
            self.show_image()
            self.selectmodel.setEnabled(True)
            self.PushButton.setEnabled(True)
            self.Slider.setEnabled(True)
            self.LineEdit.setEnabled(True)
            self.PrimaryPushButton.setEnabled(True)
            self.PrimaryPushButton_2.setEnabled(True)

    def show_image(self):
        if 0 <= self.current_index < len(self.image_files):
            pixmap = QPixmap(self.image_files[self.current_index])
            # self.BodyLabel.setPixmap(pixmap.scaled(self.BodyLabel.size(), aspectRatioMode=True))
            # self.update_slider()  # 更新进度条
            # self.update_image_name_label()
            self.BodyLabel.setPixmap(pixmap)
            self.BodyLabel.resize(pixmap.size())
            self.update_slider()  # 更新进度条
            self.update_image_name_label()

    def update_slider(self):
        total = len(self.image_files)
        if total > 0:
            self.Slider.setValue(self.current_index)
            self.LineEdit.setText(f"{self.current_index + 1}/{total}")
        else:
            self.LineEdit.setText("0/0")

    @pyqtSlot()
    def on_selectmodel_clicked(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_image()
        else:
            Flyout.create(
                icon=InfoBarIcon.SUCCESS,
                title='提示',
                content='已经是第一张图片了哦',
                isClosable=True,
                parent=self,
                target=self.selectmodel
            )

    @pyqtSlot()
    def on_PushButton_clicked(self):
        if self.current_index < len(self.image_files) - 1:
            self.current_index += 1
            self.show_image()
        else:
            Flyout.create(
                icon=InfoBarIcon.SUCCESS,
                title='提示',
                content='已经是最后一张图片了哦',
                isClosable=True,
                parent=self,
                target=self.PushButton
            )

    @pyqtSlot()
    def on_Slider_valueChanged(self):
        value = self.Slider.value()
        if 0 <= value < len(self.image_files):
            self.current_index = value
            self.show_image()
        else:
            print("⚠️ 滑动超出范围")

    @pyqtSlot()
    def jump_to_image(self):
        index = int(self.LineEdit.text().split('/')[0]) - 1
        if 0 <= index < len(self.image_files):
            self.current_index = index
            self.show_image()
        else:
            self.showErrorDialog_exceed()

    @pyqtSlot()
    def on_PrimaryPushButton_clicked(self):
        self.save_image()
    @pyqtSlot()
    def on_PrimaryPushButton_2_clicked(self):
        self.on_PushButton_clicked()

    def save_image(self):
        # 获取当前图片路径
        if 0 <= self.current_index < len(self.image_files):
            current_image = self.image_files[self.current_index]
            current_image_name = os.path.basename(current_image)
            image_base, _ = os.path.splitext(current_image_name)

            json_file = os.path.join(self.selected_folder, image_base + ".json")

            # 构造 _dirty 目标文件夹路径
            parent_dir = os.path.dirname(self.selected_folder)
            dirty_folder_name = os.path.basename(self.selected_folder) + "_dirty"
            dirty_folder_path = os.path.join(parent_dir, dirty_folder_name)
            # 创建目标目录（如果不存在）
            if not os.path.exists(dirty_folder_path):
                os.makedirs(dirty_folder_path)
                print(f"📁 已创建目录: {dirty_folder_path}")
            # 移动图片
            try:
                shutil.move(current_image, os.path.join(dirty_folder_path, current_image_name))
                print(f"✅ 图片已移动: {current_image_name}")
            except Exception as e:
                print(f"❌ 移动图片失败: {e}")

            # 移动 JSON 文件（如果存在）
            if os.path.exists(json_file):
                try:
                    shutil.move(json_file, os.path.join(dirty_folder_path, os.path.basename(json_file)))
                    print(f"✅ JSON 文件已移动: {os.path.basename(json_file)}")
                except Exception as e:
                    print(f"❌ 移动 JSON 文件失败: {e}")
            else:
                print(f"⚠️ JSON 文件不存在: {json_file}")
            # 从 image_files 中移除已移动的图片
            self.image_files.pop(self.current_index)
            self.refresh_after_deletion()
            self.on_PushButton_clicked()

    def refresh_after_deletion(self):
        total = len(self.image_files)
        if total == 0:
            self.BodyLabel.clear()
            self.BodyLabel_2.setText("没有剩余图片")
            self.Slider.setEnabled(False)
            self.LineEdit.setText("0 / 0")
            return

        # 修正 current_index 防止越界
        if self.current_index >= total:
            self.current_index = total - 1
        self.current_index = self.current_index - 1
        # 更新滑动条范围和图像
        self.Slider.setRange(0, total - 1)
        self.show_image()

    def update_image_name_label(self):
        # 更新显示图片名称和保存状态
        if 0 <= self.current_index < len(self.image_files):
            current_image_name = os.path.basename(self.image_files[self.current_index])
            # if current_image_name in self.saved_images:
            #     self.BodyLabel_2.setText(f"{current_image_name} - 已保存到: {self.saved_images[current_image_name]}")
            # else:
            self.BodyLabel_2.setText(current_image_name)