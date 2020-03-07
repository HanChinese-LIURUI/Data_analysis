#QDialog对话框使用
from PyQt5.QtWidgets import  QVBoxLayout,QWidget,QApplication ,QHBoxLayout,QDialog,QPushButton,QTextEdit

from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import  Qt

import sys

class WindowClass(QWidget):

    def __init__(self,items, data, parent=None):
        super(WindowClass, self).__init__(parent)
        self.count = 0
        self.items = items
        self.data = data
        self.showDialog()



    def showDialog(self):
        vbox=QVBoxLayout()#纵向布局
        hbox=QHBoxLayout()#横向布局
        panel=QTextEdit()
        text = str()
        for item in self.items:
            text += "行号：%s    内容：%s\n" % (item.row() + 1, item.text())
        panel.setPlainText(text)
        self.dialog=QDialog()
        self.dialog.resize(1200,500)
        self.okBtn=QPushButton("上一个")
        self.cancelBtn=QPushButton("跳至下一个")
        self.okBtn.resize(50, 50)
        self.cancelBtn.resize(50, 50)

        #绑定事件
        self.okBtn.clicked.connect(self.ok)
        self.cancelBtn.clicked.connect(self.cancel)

        self.dialog.setWindowTitle("提示信息！")
        #okBtn.move(50,50)#使用layout布局设置，因此move效果失效
        # 确定与取消按钮横向布局
        # hbox.addWidget(self.okBtn)
        hbox.addWidget(self.cancelBtn)

        #消息label与按钮组合纵向布局
        vbox.addWidget(panel)
        vbox.addLayout(hbox)
        self.dialog.setLayout(vbox)
        self.dialog.exec_()



    #槽函数如下：
    def ok(self):
        if self.count < 0:
            print(self.count)
            return 0
        item = self.items[self.count]
        item.setSelected(True)
        # 设置单元格的背脊颜色为红
        # item.setForeground(QBrush(QColor(255, 0, 0)))
        row = item.row()
        self.data.verticalScrollBar().setSliderPosition(row-1)
        self.count -= 1

    def cancel(self):
        if self.count > len(self.items) - 1:
            self.count = 0
        item = self.items[self.count]
        #item.setSelected(True)
        # 设置单元格的背脊颜色为红
        item.setBackground(QBrush(QColor(255, 0, 0)))
        row = item.row()
        self.data.verticalScrollBar().setSliderPosition(row - 1)
        self.count += 1


if __name__=="__main__":
    app=QApplication(sys.argv)
    win=WindowClass()
    sys.exit(app.exec_())