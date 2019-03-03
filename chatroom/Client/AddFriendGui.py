from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSignal, Qt, QRegExp, QRect
from PyQt5.QtGui import QFont, QRegExpValidator,QPixmap
from Extern import UserInfo


# 添加好友的界面
class AddFriendGui(QWidget):
    closeSignal = pyqtSignal()  # 界面关闭的时候发出的信号
    addFriendRequestSignal = pyqtSignal(str)  # 添加好友请求信号

    def __init__(self, parent=None):
        super().__init__(parent)

        self.myInfo = UserInfo(0)  # 自己的用户信息

        # 界面基本设置
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setAttribute(Qt.WA_QuitOnClose, False)

        # 设置标题
        self.setWindowTitle(self.tr("添加好友"))
        self.setFixedSize(464, 254)

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
        infoLabel.setGeometry(QRect(60, 10, 360, 70))
        infoLabel.setFont(QFont("微软雅黑", 20, 50))
        infoLabel.setText(self.tr("请输入要添加的好友的用户名"))

        idLabel = QLabel(self)
        idLabel.setGeometry(QRect(40, 90, 100, 70))
        idLabel.setFont(QFont("微软雅黑", 18, 50))
        idLabel.setText(self.tr("用户名"))

        self.idLineEdit = QLineEdit(self)
        self.idLineEdit.setValidator(QRegExpValidator(QRegExp("^[-_0-9a-zA-Z]{3,15}$"), self.idLineEdit))
        self.idLineEdit.setGeometry(QRect(120, 105, 310, 41))
        self.idLineEdit.setFont(QFont("微软雅黑", 18, 50))
        self.idLineEdit.returnPressed.connect(self.addButtonClicked)
        self.idLineEdit.setStyleSheet("border:2px groove gray;border-radius:10px;padding:2px 4px")

        addButton = QPushButton(self)
        addButton.setText(self.tr("添加"))
        addButton.setGeometry(QRect(200, 190, 91, 41))
        addButton.setFont(QFont("微软雅黑", 18, 50))
        addButton.clicked.connect(self.addButtonClicked)
        addButton.setStyleSheet("border:2px groove gray;border-radius:10px;padding:2px 4px")

    # 关闭界面的时候
    def closeEvent(self, QCloseEvent):
        self.closeSignal.emit()
        return super().closeEvent(QCloseEvent)

    # 单击添加按钮
    def addButtonClicked(self):
        friend_name = self.idLineEdit.text()  # 获取要添加的好友ID
        # 如果要添加的好友用户名为空
        if friend_name == "":
            QMessageBox.critical(self, self.tr("错误"), self.tr("要添加的好友用户名不可为空！"))
        # 如果要添加自己为好友
        elif friend_name == self.myInfo.name:
            QMessageBox.critical(self, self.tr("错误"), self.tr("不可添加自己为好友！"))
        # 否则发送请求
        else:
            self.addFriendRequestSignal.emit(friend_name)

    # 已经添加这个好友
    def friendExistedSlot(self):
        QMessageBox.critical(self, self.tr("已经添加"), self.tr("你已经添加了这个好友！"))

    # 要添加的好友id不存在
    def noThisUserSlot(self, msg):
        if msg == "0":
            QMessageBox.information(self, self.tr("成功"), self.tr("添加成功！"))
            self.close()
        elif msg == "1":
            QMessageBox.critical(self, self.tr("错误"), self.tr("添加失败！"))
if __name__=='__main__':
    import sys
    app = QApplication(sys.argv)
    ui = AddFriendGui()
    ui.show()
    sys.exit(app.exec_())