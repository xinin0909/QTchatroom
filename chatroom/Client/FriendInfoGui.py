from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QLineEdit, QTextEdit, QPushButton
from PyQt5.QtCore import pyqtSignal, Qt, QRect
from PyQt5.QtGui import QFont,QPixmap
from Extern import UserInfo


# 修改个人信息的界面
class FriendInfoGui(QWidget):
    closeSignal = pyqtSignal()  # 界面关闭的时候发出的信号

    def __init__(self, friend_info=UserInfo(0), parent=None):
        super().__init__(parent)

        self.friendInfo = friend_info  # 好友的用户信息

        # 界面基本设置
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setAttribute(Qt.WA_QuitOnClose, False)

        # 设置标题
        self.setWindowTitle(self.tr("好友信息"))
        self.setFixedSize(743, 529)

        self.initUI()  # UI设置

        # 移动到屏幕中央
        self.resize(self.sizeHint())
        rect = self.frameGeometry()
        rect.moveCenter(QApplication.desktop().availableGeometry().center())
        self.move(rect.topLeft())

    def initUI(self):
        font = QFont("微软雅黑", 16, 20)

        # 控件
        self.lab = QLabel('背景图片', self)
        self.lab.setGeometry(0, 0, 1024,768)
        pixmap = QPixmap('image/background/register.jpg')
        self.lab.setPixmap(pixmap)

        nicknameLabel = QLabel(self)
        nicknameLabel.setGeometry(QRect(40, 20, 81, 31))
        nicknameLabel.setFont(font)
        nicknameLabel.setText(self.tr("昵称："))

        self.nameLineEdit = QLineEdit(self)
        self.nameLineEdit.setGeometry(QRect(120, 20, 220, 30))
        self.nameLineEdit.setFont(font)
        self.nameLineEdit.setReadOnly(True)
        self.nameLineEdit.setText(self.friendInfo.nick_name)
        self.nameLineEdit.setStyleSheet("border:2px groove gray;border-radius:10px;padding:2px 4px")

        mailLabel = QLabel(self)
        mailLabel.setGeometry(QRect(40, 70, 81, 31))
        mailLabel.setFont(font)
        mailLabel.setText(self.tr("邮箱："))

        self.mailLineEdit = QLineEdit(self)
        self.mailLineEdit.setGeometry(QRect(120, 70, 220, 30))
        self.mailLineEdit.setFont(font)
        self.mailLineEdit.setReadOnly(True)
        self.mailLineEdit.setText(self.friendInfo.mail)
        self.mailLineEdit.setStyleSheet("border:2px groove gray;border-radius:10px;padding:2px 4px")

        signLabel = QLabel(self)
        signLabel.setGeometry(QRect(385, 10, 111, 51))
        signLabel.setFont(font)
        signLabel.setText(self.tr("个性签名："))

        self.signTextEdit = QTextEdit(self)
        self.signTextEdit.setGeometry(QRect(390, 70, 321, 331))
        self.signTextEdit.setFont(font)
        self.signTextEdit.setReadOnly(True)
        self.signTextEdit.setText(self.friendInfo.signature)
        self.signTextEdit.setStyleSheet('border:4px solid #A3DCED;border-radius:10px;padding:0px 0px')

        genderLabel = QLabel(self)
        genderLabel.setGeometry(QRect(40, 120, 63, 22))
        genderLabel.setFont(font)
        genderLabel.setText(self.tr("性别："))

        self.genderLineEdit = QLineEdit(self)
        self.genderLineEdit.setGeometry(QRect(120, 120, 220, 30))
        self.genderLineEdit.setFont(font)
        self.genderLineEdit.setReadOnly(True)
        if self.friendInfo.gender == 1:
            self.genderLineEdit.setText("男")
        elif self.friendInfo.gender == 2:
            self.genderLineEdit.setText("女")
        elif self.friendInfo.gender == 3:
            self.genderLineEdit.setText("保密")
        self.genderLineEdit.setStyleSheet("border:2px groove gray;border-radius:10px;padding:2px 4px")

        ageLabel = QLabel(self)
        ageLabel.setGeometry(QRect(40, 170, 63, 22))
        ageLabel.setFont(font)
        ageLabel.setText(self.tr("年龄："))

        self.ageLineEdit = QLineEdit(self)
        self.ageLineEdit.setGeometry(QRect(120, 170, 220, 30))
        self.ageLineEdit.setFont(font)
        self.ageLineEdit.setReadOnly(True)
        self.ageLineEdit.setText(str(self.friendInfo.age))
        self.ageLineEdit.setStyleSheet("border:2px groove gray;border-radius:10px;padding:2px 4px")

        birthLabel = QLabel(self)
        birthLabel.setGeometry(QRect(40, 210, 61, 41))
        birthLabel.setFont(font)
        birthLabel.setText(self.tr("生日："))

        self.birthLineEdit = QLineEdit(self)
        self.birthLineEdit.setGeometry(QRect(120, 220, 220, 30))
        self.birthLineEdit.setFont(font)
        self.birthLineEdit.setReadOnly(True)
        self.birthLineEdit.setText(self.friendInfo.birthday)
        self.birthLineEdit.setStyleSheet("border:2px groove gray;border-radius:10px;padding:2px 4px")

        vocationLabel = QLabel(self)
        vocationLabel.setGeometry(QRect(40, 270, 63, 22))
        vocationLabel.setFont(font)
        vocationLabel.setText(self.tr("职业："))

        self.vocationLineEdit = QLineEdit(self)
        self.vocationLineEdit.setGeometry(QRect(120, 270, 220, 30))
        self.vocationLineEdit.setFont(font)
        self.vocationLineEdit.setReadOnly(True)
        self.vocationLineEdit.setText(self.friendInfo.vocation)
        self.vocationLineEdit.setStyleSheet("border:2px groove gray;border-radius:10px;padding:2px 4px")

        cityLabel = QLabel(self)
        cityLabel.setGeometry(QRect(40, 320, 63, 22))
        cityLabel.setFont(font)
        cityLabel.setText(self.tr("城市："))

        self.cityLineEdit = QLineEdit(self)
        self.cityLineEdit.setGeometry(QRect(120, 320, 220, 30))
        self.cityLineEdit.setFont(font)
        self.cityLineEdit.setReadOnly(True)
        self.cityLineEdit.setText("北京")
        self.cityLineEdit.setStyleSheet("border:2px groove gray;border-radius:10px;padding:2px 4px")

        timeLabel = QLabel(self)
        timeLabel.setGeometry(QRect(40, 370, 100, 22))
        timeLabel.setFont(font)
        timeLabel.setText(self.tr("注册时间："))

        self.timeLineEdit = QLineEdit(self)
        self.timeLineEdit.setGeometry(QRect(160, 370, 180, 30))
        self.timeLineEdit.setFont(font)
        self.timeLineEdit.setReadOnly(True)
        self.timeLineEdit.setText(self.friendInfo.register_time)
        self.timeLineEdit.setStyleSheet("border:2px groove gray;border-radius:10px;padding:2px 4px")

        setButton = QPushButton(self)
        setButton.setText(self.tr("关闭"))
        setButton.setGeometry(QRect(300, 450, 140, 40))
        setButton.setFont(font)
        setButton.clicked.connect(self.closeButtonClicked)
        setButton.setStyleSheet("background:rgb(82,163,215);border:2px groove gray;border-radius:10px;padding:2px 4px")

    # 关闭界面的时候
    def closeEvent(self, QCloseEvent):
        self.closeSignal.emit()
        return super().closeEvent(QCloseEvent)

    # 单击关闭按钮
    def closeButtonClicked(self):
        self.close()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = FriendInfoGui()
    ui.show()
    app.exec()
