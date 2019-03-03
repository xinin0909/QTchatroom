from PyQt5.QtWidgets import QDialog, QApplication, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSignal, Qt, QRect, QRegExp
from PyQt5.QtGui import QFont, QRegExpValidator,QPixmap


# 注册界面
class RegisterGui(QDialog):
    registerRequestSignal = pyqtSignal(str)  # 注册请求

    def __init__(self, parent=None):
        super().__init__(parent)

        # 界面基本设置
        self.lab = QLabel('背景图片', self)
        self.lab.setGeometry(0, 0, 1024,768)
        pixmap = QPixmap('image/background/register.jpg')
        self.lab.setPixmap(pixmap)

        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setAttribute(Qt.WA_QuitOnClose, False)
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        # 设置标题和大小
        self.setWindowTitle(self.tr("i Chat注册"))
        self.setFixedSize(516, 402)

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
        infoLabel.setFont(QFont("微软雅黑", 20))
        infoLabel.setText(self.tr("请输入注册信息"))
        infoLabel.resize(infoLabel.sizeHint())
        infoLabel.move(self.width() / 2 - infoLabel.width() / 2, 10)

        nameLabel = QLabel(self)
        nameLabel.setFont(QFont("微软雅黑", 18, 10))
        nameLabel.setText(self.tr("用户名"))
        nameLabel.setGeometry(QRect(100, 70, 91, 41))

        passwordLabel1 = QLabel(self)
        passwordLabel1.setFont(QFont("微软雅黑", 18, 10))
        passwordLabel1.setText(self.tr("密码"))
        passwordLabel1.setGeometry(QRect(120, 120, 91, 51))

        passwordLabel2 = QLabel(self)
        passwordLabel2.setFont(QFont("微软雅黑", 18, 10))
        passwordLabel2.setText(self.tr("再次输入密码"))
        passwordLabel2.setGeometry(QRect(25, 180, 161, 51))

        mailLabel = QLabel(self)
        mailLabel.setFont(QFont("微软雅黑", 18, 10))
        mailLabel.setText(self.tr("邮箱"))
        mailLabel.setGeometry(QRect(120, 240, 91, 51))

        self.nameLineEdit = QLineEdit(self)
        self.nameLineEdit.setValidator(QRegExpValidator(QRegExp("^[-_0-9a-zA-Z]{3,15}$"), self.nameLineEdit))  # 只能够输入普通字符
        self.nameLineEdit.setGeometry(QRect(200, 70, 261, 41))
        self.nameLineEdit.setFont(QFont("微软雅黑", 18, 50))
        self.nameLineEdit.setStyleSheet(
            "border:2px groove gray;border-radius:10px;padding:2px 4px")

        self.passwordLineEdit1 = QLineEdit(self)
        self.passwordLineEdit1.setEchoMode(QLineEdit.Password)
        self.passwordLineEdit1.setValidator(QRegExpValidator(QRegExp("^[_0-9a-zA-Z]{3,15}$"), self.passwordLineEdit1))
        self.passwordLineEdit1.setGeometry(QRect(200, 130, 261, 41))
        self.passwordLineEdit1.setFont(QFont("微软雅黑", 18, 50))
        self.passwordLineEdit1.setStyleSheet(
            "border:2px groove gray;border-radius:10px;padding:2px 4px")

        self.passwordLineEdit2 = QLineEdit(self)
        self.passwordLineEdit2.setEchoMode(QLineEdit.Password)
        self.passwordLineEdit2.setValidator(QRegExpValidator(QRegExp("^[_0-9a-zA-Z]{3,15}$"), self.passwordLineEdit2))
        self.passwordLineEdit2.setGeometry(QRect(200, 190, 261, 41))
        self.passwordLineEdit2.setFont(QFont("微软雅黑", 18, 50))
        self.passwordLineEdit2.setStyleSheet(
            "border:2px groove gray;border-radius:10px;padding:2px 4px")

        self.mailLineEdit = QLineEdit(self)
        self.mailLineEdit.setValidator(QRegExpValidator(QRegExp("^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"), self.mailLineEdit))
        self.mailLineEdit.setGeometry(QRect(200, 250, 261, 41))
        self.mailLineEdit.setFont(QFont("微软雅黑", 18, 50))
        self.mailLineEdit.setStyleSheet(
            "border:2px groove gray;border-radius:10px;padding:2px 4px")

        registerButton = QPushButton(self)
        registerButton.setDefault(True)
        registerButton.setText(self.tr("注册"))
        registerButton.setGeometry(QRect(200, 320, 121, 41))
        registerButton.setFont(QFont("微软雅黑", 18, 50))
        registerButton.clicked.connect(self.registerButtonClicked)
        registerButton.setStyleSheet(
            "border:2px groove gray;border-radius:10px;padding:2px 4px")

    # 单击注册按钮
    def registerButtonClicked(self):
        if self.nameLineEdit.text() == "" or self.passwordLineEdit1.text() == "":
            QMessageBox.warning(self, self.tr("警告"), self.tr("用户名或密码不可为空！"))
        elif self.passwordLineEdit1.text() != self.passwordLineEdit2.text():
            QMessageBox.warning(self, self.tr("警告"), self.tr("两次密码输入不一致！"))
        else:
            msg = self.nameLineEdit.text() + ' ' + self.passwordLineEdit2.text() + ' ' + self.mailLineEdit.text()
            self.registerRequestSignal.emit(msg)
            self.nameLineEdit.clear()
            self.passwordLineEdit1.clear()
            self.passwordLineEdit2.clear()
            self.mailLineEdit.clear()

    # 注册是否成功
    def registerSuccessSlot(self, id):
        if id:
            QMessageBox.about(self, "注册成功", "注册成功！你的新ID是 %s" % id)
        else:
            QMessageBox.about(self, "注册失败", "注册失败！请重试！")
if __name__=='__main__':
    import sys
    app = QApplication(sys.argv)
    ui = RegisterGui()
    ui.show()
    sys.exit(app.exec_())