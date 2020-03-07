# -*- encoding: utf-8 -*-
"""
@文件名     : 123.py
@时间       : 2020/2/26 15:27
@作者       : 刘锐
@邮箱       : 1090339852@qq.com
@创建软件   : PyCharm
@版本信息   ：1.0.1
"""

import os
import sys
from globalvar import globalvar as gl
from Interface import Software_interface
from PyQt5.QtWidgets import (QApplication)

def File_creation():
    path = "./数据"
    isExists = os.path.exists(path)  # 判断是否存在这个文件夹
    if not isExists:  # 如果不存在则创建
        os.makedirs(path)
    path = "./数据库"
    isExists = os.path.exists(path)  # 判断是否存在这个文件夹
    if not isExists:  # 如果不存在则创建
        os.makedirs(path)

if __name__ == "__main__":
    gl.init()  # 全局变量
    File_creation()
    app = QApplication(sys.argv)
    Main = Software_interface.Qtmainwin()
    Data_creation = Software_interface.Database_class(Main)
    Main.Create_database.clicked.connect(Data_creation.initUI)
    Data_analysis = Software_interface.Data_analysis_class(Main)
    Main.Data_analysis.clicked.connect(Data_analysis.initUI)
    sys.exit(app.exec_())
