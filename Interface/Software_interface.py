# -*- encoding:utf-8 -*-
"""
@作者：刘锐
@文件名：QTPY.py
@时间：2019/11/11  12:37
@文档说明:
"""

import os
import sys
import time
import pickle
import threading
import Mail_delivery as e
from globalvar import globalvar
from Data_processing import Data_processing
from Interface import ExtendedComboBox
from Interface import Search
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QFont, QBrush
from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QApplication, QTableWidget, QHeaderView,
                             QGridLayout, QTableWidgetItem, QLineEdit,
                             QFileDialog, QCheckBox, QMessageBox, QMenu, QInputDialog)

def File_creation(path):
    isExists = os.path.exists(path)  # 判断是否存在这个文件夹
    if not isExists:  # 如果不存在则创建
        os.makedirs(path)

def Pickles(path, data, judge):
    if judge == 'dump':
        with open(path, "wb") as file:  #
            pickle.dump(data, file)
    elif judge == "read":
        with open(path, "rb") as file:  #
            Data = pickle.load(file)
        return Data

class Qtmainwin(QWidget):
    """
        Qtwindows类
    """

    def __init__(self):
        super().__init__()
        self.Create_database = None
        self.Data_analysis = None
        self.btn2 = None
        self.initUI()
        self.setUI()

    def initUI(self):
        """
            initUI为窗口方法
        """
        self.setWindowTitle("数据分析")  # 设定窗口名字
        self.setWindowIcon(QIcon("Icon/Main.ico"))  # 指定图标
        self.setWindowOpacity(0.9)  # 透明度
        palette = QPalette()  # 设置背景颜色
        palette.setColor(QPalette.Background, Qt.black)  # 颜色设置
        self.setPalette(palette)  # 主窗口设置颜色为white
        desktop = QApplication.desktop()  # 获取显示器分辨率大小
        screenRect = desktop.screenGeometry()
        height = screenRect.height()
        width = screenRect.width()
        self.setMinimumSize(QSize(width / 2, height / 2))
        self.setMaximumSize(QSize(width / 2, height / 2))

        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("Icon/timg.jpg")))
        # palette.setColor(QPalette.Background,Qt.red)
        self.setPalette(palette)
        self.show()  # 启动最大化

    def setUI(self):
        self.Create_database = QPushButton("创建数据库")
        self.Create_database.setFixedSize(150, 80)  # 设置按钮大小
        icon = QIcon()
        icon.addPixmap(QPixmap("./Icon/Create_database.png"), QIcon.Normal, QIcon.Off)  # 选择图标
        self.Create_database.setIcon(icon)  # 设置图标
        self.Create_database.setIconSize(QSize(80, 80))  # 设置图标大小

        self.Data_analysis = QPushButton("数据分析")
        self.Data_analysis.setFixedSize(150, 80)  # 设置按钮大小
        icon = QIcon()
        icon.addPixmap(QPixmap("./Icon/Data_analysis.png"), QIcon.Normal, QIcon.Off)  # 选择图标
        self.Data_analysis.setIcon(icon)  # 设置图标
        self.Data_analysis.setIconSize(QSize(80, 80))  # 设置图标大小

        grid = QGridLayout()  # 创建了一个网格布局
        self.setLayout(grid)  # 设置窗口的布局界面
        # grid.setSpacing(2)  # 即各控件之间的上下间距为10（以像素为单位）。同理还有grid.setMargin（int）为设置控件之间的左右间距。
        grid.addWidget(self.Create_database, 0, 0, 1, 1)
        grid.addWidget(self.Data_analysis, 0, 1, 1, 1)

