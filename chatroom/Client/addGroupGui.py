from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSignal, Qt, QRect, QRegExp
from PyQt5.QtGui import QFont, QRegExpValidator,QPixmap
from Extern import UserInfo


# 修改好友备注的界面
class AddGroupGui(QWidget):
    closeSignal = pyqtSignal()  # 界面关闭的时候发出的信号
    addGroupRequestSignal = pyqtSignal(str)  # 添加群请求信号

    def __init__(self, parent=None):
        super().__init__(parent)

        self.myInfo = UserInfo(0)  # 自己的用户信息

        # 界面基本设置
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setAttribute(Qt.WA_QuitOnClose, False)

        # 设置标题
        self.setWindowTitle(self.tr("添加群"))
        self.setFixedSize(464, 204)

        self.initUI()  # UI设置

        # 移动到屏幕中央
        self.resize(self.sizeHint())
        rect = self.frameGeometry()
        rect.moveCenter(QApplication.desktop().availableGeometry().center())
        self.move(rect.topLeft())

    def initUI(self):
        # 控件
        self.lab = QLabel('背景图片', self)
        self.lab.setGeometry(0, 0, 500, 313)
        pixmap = QPixmap('image/background/login.jpg')
        self.lab.setPixmap(pixmap)

        infoLabel = QLabel(self)
        infoLabel.setGeometry(QRect(100, 5, 350, 70))
        infoLabel.setFont(QFont("微软雅黑", 20, 50))
        infoLabel.setText(self.tr("请输入要加入群名称"))

        idLabel = QLabel(self)
        idLabel.setGeometry(QRect(40, 60, 100, 70))
        idLabel.setFont(QFont("微软雅黑", 18, 50))
        idLabel.setText(self.tr("群名称"))

        self.idLineEdit = QLineEdit(self)
        self.idLineEdit.setValidator(QRegExpValidator(QRegExp(r"\S+"), self.idLineEdit))
        self.idLineEdit.setGeometry(QRect(120, 75, 310, 41))
        self.idLineEdit.setFont(QFont("微软雅黑", 18, 50))
        self.idLineEdit.returnPressed.connect(self.addButtonClicked)
        self.idLineEdit.setStyleSheet("border:2px groove gray;border-radius:10px;padding:2px 4px")

        addButton = QPushButton(self)
        addButton.setText(self.tr("加入"))
        addButton.setGeometry(QRect(180, 140, 91, 41))
        addButton.setFont(QFont("微软雅黑", 18, 50))
        addButton.clicked.connect(self.addButtonClicked)
        addButton.setStyleSheet("border:2px groove gray;border-radius:10px;padding:2px 4px")

    # 关闭界面的时候
    def closeEvent(self, QCloseEvent):
        self.closeSignal.emit()
        return super().closeEvent(QCloseEvent)

    # 单击创建按钮
    def addButtonClicked(self):
        group_name = self.idLineEdit.text()
        self.addGroupRequestSignal.emit(group_name)
        if group_name == "":
            QMessageBox.critical(self, self.tr("失败"), self.tr("群名称不能为空！"))
        else:
            QMessageBox.information(self, self.tr("成功"), self.tr("加入成功！"))
            self.close()
if __name__=='__main__':
    import sys
    app = QApplication(sys.argv)
    ui = AddGroupGui()
    ui.show()
    sys.exit(app.exec_())