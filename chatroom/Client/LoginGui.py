from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QPushButton, QLineEdit, QLabel
from PyQt5.QtCore import pyqtSignal, Qt, QRegExp, QRect
from PyQt5.QtGui import QFont, QRegExpValidator,QPixmap
from RegisterGui import RegisterGui


# 登陆界面
class LoginGui(QDialog):
    loginRequestSignal = pyqtSignal(str)  # 登陆请求
    registerRequestSignal = pyqtSignal(str)  # 注册请求
    registerSuccessSignal = pyqtSignal(str)  # 注册是否成功

    def __init__(self, parent=None):
        super().__init__(parent)

        # 界面基本设置
        self.lab = QLabel('背景图片', self)
        self.lab.setGeometry(0, 0, 500, 313)
        pixmap = QPixmap('image/background/login.jpg')
        self.lab.setPixmap(pixmap)

        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setAttribute(Qt.WA_QuitOnClose, True)
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        # 设置标题和大小
        self.setWindowTitle(self.tr("i Chat登陆"))
        self.setFixedSize(464, 254)

        # 移动到屏幕中央
        rect = self.frameGeometry()
        rect.moveCenter(QApplication.desktop().availableGeometry().center())
        self.move(rect.topLeft())

        # UI设置
        self.initUI()

    def initUI(self):
        # 控件+布局
        infoLabel = QLabel(self)
        infoLabel.setAlignment(Qt.AlignCenter)
        infoLabel.setFont(QFont("微软雅黑", 20, 50))
        infoLabel.setText(self.tr("请输入账号和密码登陆"))
        infoLabel.resize(infoLabel.sizeHint())
        infoLabel.move(self.width() / 2 - infoLabel.width() / 2, 10)

        idLabel = QLabel(self)
        idLabel.setGeometry(QRect(60, 50, 101, 71))
        idLabel.setFont(QFont("微软雅黑", 18, 50))
        idLabel.setText(self.tr("账号"))

        passwordLabel = QLabel(self)
        passwordLabel.setGeometry(QRect(60, 110, 111, 71))
        passwordLabel.setFont(QFont("微软雅黑", 18, 50))
        passwordLabel.setText(self.tr("密码"))

        self.idLineEdit = QLineEdit(self)
        self.idLineEdit.setValidator(QRegExpValidator(QRegExp("^[-_0-9a-zA-Z@.]{3,15}$"), self.idLineEdit))  # 只能够输入普通字符
        self.idLineEdit.setGeometry(QRect(140, 70, 281, 41))
        self.idLineEdit.setFont(QFont("微软雅黑", 18, 50))
        self.idLineEdit.setStyleSheet("border:2px groove gray;border-radius:10px;padding:2px 4px")

        self.passwordLineEdit = QLineEdit(self)
        self.passwordLineEdit.setValidator(QRegExpValidator(QRegExp("^[_0-9a-zA-Z]{3,15}$"), self.idLineEdit))  # 只能够输入普通字符
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)
        self.passwordLineEdit.setGeometry(QRect(140, 130, 281, 41))
        self.passwordLineEdit.setFont(QFont("微软雅黑", 18, 50))
        self.passwordLineEdit.setStyleSheet("border:2px groove gray;border-radius:10px;padding:2px 4px")

        loginButton = QPushButton(self)
        loginButton.setDefault(True)
        loginButton.setText(self.tr("登陆"))
        loginButton.setGeometry(QRect(100, 190, 91, 41))
        loginButton.setFont(QFont("微软雅黑", 18, 50))
        loginButton.clicked.connect(self.loginButtonClicked)
        loginButton.setStyleSheet(
            "background:rgb(82,163,215);border:2px groove gray;border-radius:10px;padding:2px 4px")

        registerButton = QPushButton(self)
        registerButton.setText(self.tr("注册"))
        registerButton.setGeometry(QRect(260, 190, 91, 41))
        registerButton.setFont(QFont("微软雅黑", 18, 50))
        registerButton.clicked.connect(self.registerButtonClicked)
        registerButton.setStyleSheet(
            "background:rgb(82,163,215);border:2px groove gray;border-radius:10px;padding:2px 4px")

    # 单击登陆按钮
    def loginButtonClicked(self):
        if self.idLineEdit.text() == "" or self.passwordLineEdit.text() == "":
            QMessageBox.warning(self, self.tr("警告"), self.tr("账号或密码不可为空！"))
        else:
            self.loginRequestSignal.emit(self.idLineEdit.text() + ' ' + self.passwordLineEdit.text())

    # 单击注册按钮
    def registerButtonClicked(self):
        registerGui = RegisterGui()
        registerGui.registerRequestSignal.connect(self.registerRequestSignal)  # 注册请求
        self.registerSuccessSignal.connect(registerGui.registerSuccessSlot)  # 注册是否成功
        registerGui.exec()

    # 服务器连接失败
    def connectedFailedSlot(self):
        QMessageBox.critical(self, "错误", "连接服务器失败！")
        self.close()

    # 登陆失败
    def loginFailedSlot(self):
        QMessageBox.critical(self, "错误", "用户名或密码错误！")

    # 重复登陆
    def loginRepeatSlot(self):
        QMessageBox.critical(self, "错误", "该用户已经登陆！")
if __name__=='__main__':
    import sys
    app = QApplication(sys.argv)
    ui = LoginGui()
    ui.show()
    sys.exit(app.exec_())