class Database_class(QWidget):
    """
        Qtwindows类
    """

    def __init__(self, Main):
        super().__init__()
        self.main = Main
        self.data = None  # 处理后数据的显示
        self.Process_information = None  # 实时处理进度
        self.Folder_selection = None
        self.Selector_button = None  # 数据库的选择按钮
        self.Selector_button1 = None
        self.Folder_selection_textbox = None
        self.Data_loading = None
        self.Search_text = None
        self.Data_processing_mode = None
        self.Line_processing = None
        self.First_column_data = None
        self.Second_column_data = None
        self.Dispose = None
        self.fname = ""  # 文件夹选择
        self.Characteristic = None
        self.Characteristic_textbox = None
        self.First_Characteristic = None
        self.First_Characteristic_textbox = None
        self.Second_Characteristic = None
        self.Second_Characteristic_textbox = None
        self.grid = None
        self.Library_choose = None
        self.Search_file = None
        self.Selector_button2 = None
        self.End_number = 0
        self.Multiple_key = list()

    def initUI(self):
        """
            initUI为窗口方法
        """
        self.setWindowTitle("创建数据库")  # 设定窗口名字
        self.setWindowIcon(QIcon("Icon/Main.ico"))  # 指定图标
        palette = QPalette()  # 设置背景颜色
        palette.setColor(QPalette.Background, Qt.white)  # 颜色设置
        self.setPalette(palette)  # 主窗口设置颜色为white
        self.showMaximized()  # 启动最大化
        self.setUI()
        self.main.Create_database.setEnabled(False)  # 设置不可用状态.

    def setUI(self):
        self.Folder_selection = QLabel("数据选择")
        self.Folder_selection.setFont(QFont("宋体", 11, QFont.Bold))  # 设置字体
        self.Folder_selection_textbox = QLineEdit()  # 建立文本框
        self.Selector_button = QPushButton("选择")
        self.Selector_button.clicked.connect(self.Database_loading)

        self.Characteristic = QLabel("特征字符")
        self.Characteristic.setFont(QFont("宋体", 11, QFont.Bold))  # 设置字体
        self.Characteristic_textbox = QLineEdit()  # 建立文本框


        self.First_Characteristic = QLabel("一列特征")
        self.First_Characteristic.setFont(QFont("宋体", 11, QFont.Bold))  # 设置字体
        self.First_Characteristic_textbox = QLineEdit()  # 建立文本框

        self.Second_Characteristic = QLabel("二列特征")
        self.Second_Characteristic.setFont(QFont("宋体", 11, QFont.Bold))  # 设置字体
        self.Second_Characteristic_textbox = QLineEdit()  # 建立文本框

        self.data = QTableWidget(0, 1)
        # self.data.setColumnWidth(0, 140)  # 设置行的宽度
        # self.data.setColumnWidth(1, 800)
        # self.data.setRowHeight(0, 5)  # 设置列的高度
        # self.data.setRowHeight(1, 5)
        self.data.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 使所有表格充满行
        # self.data.verticalHeader().setVisible(False)  # 表格头的隐藏
        self.data.setHorizontalHeaderLabels(['详情'])  # 设置水平方向的表头标签
        self.data.setContextMenuPolicy(Qt.CustomContextMenu)  #设置允许右键创建
        self.data.customContextMenuRequested.connect(self.generateMenu)  # 设置右键函数

        self.Process_information = QTableWidget(0, 1)
        self.Process_information.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 使所有表格充满行
        self.Process_information.verticalHeader().setVisible(False)  # 表格头的隐藏
        self.Process_information.setHorizontalHeaderLabels(['数据处理进度'])  # 设置水平方向的表头标签

        self.Library_choose = QLabel("库选择")
        self.Library_choose.setFont(QFont("Roman times", 11, QFont.Bold))  # 设置字体
        self.Search_file = ExtendedComboBox.ExtendedComboBox()  # 自定义的文本搜素框
        self.Search_file.setFont(QFont("Roman times", 11))  # 字体加粗self.Selector_button = QPushButton("选择")
        self.Search_file.activated.connect(self.Display_file)  # 设置选择下拉选项后显示文件
        Database_path =  "./数据库/"
        fileList = os.listdir(Database_path)  # 将目录中的数据库文件夹全部加入列表
        self.Search_file.addItems(fileList)

        self.Data_loading = QLabel("数据加载")
        self.Data_loading.setFont(QFont("Roman times", 11, QFont.Bold))  # 设置字体
        self.Search_text = ExtendedComboBox.ExtendedComboBox()  # 自定义的文本搜素框
        self.Search_text.setFont(QFont("Roman times", 11))  # 字体加粗self.Selector_button = QPushButton("选择")
        self.Selector_button1 = QPushButton("加载")
        self.Selector_button1.clicked.connect(self.Data_display)
        # self.Selector_button1.clicked.connect(self.Data_type)

        self.Data_processing_mode = QLabel("数据处理模式")
        self.Data_processing_mode.setFont(QFont("Roman times", 11, QFont.Bold))  # 设置字体
        self.Line_processing = QCheckBox("整行处理")
        self.First_column_data = QCheckBox("一列处理")
        self.Second_column_data = QCheckBox("二列处理")
        self.Line_processing.toggle()  # 默认复选框启用
        self.First_column_data.toggle()  # 默认复选框启用
        self.Second_column_data.toggle()  # 默认复选框启用
        self.Dispose = QPushButton("处理数据")
        self.Dispose.clicked.connect(self.Processing_data_function)

        self.grid = QGridLayout()  # 创建了一个网格布局
        self.setLayout(self.grid)  # 设置窗口的布局界面
        self.grid.addWidget(self.Folder_selection, 0, 0, 1, 2, Qt.AlignCenter | Qt.AlignLeft)
        self.grid.addWidget(self.Folder_selection_textbox, 0, 1, 1, 3)
        self.grid.addWidget(self.Selector_button, 0, 4, 1, 1, Qt.AlignTop | Qt.AlignLeft)

        self.grid.addWidget(self.Characteristic, 1, 0, 1, 2, Qt.AlignCenter | Qt.AlignLeft)
        self.grid.addWidget(self.Characteristic_textbox, 1, 1, 1, 3)

        self.grid.addWidget(self.First_Characteristic, 2, 0, 1, 2, Qt.AlignCenter | Qt.AlignLeft)
        self.grid.addWidget(self.First_Characteristic_textbox, 2, 1, 1, 3)

        self.grid.addWidget(self.Second_Characteristic, 3, 0, 1, 2, Qt.AlignCenter | Qt.AlignLeft)
        self.grid.addWidget(self.Second_Characteristic_textbox, 3, 1, 1, 3)

        self.grid.addWidget(self.Data_processing_mode, 4, 0, 1, 1, Qt.AlignCenter | Qt.AlignLeft)
        self.grid.addWidget(self.Line_processing, 4, 1, 1, 1, Qt.AlignCenter | Qt.AlignLeft)
        self.grid.addWidget(self.First_column_data, 4, 2, 1, 1, Qt.AlignCenter | Qt.AlignLeft)
        self.grid.addWidget(self.Second_column_data, 4, 3, 1, 1, Qt.AlignCenter | Qt.AlignLeft)
        self.grid.addWidget(self.Dispose, 4, 4, 1, 1, Qt.AlignCenter | Qt.AlignLeft)



        self.grid.addWidget(self.data, 0, 6, 15, 15)
        self.grid.addWidget(self.Process_information, 5, 0, 8, 5)

        self.grid.addWidget(self.Library_choose, 13, 0, 1, 2)
        self.grid.addWidget(self.Search_file, 13, 1, 1, 3)

        self.grid.addWidget(self.Data_loading, 14, 0, 1, 2)
        self.grid.addWidget(self.Search_text, 14, 1, 1, 3)
        self.grid.addWidget(self.Selector_button1, 14, 4, 1, 1, Qt.AlignTop | Qt.AlignLeft)

    def Database_loading(self):
        global Result
        self.fname = QFileDialog.getExistingDirectory(self, "选择文件夹")
        self.Folder_selection_textbox.setText(self.fname)  # 将路径设置到文本中
        if len(self.fname) <= 0:
            return 0
        globalvar.set_value("Database_file", self.fname)  # 将数据库的文件路径加入全局变量中
        Result = Data_processing.Line_analysis()  # 返回文件夹中文件列表[0]，数据处理判断位[1]，整行长度[2]，一列长度[3]，二列长度[4]，预判特征字符[5][6][7]
        if Result == (0, 0, 0, 0, 0, 0, 0, 0):
            return False
        if Result[1] == 1:  # 如果是没有逗号的数据
            self.Characteristic_textbox.setText(Result[5])  # 将没有分隔符时的特征字符放入到文本中
            self.First_Characteristic_textbox.setReadOnly(True)  # 将其设置为不可编辑
            self.Second_Characteristic_textbox.setReadOnly(True)  # 将其设置为不可编辑
        if Result[1] == 2:  # 如果是没有逗号的数据
            self.First_Characteristic_textbox.setText(Result[6])  # 将没有分隔符时的特征字符放入到文本中
            self.Second_Characteristic_textbox.setText(Result[7])  # 将没有分隔符时的特征字符放入到文本中
            self.Characteristic_textbox.setReadOnly(True)  # 将其设置为不可编辑
        if Result[1] == 3:  # 如果是没有逗号的数据
            self.First_Characteristic_textbox.setText(Result[6])  # 将没有分隔符时的特征字符放入到文本中
            self.Second_Characteristic_textbox.setText(Result[7])  # 将没有分隔符时的特征字符放入到文本中
            self.Characteristic_textbox.setReadOnly(True)  # 将其设置为不可编辑

    def Processing_data_function(self):
        if len(self.fname) <= 0:
            return 0
        Single_data = dict()
        First_data = dict()
        Second_data = dict()

        Line_length_error = list()
        First_length_error = list()
        Second_length_error = list()

        Repeated_code_error = dict()
        First_Repeated_code_error = dict()
        Second_Repeated_code_error = dict()

        Public_substring_error = list()
        First_Public_substring_error = list()
        Second_Public_substring_error = list()

        rowPosition = self.Process_information.rowCount()
        # 这句是关键！ range(0, rowPosition)[::-1] 逆序循环
        for rP in range(0, rowPosition)[::-1]:
            self.Process_information.removeRow(rP)

        # 返回文件夹中文件列表[0]，数据处理判断位[1]，整行长度[2]，一列长度[3]，二列长度[4]，预判特征字符[5][6][7]
        # fileList, Data_processing_judgment, Line_length, First_length, Second_length, Public_substring, First_Public_substring, Second_Public_substring
        fileList, Data_processing_judgment, Line_length, First_length, Second_length, \
        Public_substring, First_Public_substring, Second_Public_substring = Result

        Public_substring = self.Characteristic_textbox.text()  # 获取特征字符
        First_Public_substring = self.First_Characteristic_textbox.text()  # 获取特征字符
        Second_Public_substring = self.Second_Characteristic_textbox.text()
        # 由于是没有逗号的数据，所以将数据处理模式屏蔽
        if Data_processing_judgment == 1:  # 如果是没有逗号的数据
            for file in fileList:
                path = self.fname + "/" + file
                if Data_processing.Single_processing(path, file, Line_length, Public_substring, Single_data,
                                                     Line_length_error, Repeated_code_error, Public_substring_error):
                                                     # 文件路径，文件名，字符长度，特征字符，去重字典,长度错误，重码错误，特征错误
                    text = file + "  数据处理完成"
                    i = self.Process_information.rowCount()  # 获取当前行数
                    self.Process_information.insertRow(i)  # 在当前行数下插入一行
                    newItem = QTableWidgetItem("%s" % text)  # 写入数据
                    self.Process_information.setItem(i, 0, newItem)
                    self.Process_information.verticalScrollBar().setValue(self.Process_information.maximumHeight())
                    QApplication.processEvents()
                else:
                    QMessageBox.warning(None, "严重错误", "(%s)文件读取失败因为该文件的编码格式不对，请将格式改为UTF-8或ANSI"
                                        % file, QMessageBox.Yes)
                    return False

            path1 = "./数据库/%s/" % self.fname.split("/")[-1]  # 当前数据库的文件名
            File_creation(path1)  # 判断文件夹是否存在并建立文件夹
            path2 = path1 + "整体去重数据"
            Pickles(path2, Single_data, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
            path2 = path1 + "整体长度不符数据"
            Pickles(path2, Line_length_error, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
            path2 = path1 + "整体重码数据"
            Pickles(path2, Repeated_code_error, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
            path2 = path1 + "整体特征不符数据"
            Pickles(path2, Public_substring_error, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
            QMessageBox.information(self, "消息提示", "数据库创建完成")

        if Data_processing_judgment == 2:

            if self.Line_processing.isChecked():
                for file in fileList:
                    path = self.fname + "/" + file
                    if Data_processing.Double_Entirety_processing(path, file, Line_length, Single_data,
                                                                  Line_length_error,
                                                                  Repeated_code_error):
                        # 文件路径，文件名，字符长度，特征字符，去重字典,长度错误，重码错误，特征错误
                        text = file + "  数据处理完成"
                        i = self.Process_information.rowCount()  # 获取当前行数
                        self.Process_information.insertRow(i)  # 在当前行数下插入一行
                        newItem = QTableWidgetItem("%s" % text)  # 写入数据
                        self.Process_information.setItem(i, 0, newItem)
                        self.Process_information.verticalScrollBar().setValue(self.Process_information.maximumHeight())
                        QApplication.processEvents()
                    else:
                        QMessageBox.warning(None, "严重错误", "(%s)文件读取失败因为该文件的编码格式不对，请将格式改为UTF-8或ANSI"
                                            % file, QMessageBox.Yes)
                        return False

            if self.First_column_data.isChecked():
                start = time.perf_counter()
                Data_processing.Double_First_processing(Single_data, First_length, First_length_error, First_Public_substring,
                                                        First_data, First_Public_substring_error, First_Repeated_code_error)
                end = time.perf_counter()
                text = "一列数据处理完成,耗时%s秒" %(int((end - start) * 1000) / 1000)
                i = self.Process_information.rowCount()  # 获取当前行数
                self.Process_information.insertRow(i)  # 在当前行数下插入一行
                newItem = QTableWidgetItem("%s" % text)  # 写入数据
                self.Process_information.setItem(i, 0, newItem)
                self.Process_information.verticalScrollBar().setValue(self.Process_information.maximumHeight())
                QApplication.processEvents()
            if self.Second_column_data.isChecked():
                start = time.perf_counter()
                Data_processing.Double_Second_processing(First_data, Second_length, Second_length_error, Second_Public_substring,
                                                     Second_data, Second_Public_substring_error, Second_Repeated_code_error)
                end = time.perf_counter()
                text = "一列数据处理完成,耗时%s秒" %(int((end - start) * 1000) / 1000)
                i = self.Process_information.rowCount()  # 获取当前行数
                self.Process_information.insertRow(i)  # 在当前行数下插入一行
                newItem = QTableWidgetItem("%s" % text)  # 写入数据
                self.Process_information.setItem(i, 0, newItem)
                self.Process_information.verticalScrollBar().setValue(self.Process_information.maximumHeight())
                QApplication.processEvents()

            path1 = "./数据库/%s/" % self.fname.split("/")[-1]  # 当前数据库的文件名
            File_creation(path1)  # 判断文件夹是否存在并建立文件夹
            path2 = path1 + "整体去重数据"
            Pickles(path2, Single_data, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
            path2 = path1 + "整体长度不符数据"
            Pickles(path2, Line_length_error, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
            path2 = path1 + "整体重码数据"
            Pickles(path2, Repeated_code_error, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作

            path2 = path1 + "一列去重数据"
            Pickles(path2, First_data, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
            path2 = path1 + "一列长度不符数据"
            Pickles(path2, First_length_error, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
            path2 = path1 + "一列重码数据"
            Pickles(path2, First_Repeated_code_error, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
            path2 = path1 + "一列特征不符数据"
            Pickles(path2, First_Public_substring_error, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作

            path2 = path1 + "二列去重数据"
            Pickles(path2, Second_data, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
            path2 = path1 + "二列长度不符数据"
            Pickles(path2, Second_length_error, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
            path2 = path1 + "二列重码数据"
            Pickles(path2, Second_Repeated_code_error, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
            path2 = path1 + "二列特征不符数据"
            Pickles(path2, Second_Public_substring_error, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作

            QMessageBox.information(self, "消息提示", "数据库创建完成")

        if Data_processing_judgment == 3:

            if self.Line_processing.isChecked():
                for file in fileList:
                    path = self.fname + "/" + file
                    if Data_processing.Three_Entirety_processing(path, file, Line_length, Single_data,
                                                                 Line_length_error,
                                                                 Repeated_code_error):
                        # 文件路径，文件名，字符长度，特征字符，去重字典,长度错误，重码错误，特征错误
                        text = file + "  整体数据处理完成"
                        i = self.Process_information.rowCount()  # 获取当前行数
                        self.Process_information.insertRow(i)  # 在当前行数下插入一行
                        newItem = QTableWidgetItem("%s" % text)  # 写入数据
                        self.Process_information.setItem(i, 0, newItem)
                        self.Process_information.verticalScrollBar().setValue(self.Process_information.maximumHeight())
                        QApplication.processEvents()
                    else:
                        QMessageBox.warning(None, "严重错误", "(%s)文件读取失败因为该文件的编码格式不对，请将格式改为UTF-8或ANSI"
                                            % file, QMessageBox.Yes)
                        return False

            if self.First_column_data.isChecked():
                start = time.perf_counter()
                Data_processing.Three_First_processing(Single_data, First_length, First_length_error,
                                                    First_Public_substring,
                                                    First_data, First_Public_substring_error, First_Repeated_code_error)
                end = time.perf_counter()
                text = "一列数据处理完成,耗时%ss" %(int((end - start) * 1000) / 1000)
                i = self.Process_information.rowCount()  # 获取当前行数
                self.Process_information.insertRow(i)  # 在当前行数下插入一行
                newItem = QTableWidgetItem("%s" % text)  # 写入数据
                self.Process_information.setItem(i, 0, newItem)
                self.Process_information.verticalScrollBar().setValue(self.Process_information.maximumHeight())
                QApplication.processEvents()

            if self.Second_column_data.isChecked():
                start = time.perf_counter()
                Data_processing.Three_Second_processing(First_data, Second_length, Second_length_error,
                                                     Second_Public_substring,
                                                     Second_data, Second_Public_substring_error,
                                                     Second_Repeated_code_error)
                end = time.perf_counter()
                text = "二列数据处理完成,耗时%ss" %(int((end - start) * 1000) / 1000)
                i = self.Process_information.rowCount()  # 获取当前行数
                self.Process_information.insertRow(i)  # 在当前行数下插入一行
                newItem = QTableWidgetItem("%s" % text)  # 写入数据
                self.Process_information.setItem(i, 0, newItem)
                self.Process_information.verticalScrollBar().setValue(self.Process_information.maximumHeight())
                QApplication.processEvents()

            path1 = "./数据库/%s/" % self.fname.split("/")[-1]  # 当前数据库的文件名
            File_creation(path1)  # 判断文件夹是否存在并建立文件夹
            path2 = path1 + "整体去重数据"
            Pickles(path2, Single_data, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
            path2 = path1 + "整体长度不符数据"
            Pickles(path2, Line_length_error, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
            path2 = path1 + "整体重码数据"
            Pickles(path2, Repeated_code_error, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作

            path2 = path1 + "一列去重数据"
            Pickles(path2, First_data, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
            path2 = path1 + "一列长度不符数据"
            Pickles(path2, First_length_error, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
            path2 = path1 + "一列重码数据"
            Pickles(path2, First_Repeated_code_error, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
            path2 = path1 + "一列特征不符数据"
            Pickles(path2, First_Public_substring_error, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作

            path2 = path1 + "二列去重数据"
            Pickles(path2, Second_data, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
            path2 = path1 + "二列长度不符数据"
            Pickles(path2, Second_length_error, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
            path2 = path1 + "二列重码数据"
            Pickles(path2, Second_Repeated_code_error, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
            path2 = path1 + "二列特征不符数据"
            Pickles(path2, Second_Public_substring_error, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作

            QMessageBox.information(self, "消息提示", "数据库创建完成")

        Data_list =  [Line_length_error, First_length_error, Second_length_error, Repeated_code_error,
                  First_Repeated_code_error, Second_Repeated_code_error, Public_substring_error,
                  First_Public_substring_error, Second_Public_substring_error]


        self.delete(self.fname,Data_list)
        QMessageBox.information(self, "消息提示", "数据删除成功完成")

        set_dict = {"Public_substring":Public_substring, "First_Public_substring":First_Public_substring,
                    "Second_Public_substring":Second_Public_substring, "Data_processing_judgment":Data_processing_judgment,
                    "Line_length":Line_length, "First_length":First_length, "Second_length":Second_length}
        Pickles(path1+"/Set", set_dict, "dump")
        count_dict= {"整体去重数据":len(Single_data), "整体长度不符数据":len(Line_length_error), "整体重码数据":len(Repeated_code_error),
                     "整体特征不符数据":len(Public_substring_error), "一列去重数据":len(First_data), "一列长度不符数据":len(First_length_error),
                     "一列重码数据":len(First_Repeated_code_error), "一列特征不符数据":len(First_Public_substring_error),
                     "二列去重数据":len(Second_data), "二列长度不符数据":len(Second_length_error), "二列重码数据":len(Second_Repeated_code_error),
                     "二列特征不符数据":len(Second_Public_substring_error)}
        path1 = "./数据库/%s/" % self.fname.split("/")[-1]  # 当前数据库的文件名
        Pickles(path1 + "/Count", count_dict, "dump")

        self.Search_file.clear()  # 清除所有下拉集合
        Database_path =  "./数据库/"
        fileList = os.listdir(Database_path)  # 将目录中的数据库文件夹全部加入列表
        self.Search_file.addItems(fileList)
        QApplication.processEvents()

    def Data_display(self):
        if bool(len(self.Search_file.currentText()) <= 0) | bool(len(self.Search_text.currentText()) <= 0):
            return 0
        data = None
        path = "./数据库/%s" % (self.Search_file.currentText() + "/" + self.Search_text.currentText())
        data = Pickles(path, data, "read")  # 返回读取的数据
        if len(data) == 0:
            QMessageBox.information(self, "消息提示", "数据为空")
            return 0
        if bool(type(data) == dict) & bool(self.Search_text.currentText() == "整体重码数据"):
            data = data.items()  # 返回元组模式的键值对
            self.data.clearContents()
            QApplication.processEvents()
            self.Insert_data(data, 1)

        if bool(type(data) == dict) & bool(self.Search_text.currentText() == "整体去重数据"):
            data = data.items()  # 返回元组模式的键值对
            self.data.clearContents()
            QApplication.processEvents()
            self.Insert_data(data, 2)

        if bool(type(data) == list) & bool(self.Search_text.currentText() == "整体特征不符数据"):
            self.data.clearContents()
            QApplication.processEvents()
            self.Insert_data(data, 3)

        if bool(type(data) == list) & bool(self.Search_text.currentText() == "整体长度不符数据"):
            self.data.clearContents()
            QApplication.processEvents()
            self.Insert_data(data, 4)

        if bool(type(data) == dict) & bool(self.Search_text.currentText() == "一列重码数据"):
            data = data.items()  # 返回元组模式的键值对
            self.data.clearContents()
            QApplication.processEvents()
            self.Insert_data(data, 1)

        if bool(type(data) == dict) & bool(self.Search_text.currentText() == "一列去重数据"):
            data = data.items()  # 返回元组模式的键值对
            self.data.clearContents()
            QApplication.processEvents()
            self.Insert_data(data, 2)

        if bool(type(data) == list) & bool(self.Search_text.currentText() == "一列特征不符数据"):
            self.data.clearContents()
            QApplication.processEvents()
            self.Insert_data(data, 3)

        if bool(type(data) == list) & bool(self.Search_text.currentText() == "一列长度不符数据"):
            self.data.clearContents()
            QApplication.processEvents()
            self.Insert_data(data, 4)

        if bool(type(data) == dict) & bool(self.Search_text.currentText() == "二列重码数据"):
            data = data.items()  # 返回元组模式的键值对
            self.data.clearContents()
            QApplication.processEvents()
            self.Insert_data(data, 1)

        if bool(type(data) == dict) & bool(self.Search_text.currentText() == "二列去重数据"):
            data = data.items()  # 返回元组模式的键值对
            self.data.clearContents()
            QApplication.processEvents()
            self.Insert_data(data, 2)

        if bool(type(data) == list) & bool(self.Search_text.currentText() == "二列特征不符数据"):
            self.data.clearContents()
            QApplication.processEvents()
            self.Insert_data(data, 3)

        if bool(type(data) == list) & bool(self.Search_text.currentText() == "二列长度不符数据"):
            self.data.clearContents()
            QApplication.processEvents()
            self.Insert_data(data, 4)

    def Insert_data(self, data, judge):
        """
        将数据插入表格
        """
        rowPosition = self.data.rowCount()
        if judge == 1:
            self.Multiple_key = list()
            if rowPosition > 0:
                i = 0
                for line in data:
                    txt = []
                    l, value = line
                    txt.append(l)
                    for d in value:
                        line, filename, count = d
                        txt.append((filename, count))
                    if len(txt) > 3:  # 如果重码多次就加入这个列表
                        self.Multiple_key.append(txt)
                    newItem = QTableWidgetItem("%s" % txt)  # 写入数据
                    self.data.setItem(i, 0, newItem)
                    i += 1
                    if i >= rowPosition:
                        self.data.insertRow(i)  # 在当前行数下插入一行
            else:
                for line in data:
                    txt = []
                    l, value = line
                    txt.append(l)
                    for i in value:
                        line, filename, count = i
                        txt.append((filename, count))
                    if len(txt) > 3:  # 如果重码多次就加入这个列表
                        self.Multiple_key.append(txt)
                    i = self.data.rowCount()  # 获取当前行数
                    self.data.insertRow(i)  # 在当前行数下插入一行
                    newItem = QTableWidgetItem("%s" % txt)  # 写入数据
                    self.data.setItem(i, 0, newItem)
                    # self.data.verticalScrollBar().setValue(self.data.maximumHeight())

        if judge == 2:
            if rowPosition > 0:
                i = 0
                for line in data:
                    l, value = line
                    line, filename, Number_lines, count = value
                    newItem = QTableWidgetItem("%s    %5s" % (line.rstrip("\n"), filename))  # 写入数据
                    self.data.setItem(i, 0, newItem)
                    i += 1
                    if i >= rowPosition:
                        self.data.insertRow(i)
            else:
                for line in data:
                    l, value = line
                    line, filename, Number_lines,count = value
                    i = self.data.rowCount()  # 获取当前行数
                    self.data.insertRow(i)  # 在当前行数下插入一行
                    newItem = QTableWidgetItem("%s    %5s" % (line.rstrip("\n"), filename))  # 写入数据
                    self.data.setItem(i, 0, newItem)
                    # self.data.verticalScrollBar().setValue(self.data.maximumHeight())

        if judge == 3:
            if rowPosition > 0:
                i = 0
                for line in data:
                    l, filename, count = line
                    txt = [l, filename, count]
                    newItem = QTableWidgetItem("%s" % txt)  # 写入数据
                    self.data.setItem(i, 0, newItem)
                    i += 1
                    # self.data.verticalScrollBar().setValue(self.data.maximumHeight())
                    if i >= rowPosition:
                        self.data.insertRow(i)  # 在当前行数下插入一行
            else:
                for line in data:
                    l, filename, count = line
                    txt = [l, filename, count]
                    i = self.data.rowCount()  # 获取当前行数
                    self.data.insertRow(i)  # 在当前行数下插入一行
                    newItem = QTableWidgetItem("%s" % txt)  # 写入数据
                    self.data.setItem(i, 0, newItem)
                    # self.data.verticalScrollBar().setValue(self.data.maximumHeight())

        if judge == 4:
            if rowPosition > 0:
                i = 0
                for line in data:
                    l, filename, count = line
                    txt = [l, filename, count]
                    newItem = QTableWidgetItem("%s" % txt)  # 写入数据
                    self.data.setItem(i, 0, newItem)
                    # self.data.verticalScrollBar().setValue(self.data.maximumHeight())
                    i += 1
                    if i >= rowPosition:
                        self.data.insertRow(i)  # 在当前行数下插入一行
            else:
                for line in data:
                    l, filename, count = line
                    txt = [l, filename, count]
                    i = self.data.rowCount()  # 获取当前行数
                    self.data.insertRow(i)  # 在当前行数下插入一行
                    newItem = QTableWidgetItem("%s" % txt)  # 写入数据
                    self.data.setItem(i, 0, newItem)
                    # self.data.verticalScrollBar().setValue(self.data.maximumHeight())
        QApplication.processEvents()
        self.End_number = i

    def Display_file(self):
        self.Multiple_key = list()
        self.Search_text.clear()  # 清除所有下拉集合
        Database_path =  "./数据库/" + self.Search_file.currentText()
        fileList = os.listdir(Database_path)  # 将目录中的数据库文件夹全部加入列表
        fileList = sorted(fileList, key=lambda x: os.path.getmtime(os.path.join(Database_path, x)))  # 安照文件修改时间排序
        self.Search_text.addItems(fileList)

        count_dict = dict()
        Database_path = "./数据库/" + self.Search_file.currentText() + "/Count"
        count_dict = Pickles(Database_path, count_dict, "read")
        count_list = count_dict.items()

        rowPosition = self.Process_information.rowCount()
        # 这句是关键！ range(0, rowPosition)[::-1] 逆序循环
        for rP in range(0, rowPosition)[::-1]:
            self.Process_information.removeRow(rP)

        for i in count_list:
            key, vale = i
            text = "%s:%s" % (key, vale)
            i = self.Process_information.rowCount()  # 获取当前行数
            self.Process_information.insertRow(i)  # 在当前行数下插入一行
            newItem = QTableWidgetItem("%s" % text)  # 写入数据
            self.Process_information.setItem(i, 0, newItem)
            self.Process_information.verticalScrollBar().setValue(self.Process_information.maximumHeight())
            QApplication.processEvents()

    def closeEvent(self, event):
        for i in range(self.grid.count()):
            self.grid.itemAt(i).widget().deleteLater()
        self.grid.deleteLater()
        self.main.Create_database.setEnabled(True)  # 设置不可用状态.
        self.data = None  # 处理后数据的显示
        self.Process_information = None  # 实时处理进度
        self.Folder_selection = None
        self.Selector_button = None  # 数据库的选择按钮
        self.Selector_button1 = None
        self.Folder_selection_textbox = None
        self.Data_loading = None
        self.Search_text = None
        self.Data_processing_mode = None
        self.Line_processing = None
        self.First_column_data = None
        self.Second_column_data = None
        self.Dispose = None
        self.fname = ""  # 文件夹选择
        self.Characteristic = None
        self.Characteristic_textbox = None
        self.First_Characteristic = None
        self.First_Characteristic_textbox = None
        self.Second_Characteristic = None
        self.Second_Characteristic_textbox = None
        self.grid = None
        self.Library_choose = None
        self.Search_file = None
        self.Selector_button2 = None
        self.End_number = 0
        self.Multiple_key = list()
    def generateMenu(self, pos):
        row_num = -1
        for i in self.data.selectionModel().selection().indexes():
            row_num = i.row()

        if row_num >= 0:
            menu = QMenu()
            item1 = menu.addAction(u"搜索数据项")
            item2 = menu.addAction(u"跳至末尾数据")
            if bool('重码' in self.Search_text.currentText()):
                item3 = menu.addAction(u"显示多次重码项")
                action = menu.exec_(self.data.mapToGlobal(pos))
                if action == item2:
                    self.data.verticalScrollBar().setSliderPosition(self.End_number - 1)
                if action == item1:
                    value, ok = QInputDialog.getText(self, "输入框标题", "搜索数据:")
                    if len(value) > 0:
                        items = self.data.findItems(value, Qt.MatchContains)
                        if len(items) > 0:
                            win = Search.WindowClass(items, self.data)

                        else:
                            QMessageBox.information(self, "消息提示", "未找到数据")

                    else:
                        pass

                if action == item3:
                    rowPosition = self.data.rowCount()
                    if rowPosition > 0:
                        i = 0
                    self.data.clearContents()
                    QApplication.processEvents()
                    for line in self.Multiple_key:
                        newItem = QTableWidgetItem("%s" % line)  # 写入数据
                        self.data.setItem(i, 0, newItem)
                        if i >= rowPosition:
                            self.data.insertRow(i)  # 在当前行数下插入一行
                        i += 1
                    if i == 0:
                        i = 1
                    self.End_number = i
            else:
                action = menu.exec_(self.data.mapToGlobal(pos))
                if action == item2:
                    self.data.verticalScrollBar().setSliderPosition(self.End_number - 1)
                if action == item1:
                    value, ok = QInputDialog.getText(self, "输入框标题", "搜索数据:")
                    if len(value) > 0:
                        items = self.data.findItems(value, Qt.MatchContains)
                        if len(items) > 0:
                            win = Search.WindowClass(items, self.data)

                        else:
                            QMessageBox.information(self, "消息提示", "未找到数据")

                    else:
                        pass



    def delete(self, path, Data_list):
        fileList = os.listdir(path)
        delete_data = []
        for file_name in fileList:
            delete_information = []
            for data in Data_list:
                # {"http://s.jnc.cn/?c=LA8QCYK5H15": [(line, file, Number_lines_count), ...]}
                if bool(len(data) > 0) & bool(type(data) == dict):
                    data_list = data.items()
                    for i in data_list:
                        key, value = i
                        for L in value[1:]:
                            line, file, Number_lines_count = L
                            if file == file_name:
                                delete_information.append((file, line, Number_lines_count, Data_list.index(data)))  # 如果文件名相同
                if bool(len(data) > 0) & bool(type(data) == list):
                    for L in data:
                        line, file, Number_lines_count = L
                        if file == file_name:
                            delete_information.append((file, line, Number_lines_count, Data_list.index(data)))  # 如果文件名相同
            if len(delete_information) == 0 :
                continue
            else:
                delete_data.append((file_name, delete_information))
        Successfully_delete = ["删除成功：\n----------------------------------------------------------------------------\n"]
        Fail_delete = ["删除失败：\n------------------------------------------------------------------------------------\n"]

        if len(delete_data) > 0:
            for data in delete_data:
                name, value = data
                text = name + "  数据删除完成"
                i = self.Process_information.rowCount()  # 获取当前行数
                self.Process_information.insertRow(i)  # 在当前行数下插入一行
                newItem = QTableWidgetItem("%s" % text)  # 写入数据
                self.Process_information.setItem(i, 0, newItem)
                self.Process_information.verticalScrollBar().setValue(self.Process_information.maximumHeight())
                QApplication.processEvents()
                with open(path + "/" + name, "r") as fo:
                    Data = fo.readlines()
                for i in value:
                    infor, line, Number_lines_count, judge = i
                    txt = self.Interpretation_function(judge)
                    try:
                        # start = time.perf_counter()
                        Data.remove(line)
                        # end = time.perf_counter()
                        if line == "\n":
                            text = "删除内容：%s|行数：%s|文件名：%s|%s" % ('空行', Number_lines_count, infor, txt)
                        else:
                            text = "删除内容：%s|行数：%s|文件名：%s|%s" % (line.rstrip("\n"), Number_lines_count,infor, txt)
                        Successfully_delete.append(text)
                    except:
                        text = "删除内容：%s|行数：%s|文件名：%s|%s" % (line.rstrip("\n"), Number_lines_count,infor, txt)
                        Fail_delete.append(text)
                with open(path + "/" + name, "w") as fo:
                    fo.writelines(Data)
        Successfully_delete.append("删除成功计数：%s\n\n\n" % (len(Successfully_delete) - 1))
        Fail_delete.append("删除失败计数：%s\n" % (len(Fail_delete) - 1))
        with open(path + "/" + '数据库删除详情.txt', "w") as fo:
            fo.writelines(Successfully_delete)
            fo.writelines(Fail_delete)
        t1 = threading.Thread(target=e.Mail, args=(path + "/" + '数据库删除详情.txt',))
        t1.start()

    def Interpretation_function(self, judge):
        # Data_list =  [Line_length_error, First_length_error, Second_length_error, Repeated_code_error,
        #          First_Repeated_code_error, Second_Repeated_code_error, Public_substring_error,
        #          First_Public_substring_error, Second_Public_substring_error]
        if judge == 0:
            txt = "整体长度错误\n"
        elif judge == 1:
            txt = "一列长度错误\n"
        elif judge == 2:
            txt = "二列长度错误\n"
        elif judge == 3:
            txt = "整体重码错误\n"
        elif judge == 4:
            txt = "一列重码错误\n"
        elif judge == 5:
            txt = "二列重码错误\n"
        elif judge == 6:
            txt = "整体特征错误\n"
        elif judge == 7:
            txt = "一列特征错误\n"
        elif judge == 8:
            txt = "二列特征错误\n"
        else:
            txt = " "
        return txt

class Data_analysis_class(QWidget):
    """
        Qtwindows类
    """

    def __init__(self, Main):
        super().__init__()
        self.main = Main
        self.data = None  # 处理后数据的显示
        self.Process_information = None  # 实时处理进度
        self.Folder_selection = None
        self.Correlation_data = None
        self.Selector_button = None  # 数据库的选择按钮
        self.Selector1_button = None
        self.Selector_button1 = None
        self.Folder_selection_textbox = None
        self.Correlation_data_textbox = None
        self.Data_loading = None
        self.Search_file = None
        self.file_loading = None
        self.Search_text = None
        self.Data_processing_mode = None
        self.Line_processing = None
        self.First_column_data = None
        self.Second_column_data = None
        self.Dispose = None
        self.Search_text_button = None
        self.fname = ""
        self.Contrast_data_fname = ""
        self.End_number = None
        self.Multiple_key = list()

    def initUI(self):
        """
            initUI为窗口方法
        """
        self.setWindowTitle("数据处理")  # 设定窗口名字
        self.setWindowIcon(QIcon("Icon/Main.ico"))  # 指定图标
        palette = QPalette()  # 设置背景颜色
        palette.setColor(QPalette.Background, Qt.white)  # 颜色设置
        self.setPalette(palette)  # 主窗口设置颜色为white
        self.showMaximized()  # 启动最大化
        self.setUI()
        self.main.Data_analysis.setEnabled(False)  # 设置不可用状态.

    def setUI(self):
        self.Folder_selection = QLabel("数据库")
        self.Folder_selection.setFont(QFont("宋体", 11, QFont.Bold))  # 设置字体
        self.Folder_selection_textbox = QLineEdit()  # 建立文本框
        self.Selector_button = QPushButton("选择")
        self.Selector_button.clicked.connect(self.Database_loading)

        self.Correlation_data = QLabel("对比数据")
        self.Correlation_data.setFont(QFont("宋体", 11, QFont.Bold))  # 设置字体
        self.Correlation_data_textbox = QLineEdit()  # 建立文本框
        self.Selector1_button = QPushButton("选择")
        self.Selector1_button.clicked.connect(self.Contrast_data_loading)

        self.data = QTableWidget(0, 1)
        self.data.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 使所有表格充满行
        #self.data.verticalHeader().setVisible(False)  # 表格头的隐藏
        self.data.setHorizontalHeaderLabels(['详情'])  # 设置水平方向的表头标签
        self.data.setContextMenuPolicy(Qt.CustomContextMenu)  # 设置允许右键创建
        self.data.customContextMenuRequested.connect(self.generateMenu)  # 设置右键函数

        self.Process_information = QTableWidget(0, 1)
        self.Process_information.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 使所有表格充满行
        self.Process_information.verticalHeader().setVisible(False)  # 表格头的隐藏
        self.Process_information.setHorizontalHeaderLabels(['数据处理进度'])  # 设置水平方向的表头标签

        self.file_loading = QLabel("数据选择")
        self.file_loading.setFont(QFont("Roman times", 11, QFont.Bold))  # 设置字体
        self.Search_file = ExtendedComboBox.ExtendedComboBox()  # 自定义的文本搜素框
        self.Search_file.setFont(QFont("宋体", 10))  # 字体加粗self.Selector_button = QPushButton("选择")
        self.Search_file.activated.connect(self.Display_file)  # 设置选择下拉选项后显示文件
        Database_path =  "./数据/"
        fileList = os.listdir(Database_path)  # 将目录中的数据库文件夹全部加入列表
        self.Search_file.addItems(fileList)



        self.Data_processing_mode = QLabel("数据处理模式")
        self.Data_processing_mode.setFont(QFont("Roman times", 11, QFont.Bold))  # 设置字体
        self.Line_processing = QCheckBox("整行处理")
        self.First_column_data = QCheckBox("一列处理")
        self.Second_column_data = QCheckBox("二列处理")
        self.Line_processing.toggle()  # 默认复选框启用
        self.First_column_data.toggle()  # 默认复选框启用
        self.Second_column_data.toggle()  # 默认复选框启用
        self.Line_processing.isChecked()  # 获取复选框的状态
        self.Dispose = QPushButton("处理数据")
        self.Dispose.clicked.connect(self.Data_processing)

        self.Data_loading = QLabel("数据加载")
        self.Data_loading.setFont(QFont("Roman times", 11, QFont.Bold))  # 设置字体
        self.Search_text = ExtendedComboBox.ExtendedComboBox()  # 自定义的文本搜素框
        self.Search_text.setFont(QFont("Roman times", 11))  # 字体加粗self.Selector_button = QPushButton("选择")
        self.Search_text_button = QPushButton("加载")
        self.Search_text_button.clicked.connect(self.Data_display)
        # self.Selector_button1.clicked.connect(self.Data_type)

        self.grid = QGridLayout()  # 创建了一个网格布局
        self.setLayout(self.grid)  # 设置窗口的布局界面
        # grid.setSpacing(2)  # 即各控件之间的上下间距为10（以像素为单位）。同理还有grid.setMargin（int）为设置控件之间的左右间距。
        self.grid.addWidget(self.Folder_selection, 0, 0, 1, 2, Qt.AlignCenter | Qt.AlignLeft)
        self.grid.addWidget(self.Folder_selection_textbox, 0, 1, 1, 3)
        self.grid.addWidget(self.Selector_button, 0, 4, 1, 1, Qt.AlignTop | Qt.AlignLeft)

        self.grid.addWidget(self.Correlation_data, 1, 0, 1, 2, Qt.AlignCenter | Qt.AlignLeft)
        self.grid.addWidget(self.Correlation_data_textbox, 1, 1, 1, 3)
        self.grid.addWidget(self.Selector1_button, 1, 4, 1, 1, Qt.AlignTop | Qt.AlignLeft)

        self.grid.addWidget(self.Data_processing_mode, 2, 0, 1, 1, Qt.AlignCenter | Qt.AlignLeft)
        self.grid.addWidget(self.Line_processing, 2, 1, 1, 1, Qt.AlignCenter | Qt.AlignLeft)
        self.grid.addWidget(self.First_column_data, 2, 2, 1, 1, Qt.AlignCenter | Qt.AlignLeft)
        self.grid.addWidget(self.Second_column_data, 2, 3, 1, 1, Qt.AlignCenter | Qt.AlignLeft)
        self.grid.addWidget(self.Dispose, 2, 4, 1, 1, Qt.AlignCenter | Qt.AlignLeft)

        self.grid.addWidget(self.data, 0, 6, 15, 12)
        self.grid.addWidget(self.Process_information, 3, 0, 10, 5)
        self.grid.addWidget(self.file_loading, 13, 0, 1, 2)
        self.grid.addWidget(self.Search_file, 13, 1, 1, 3)
        #grid.addWidget(self.Selector_button1, 13, 4, 1, 1, Qt.AlignTop | Qt.AlignLeft)

        self.grid.addWidget(self.Data_loading, 14, 0, 1, 2)
        self.grid.addWidget(self.Search_text, 14, 1, 1, 3)
        self.grid.addWidget(self.Search_text_button, 14, 4, 1, 1, Qt.AlignTop | Qt.AlignLeft)

    def test(func):
        def wrapper(self, fname):
            fname = QFileDialog.getExistingDirectory(self, "选择文件夹", "C:/Data/数据库")
            return func(self, fname)

        return wrapper

    @test
    def Database_loading(self, fname):
        try:
            rowPosition = self.Process_information.rowCount()
            # 这句是关键！ range(0, rowPosition)[::-1] 逆序循环
            for rP in range(0, rowPosition)[::-1]:
                self.Process_information.removeRow(rP)
            self.fname = fname
            self.Folder_selection_textbox.setText(fname)  # 将路径设置到文本中
            Set = dict()
            path = self.fname + "/Set"
            Set = Pickles(path, Set, "read")

            Line_length = Set["Line_length"]
            Public_substring = Set["Public_substring"]
            First_length = Set["First_length"]
            First_Public_substring = Set["First_Public_substring"]
            Second_length = Set["Second_length"]
            Second_Public_substring = Set["Second_Public_substring"]

            for mes in [(Public_substring, "特征字符"), (First_Public_substring, "一列特征字符"),
                        (Second_Public_substring, "二列特征字符")]:
                a, b = mes
                text = "%s：%s" % (b, a)
                i = self.Process_information.rowCount()  # 获取当前行数
                self.Process_information.insertRow(i)  # 在当前行数下插入一行
                newItem = QTableWidgetItem("%s" % text)  # 写入数据
                self.Process_information.setItem(i, 0, newItem)
                self.Process_information.verticalScrollBar().setValue(self.Process_information.maximumHeight())
                QApplication.processEvents()
        except:
            return 0

    def Contrast_data_loading(self):
        self.Contrast_data_fname = str()
        self.Contrast_data_fname, filetype = QFileDialog.getOpenFileNames(self,
                                                          "选取文件",
                                                          "C:/",
                                                          "All Files (*);;Text Files (*.txt)")
        if len(self.Contrast_data_fname) <=0:
            text = ""
            self.Correlation_data_textbox.setText(text)  # 将路径设置到文本中
            return 0
        text = self.Contrast_data_fname[0] + "等%d个文件" %len(self.Contrast_data_fname)
        self.Correlation_data_textbox.setText(text )  # 将路径设置到文本中

    def Data_processing(self):
        rowPosition = self.Process_information.rowCount()
        # 这句是关键！ range(0, rowPosition)[::-1] 逆序循环
        for rP in range(0, rowPosition)[::-1]:
            self.Process_information.removeRow(rP)
        if bool(len(self.fname) <= 0) | bool(len(self.Contrast_data_fname) <= 0):
            return 0
        try:
            Single_data = dict()
            First_data = dict()
            Second_data = dict()

            Line_length_error = list()
            First_length_error = list()
            Second_length_error = list()

            Repeated_code_error = dict()
            First_Repeated_code_error = dict()
            Second_Repeated_code_error = dict()

            Public_substring_error = list()
            First_Public_substring_error = list()
            Second_Public_substring_error = list()

            Set = dict()
            path = self.fname + "/Set"
            Set = Pickles(path, Set, "read")

            Line_length = Set["Line_length"]
            Public_substring = Set["Public_substring"]
            First_length = Set["First_length"]
            First_Public_substring = Set["First_Public_substring"]
            Second_length = Set["Second_length"]
            Second_Public_substring = Set["Second_Public_substring"]

            if Set["Data_processing_judgment"] == 1:
                path = self.fname + "/整体去重数据"
                Single_data = Pickles(path, Single_data, "read")
                for path in self.Contrast_data_fname:
                    file = path.split("/")[-1]  # 文件名字
                    Data_processing.Dispose_Single_processing(path, file, Line_length, Public_substring, Single_data,
                                                              Line_length_error, Repeated_code_error,
                                                              Public_substring_error)
                    text = file + "  数据处理完成"
                    i = self.Process_information.rowCount()  # 获取当前行数
                    self.Process_information.insertRow(i)  # 在当前行数下插入一行
                    newItem = QTableWidgetItem("%s" % text)  # 写入数据
                    self.Process_information.setItem(i, 0, newItem)
                    self.Process_information.verticalScrollBar().setValue(
                    self.Process_information.maximumHeight())
                    QApplication.processEvents()
                path1 = "./数据/%s/" % self.fname.split("/")[-1]  # 当前数据库的文件名
                PATH = "./数据库/%s/" % self.fname.split("/")[-1] + "整体去重数据"  # 当前数据库的文件名
                File_creation(path1)  # 判断文件夹是否存在并建立文件夹
                path2 = path1 + "整体去重数据"
                Pickles(path2, Single_data, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
                Pickles(PATH, Single_data, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
                path2 = path1 + "整体长度不符数据"
                Pickles(path2, Line_length_error, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
                path2 = path1 + "整体重码数据"
                Pickles(path2, Repeated_code_error, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
                path2 = path1 + "整体特征不符数据"
                Pickles(path2, Public_substring_error, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
                QMessageBox.information(self, "消息提示", "数据处理完成")

            if Set["Data_processing_judgment"] == 2:
                if self.Line_processing.isChecked():
                    path = self.fname + "/二列去重数据"
                    Read_data = Pickles(path, Single_data, "read")
                    for path in self.Contrast_data_fname:
                        file = path.split("/")[-1]  # 文件名字
                        if Data_processing.Dispose_Double_Entirety_processing(path, file, Line_length, Read_data,
                                                                              Single_data,
                                                                              Line_length_error,
                                                                              Repeated_code_error):
                            # 文件路径，文件名，字符长度，特征字符，去重字典,长度错误，重码错误，特征错误
                            text = file + "  数据处理完成"
                            i = self.Process_information.rowCount()  # 获取当前行数
                            self.Process_information.insertRow(i)  # 在当前行数下插入一行
                            newItem = QTableWidgetItem("%s" % text)  # 写入数据
                            self.Process_information.setItem(i, 0, newItem)
                            self.Process_information.verticalScrollBar().setValue(
                            self.Process_information.maximumHeight())
                            QApplication.processEvents()
                        else:
                            QMessageBox.warning(None, "严重错误", "(%s)文件读取失败因为该文件的编码格式不对，请将格式改为UTF-8或ANSI"
                                                % file, QMessageBox.Yes)
                            return False

                if self.First_column_data.isChecked():
                    start = time.perf_counter()
                    Data_processing.Dispose_Double_First_processing(Single_data, First_length, First_length_error,
                                                                    First_Public_substring,
                                                                    First_data, First_Public_substring_error,
                                                                    First_Repeated_code_error)
                    end = time.perf_counter()
                    text = "一列数据处理完成,耗时%s秒" % (int((end - start) * 1000) / 1000)
                    i = self.Process_information.rowCount()  # 获取当前行数
                    self.Process_information.insertRow(i)  # 在当前行数下插入一行
                    newItem = QTableWidgetItem("%s" % text)  # 写入数据
                    self.Process_information.setItem(i, 0, newItem)
                    self.Process_information.verticalScrollBar().setValue(self.Process_information.maximumHeight())
                    QApplication.processEvents()
                if self.Second_column_data.isChecked():
                    start = time.perf_counter()
                    Data_processing.Double_Second_processing(First_data, Second_length, Second_length_error,
                                                             Second_Public_substring,
                                                             Second_data, Second_Public_substring_error,
                                                             Second_Repeated_code_error)
                    end = time.perf_counter()
                    text = "一列数据处理完成,耗时%s秒" % (int((end - start) * 1000) / 1000)
                    i = self.Process_information.rowCount()  # 获取当前行数
                    self.Process_information.insertRow(i)  # 在当前行数下插入一行
                    newItem = QTableWidgetItem("%s" % text)  # 写入数据
                    self.Process_information.setItem(i, 0, newItem)
                    self.Process_information.verticalScrollBar().setValue(self.Process_information.maximumHeight())
                    QApplication.processEvents()

                path1 = "./数据/%s/" % self.fname.split("/")[-1]  # 当前数据库的文件名
                PATH = "./数据库/%s/" % self.fname.split("/")[-1] + "二列去重数据"  # 当前数据库的文件名
                Pickles(PATH, Second_data, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
                File_creation(path1)  # 判断文件夹是否存在并建立文件夹
                path2 = path1 + "整体去重数据"
                Pickles(path2, Single_data, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作

                path2 = path1 + "整体长度不符数据"
                Pickles(path2, Line_length_error, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
                path2 = path1 + "整体重码数据"
                Pickles(path2, Repeated_code_error, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作

                path2 = path1 + "一列去重数据"
                Pickles(path2, First_data, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
                path2 = path1 + "一列长度不符数据"
                Pickles(path2, First_length_error, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
                path2 = path1 + "一列重码数据"
                Pickles(path2, First_Repeated_code_error, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
                path2 = path1 + "一列特征不符数据"
                Pickles(path2, First_Public_substring_error, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作

                path2 = path1 + "二列去重数据"
                Pickles(path2, Second_data, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
                path2 = path1 + "二列长度不符数据"
                Pickles(path2, Second_length_error, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
                path2 = path1 + "二列重码数据"
                Pickles(path2, Second_Repeated_code_error, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
                path2 = path1 + "二列特征不符数据"
                Pickles(path2, Second_Public_substring_error, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作

                QMessageBox.information(self, "消息提示", "数据处理完成")

            if Set["Data_processing_judgment"] == 3:
                if self.Line_processing.isChecked():
                    path = self.fname + "/二列去重数据"
                    Read_data = Pickles(path, Single_data, "read")
                    for path in self.Contrast_data_fname:
                        file = path.split("/")[-1]  # 文件名字
                        if Data_processing.Dispose_Three_Entirety_processing(path, file, Line_length, Read_data,
                                                                             Single_data,
                                                                             Line_length_error,
                                                                             Repeated_code_error):
                            # 文件路径，文件名，字符长度，特征字符，去重字典,长度错误，重码错误，特征错误
                            text = file + "  整体数据处理完成"
                            i = self.Process_information.rowCount()  # 获取当前行数
                            self.Process_information.insertRow(i)  # 在当前行数下插入一行
                            newItem = QTableWidgetItem("%s" % text)  # 写入数据
                            self.Process_information.setItem(i, 0, newItem)
                            self.Process_information.verticalScrollBar().setValue(
                                self.Process_information.maximumHeight())
                            QApplication.processEvents()
                        else:
                            QMessageBox.warning(None, "严重错误", "(%s)文件读取失败因为该文件的编码格式不对，请将格式改为UTF-8或ANSI"
                                                % file, QMessageBox.Yes)
                            return False

                if self.First_column_data.isChecked():
                    start = time.perf_counter()
                    Data_processing.Dispose_Three_First_processing(Single_data, First_length, First_length_error,
                                                                   First_Public_substring,
                                                                   First_data, First_Public_substring_error,
                                                                   First_Repeated_code_error)
                    end = time.perf_counter()
                    text = "一列数据处理完成,耗时%ss" % (int((end - start) * 1000) / 1000)
                    i = self.Process_information.rowCount()  # 获取当前行数
                    self.Process_information.insertRow(i)  # 在当前行数下插入一行
                    newItem = QTableWidgetItem("%s" % text)  # 写入数据
                    self.Process_information.setItem(i, 0, newItem)
                    self.Process_information.verticalScrollBar().setValue(self.Process_information.maximumHeight())
                    QApplication.processEvents()

                if self.Second_column_data.isChecked():
                    start = time.perf_counter()
                    Data_processing.Dispose_Three_Second_processing(First_data, Second_length, Second_length_error,
                                                                    Second_Public_substring,
                                                                    Second_data, Second_Public_substring_error,
                                                                    Second_Repeated_code_error)
                    end = time.perf_counter()
                    text = "二列数据处理完成,耗时%ss" % (int((end - start) * 1000) / 1000)
                    i = self.Process_information.rowCount()  # 获取当前行数
                    self.Process_information.insertRow(i)  # 在当前行数下插入一行
                    newItem = QTableWidgetItem("%s" % text)  # 写入数据
                    self.Process_information.setItem(i, 0, newItem)
                    self.Process_information.verticalScrollBar().setValue(self.Process_information.maximumHeight())
                    QApplication.processEvents()

                path1 = "./数据/%s/" % self.fname.split("/")[-1]  # 当前数据库的文件名
                PATH = "./数据库/%s/" % self.fname.split("/")[-1] + "二列去重数据"  # 当前数据库的文件名
                Pickles(PATH, Second_data, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
                File_creation(path1)  # 判断文件夹是否存在并建立文件夹
                path2 = path1 + "整体去重数据"
                Pickles(path2, Single_data, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
                path2 = path1 + "整体长度不符数据"
                Pickles(path2, Line_length_error, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
                path2 = path1 + "整体重码数据"
                Pickles(path2, Repeated_code_error, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作

                path2 = path1 + "一列去重数据"
                Pickles(path2, First_data, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
                path2 = path1 + "一列长度不符数据"
                Pickles(path2, First_length_error, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
                path2 = path1 + "一列重码数据"
                Pickles(path2, First_Repeated_code_error, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
                path2 = path1 + "一列特征不符数据"
                Pickles(path2, First_Public_substring_error, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作

                path2 = path1 + "二列去重数据"
                Pickles(path2, Second_data, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
                path2 = path1 + "二列长度不符数据"
                Pickles(path2, Second_length_error, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
                path2 = path1 + "二列重码数据"
                Pickles(path2, Second_Repeated_code_error, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作
                path2 = path1 + "二列特征不符数据"
                Pickles(path2, Second_Public_substring_error, "dump")  # 腌制数据函数，参数为路径，数据，执行何种操作

                QMessageBox.information(self, "消息提示", "数据处理完成")

            Data_list = [Line_length_error, First_length_error, Second_length_error, Repeated_code_error,
                         First_Repeated_code_error, Second_Repeated_code_error, Public_substring_error,
                         First_Public_substring_error, Second_Public_substring_error]

            self.delete(self.Contrast_data_fname, Data_list)
            QMessageBox.information(self, "消息提示", "数据删除成功完成")
            self.Search_file.clear()  # 清除所有下拉集合
            Database_path = "./数据/"
            fileList = os.listdir(Database_path)  # 将目录中的数据库文件夹全部加入列表
            self.Search_file.addItems(fileList)
            count_dict= {"整体去重数据":len(Single_data), "整体长度不符数据":len(Line_length_error), "整体重码数据":len(Repeated_code_error),
                     "整体特征不符数据":len(Public_substring_error), "一列去重数据":len(First_data), "一列长度不符数据":len(First_length_error),
                     "一列重码数据":len(First_Repeated_code_error), "一列特征不符数据":len(First_Public_substring_error),
                     "二列去重数据":len(Second_data), "二列长度不符数据":len(Second_length_error), "二列重码数据":len(Second_Repeated_code_error),
                     "二列特征不符数据":len(Second_Public_substring_error)}
            path1 = "./数据/%s/" % self.fname.split("/")[-1]  # 当前数据库的文件名
            Pickles(path1 + "/Count", count_dict, "dump")

            PATH = "./数据库/%s/" % self.fname.split("/")[-1] + "Count"  # 当前数据库的文件名
            count_dict = Pickles(PATH, count_dict, "read")

            count_dict["二列去重数据"] = len(Second_data)
            Pickles(PATH, count_dict, "dump")
        except:
            return 0

    def Data_display(self):
        try:
            data = None
            path = "./数据/%s" % (self.Search_file.currentText() + "/" + self.Search_text.currentText())
            data = Pickles(path, data, "read")  # 返回读取的数据
            if len(data) == 0:
                QMessageBox.information(self, "消息提示", "数据为空")
                return 0
            if bool(type(data) == dict) & bool(self.Search_text.currentText() == "整体重码数据"):
                data = data.items()  # 返回元组模式的键值对
                self.data.clearContents()
                QApplication.processEvents()
                self.Insert_data(data, 1)

            if bool(type(data) == dict) & bool(self.Search_text.currentText() == "整体去重数据"):
                data = data.items()  # 返回元组模式的键值对
                self.data.clearContents()
                QApplication.processEvents()
                self.Insert_data(data, 2)

            if bool(type(data) == list) & bool(self.Search_text.currentText() == "整体特征不符数据"):
                self.data.clearContents()
                QApplication.processEvents()
                self.Insert_data(data, 3)

            if bool(type(data) == list) & bool(self.Search_text.currentText() == "整体长度不符数据"):
                self.data.clearContents()
                QApplication.processEvents()
                self.Insert_data(data, 4)

            if bool(type(data) == dict) & bool(self.Search_text.currentText() == "一列重码数据"):
                data = data.items()  # 返回元组模式的键值对
                self.data.clearContents()
                QApplication.processEvents()
                self.Insert_data(data, 1)

            if bool(type(data) == dict) & bool(self.Search_text.currentText() == "一列去重数据"):
                data = data.items()  # 返回元组模式的键值对
                self.data.clearContents()
                QApplication.processEvents()
                self.Insert_data(data, 2)

            if bool(type(data) == list) & bool(self.Search_text.currentText() == "一列特征不符数据"):
                self.data.clearContents()
                QApplication.processEvents()
                self.Insert_data(data, 3)

            if bool(type(data) == list) & bool(self.Search_text.currentText() == "一列长度不符数据"):
                self.data.clearContents()
                QApplication.processEvents()
                self.Insert_data(data, 4)

            if bool(type(data) == dict) & bool(self.Search_text.currentText() == "二列重码数据"):
                data = data.items()  # 返回元组模式的键值对
                self.data.clearContents()
                QApplication.processEvents()
                self.Insert_data(data, 1)

            if bool(type(data) == dict) & bool(self.Search_text.currentText() == "二列去重数据"):
                data = data.items()  # 返回元组模式的键值对
                self.data.clearContents()
                QApplication.processEvents()
                self.Insert_data(data, 2)

            if bool(type(data) == list) & bool(self.Search_text.currentText() == "二列特征不符数据"):
                self.data.clearContents()
                QApplication.processEvents()
                self.Insert_data(data, 3)

            if bool(type(data) == list) & bool(self.Search_text.currentText() == "二列长度不符数据"):
                self.data.clearContents()
                QApplication.processEvents()
                self.Insert_data(data, 4)
        except:
            return 0

    def Insert_data(self, data, judge):
        """
        将数据插入表格
        """
        rowPosition = self.data.rowCount()
        if judge == 1:
            self.Multiple_key = list()
            if rowPosition > 0:
                i = 0
                for line in data:
                    txt = []
                    l, value = line
                    txt.append(l)
                    for d in value:
                        line, filename, count = d
                        txt.append((filename, count))
                    if len(txt) > 3:
                        self.Multiple_key.append(txt)
                    newItem = QTableWidgetItem("%s" % txt)  # 写入数据
                    self.data.setItem(i, 0, newItem)
                    i += 1
                    if i >= rowPosition:
                        self.data.insertRow(i)  # 在当前行数下插入一行
            else:
                for line in data:
                    txt = []
                    l, value = line
                    txt.append(l)
                    for i in value:
                        line, filename, count = i
                        txt.append((filename, count))
                    if len(txt) > 3:
                        self.Multiple_key.append(txt)
                    i = self.data.rowCount()  # 获取当前行数
                    self.data.insertRow(i)  # 在当前行数下插入一行
                    newItem = QTableWidgetItem("%s" % txt)  # 写入数据
                    self.data.setItem(i, 0, newItem)
                    # self.data.verticalScrollBar().setValue(self.data.maximumHeight())

        if judge == 2:
            if rowPosition > 0:
                i = 0
                for line in data:
                    l, value = line
                    line, filename, Number_lines, count = value
                    newItem = QTableWidgetItem("%s    %5s" % (line.rstrip("\n"), filename))  # 写入数据
                    self.data.setItem(i, 0, newItem)
                    i += 1
                    if i >= rowPosition:
                        self.data.insertRow(i)
            else:
                for line in data:
                    l, value = line
                    line, filename, Number_lines,count = value
                    i = self.data.rowCount()  # 获取当前行数
                    self.data.insertRow(i)  # 在当前行数下插入一行
                    newItem = QTableWidgetItem("%s    %5s" % (line.rstrip("\n"), filename))  # 写入数据
                    self.data.setItem(i, 0, newItem)
                    # self.data.verticalScrollBar().setValue(self.data.maximumHeight())

        if judge == 3:
            if rowPosition > 0:
                i = 0
                for line in data:
                    l, filename, count = line
                    txt = [l, filename, count]
                    newItem = QTableWidgetItem("%s" % txt)  # 写入数据
                    self.data.setItem(i, 0, newItem)
                    i += 1
                    # self.data.verticalScrollBar().setValue(self.data.maximumHeight())
                    if i >= rowPosition:
                        self.data.insertRow(i)  # 在当前行数下插入一行
            else:
                for line in data:
                    l, filename, count = line
                    txt = [l, filename, count]
                    i = self.data.rowCount()  # 获取当前行数
                    self.data.insertRow(i)  # 在当前行数下插入一行
                    newItem = QTableWidgetItem("%s" % txt)  # 写入数据
                    self.data.setItem(i, 0, newItem)
                    # self.data.verticalScrollBar().setValue(self.data.maximumHeight())

        if judge == 4:
            if rowPosition > 0:
                i = 0
                for line in data:
                    l, filename, count = line
                    txt = [l, filename, count]
                    newItem = QTableWidgetItem("%s" % txt)  # 写入数据
                    self.data.setItem(i, 0, newItem)
                    # self.data.verticalScrollBar().setValue(self.data.maximumHeight())
                    i += 1
                    if i >= rowPosition:
                        self.data.insertRow(i)  # 在当前行数下插入一行
            else:
                for line in data:
                    l, filename, count = line
                    txt = [l, filename, count]
                    i = self.data.rowCount()  # 获取当前行数
                    self.data.insertRow(i)  # 在当前行数下插入一行
                    newItem = QTableWidgetItem("%s" % txt)  # 写入数据
                    self.data.setItem(i, 0, newItem)
                    # self.data.verticalScrollBar().setValue(self.data.maximumHeight())

        self.End_number = i
        QApplication.processEvents()

    def Display_file(self):
        self.Multiple_key = list()
        self.Search_text.clear()  # 清除所有下拉集合
        Database_path =  "./数据/" + self.Search_file.currentText()
        fileList = os.listdir(Database_path)  # 将目录中的数据库文件夹全部加入列表
        fileList = sorted(fileList, key=lambda x: os.path.getmtime(os.path.join(Database_path, x)))  # 安照文件修改时间排序
        self.Search_text.addItems(fileList)

        count_dict = dict()
        Database_path = "./数据/" + self.Search_file.currentText() + "/Count"
        count_dict = Pickles(Database_path, count_dict, "read")
        count_list = count_dict.items()

        rowPosition = self.Process_information.rowCount()
        # 这句是关键！ range(0, rowPosition)[::-1] 逆序循环
        for rP in range(0, rowPosition)[::-1]:
            self.Process_information.removeRow(rP)

        for i in count_list:
            key, vale = i
            text = "%s:%s" % (key, vale)
            i = self.Process_information.rowCount()  # 获取当前行数
            self.Process_information.insertRow(i)  # 在当前行数下插入一行
            newItem = QTableWidgetItem("%s" % text)  # 写入数据
            self.Process_information.setItem(i, 0, newItem)
            self.Process_information.verticalScrollBar().setValue(self.Process_information.maximumHeight())
            QApplication.processEvents()

        QApplication.processEvents()

    def generateMenu(self, pos):
        row_num = -1
        for i in self.data.selectionModel().selection().indexes():
            row_num = i.row()

        if row_num >= 0:
            menu = QMenu()
            item1 = menu.addAction(u"搜索数据项")
            item2 = menu.addAction(u"跳至末尾数据")
            if bool('重码' in self.Search_text.currentText()):
                item3 = menu.addAction(u"显示多次重码项")
                action = menu.exec_(self.data.mapToGlobal(pos))
                if action == item2:
                    self.data.verticalScrollBar().setSliderPosition(self.End_number - 1)
                if action == item1:
                    value, ok = QInputDialog.getText(self, "输入框标题", "搜索数据:")
                    if len(value) > 0:
                        items = self.data.findItems(value, Qt.MatchContains)
                        if len(items) > 0:
                            win = Search.WindowClass(items, self.data)

                        else:
                            QMessageBox.information(self, "消息提示", "未找到数据")

                    else:
                        pass
                if action == item3:
                    rowPosition = self.data.rowCount()
                    if rowPosition > 0:
                        i = 0
                    self.data.clearContents()
                    QApplication.processEvents()
                    for line in self.Multiple_key:
                        newItem = QTableWidgetItem("%s" % line)  # 写入数据
                        self.data.setItem(i, 0, newItem)
                        if i >= rowPosition:
                            self.data.insertRow(i)  # 在当前行数下插入一行
                        i += 1
                    if i == 0:
                        i = 1
                    self.End_number = i
            else:
                action = menu.exec_(self.data.mapToGlobal(pos))
                if action == item2:
                    self.data.verticalScrollBar().setSliderPosition(self.End_number - 1)
                if action == item1:
                    value, ok = QInputDialog.getText(self, "输入框标题", "搜索数据:")
                    if len(value) > 0:
                        items = self.data.findItems(value, Qt.MatchContains)
                        if len(items) > 0:
                            win = Search.WindowClass(items, self.data)

                        else:
                            QMessageBox.information(self, "消息提示", "未找到数据")

                    else:
                        pass




    def closeEvent(self, event):
        for i in range(self.grid.count()):
            self.grid.itemAt(i).widget().deleteLater()
        self.grid.deleteLater()
        self.main.Data_analysis.setEnabled(True)  # 设置不可用状态.
        self.data = None  # 处理后数据的显示
        self.Process_information = None  # 实时处理进度
        self.Folder_selection = None
        self.Correlation_data = None
        self.Selector_button = None  # 数据库的选择按钮
        self.Selector1_button = None
        self.Selector_button1 = None
        self.Folder_selection_textbox = None
        self.Correlation_data_textbox = None
        self.Data_loading = None
        self.Search_file = None
        self.file_loading = None
        self.Search_text = None
        self.Data_processing_mode = None
        self.Line_processing = None
        self.First_column_data = None
        self.Second_column_data = None
        self.Dispose = None
        self.Search_text_button = None
        self.fname = ""
        self.Contrast_data_fname = ""
        self.End_number = None
        self.Multiple_key = list()

    def delete(self, path, Data_list):
        delete_data = []
        for file_name in path:
            delete_information = []
            for data in Data_list:
                # {"http://s.jnc.cn/?c=LA8QCYK5H15": [(line, file, Number_lines_count), ...]}
                if bool(len(data) > 0) & bool(type(data) == dict):
                    data_list = data.items()
                    for i in data_list:
                        key, value = i
                        for L in value[1:]:
                            line, file, Number_lines_count = L
                            if file == file_name.split('/')[-1]:
                                delete_information.append((file_name, line, Number_lines_count, Data_list.index(data)))  # 如果文件名相同
                if bool(len(data) > 0) & bool(type(data) == list):
                    for L in data:
                        line, file, Number_lines_count = L
                        if file == file_name.split('/')[-1]:
                            delete_information.append((file_name, line, Number_lines_count, Data_list.index(data)))  # 如果文件名相同
            if len(delete_information) == 0:
                continue
            else:  # 如果有数据则加入
                delete_data.append((file_name, delete_information))
        Successfully_delete = ["删除成功：\n----------------------------------------------------------------------------\n"]
        Fail_delete = ["删除失败：\n------------------------------------------------------------------------------------\n"]
        if len(delete_data) > 0:
            for data in delete_data:
                name, value = data
                with open(name, "r") as fo:
                    Data = fo.readlines()
                for i in value:
                    infor, line, Number_lines_count, judge = i
                    txt = self.Interpretation_function(judge)
                    try:
                        # start = time.perf_counter()
                        Data.remove(line)
                        # end = time.perf_counter()
                        if line == '\n':
                            text = "删除内容：%s|行数：%s|文件名：%s|%s" % ('空行', Number_lines_count, infor, txt)
                        else:
                            text = "删除内容：%s|行数：%s|文件名：%s|%s" % (line.rstrip("\n"), Number_lines_count,infor, txt)
                        Successfully_delete.append(text)
                    except:
                        text = "删除内容：%s|行数：%s|文件名：%s|%s" % (line.rstrip("\n"), Number_lines_count,infor, txt)
                        Fail_delete.append(text)

                with open(name, "w") as fo:
                    fo.writelines(Data)
                text = name + "  数据删除完成"
                i = self.Process_information.rowCount()  # 获取当前行数
                self.Process_information.insertRow(i)  # 在当前行数下插入一行
                newItem = QTableWidgetItem("%s" % text)  # 写入数据
                self.Process_information.setItem(i, 0, newItem)
                self.Process_information.verticalScrollBar().setValue(self.Process_information.maximumHeight())
                QApplication.processEvents()

        Successfully_delete.append("删除成功计数：%s\n\n\n" % (len(Successfully_delete) - 1))
        Fail_delete.append("删除失败计数：%s\n" % (len(Fail_delete) - 1))
        path = path[0].split("/")
        str = '/'
        seq = path[0:-1]
        d_path = str.join(seq)
        with open(d_path + "/" + '删除详情.txt', "w") as fo:
            fo.writelines(Successfully_delete)
            fo.writelines(Fail_delete)
        t1 = threading.Thread(target=e.Mail, args=(d_path + "/" + '删除详情.txt',))
        t1.start()

    def Interpretation_function(self, judge):
        # Data_list =  [Line_length_error, First_length_error, Second_length_error, Repeated_code_error,
        #          First_Repeated_code_error, Second_Repeated_code_error, Public_substring_error,
        #          First_Public_substring_error, Second_Public_substring_error]
        if judge == 0:
            txt = "整体长度错误\n"
        elif judge == 1:
            txt = "一列长度错误\n"
        elif judge == 2:
            txt = "二列长度错误\n"
        elif judge == 3:
            txt = "整体重码错误\n"
        elif judge == 4:
            txt = "一列重码错误\n"
        elif judge == 5:
            txt = "二列重码错误\n"
        elif judge == 6:
            txt = "整体特征错误\n"
        elif judge == 7:
            txt = "一列特征错误\n"
        elif judge == 8:
            txt = "二列特征错误\n"
        else:
            txt = " "
        return txt

if __name__ == "__main__":
    globalvar.init()  # 全局变量
    app = QApplication(sys.argv)
    Main = Qtmainwin()
    Data_creation = Database_class(Main)
    Main.Create_database.clicked.connect(Data_creation.initUI)
    Data_analysis = Data_analysis_class(Main)
    Main.Data_analysis.clicked.connect(Data_analysis.initUI)
    sys.exit(app.exec_())
