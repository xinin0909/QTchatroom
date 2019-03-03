from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QLineEdit,QTextEdit, QPushButton, QMessageBox, QRadioButton
from PyQt5.QtCore import pyqtSignal, Qt, QRect, QRegExp
from PyQt5.QtGui import QFont, QRegExpValidator,QPixmap
from Extern import UserInfo


# 修改个人信息的界面
class MyInfoGui(QWidget):
    closeSignal = pyqtSignal()  # 界面关闭的时候发出的信号
    setMyInfoSignal = pyqtSignal(dict)  # 修改个人信息请求信号

    def __init__(self, my_info=UserInfo(0), parent=None):
        super().__init__(parent)

        self.myInfo = my_info  # 自己的用户信息

        # 界面基本设置
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setAttribute(Qt.WA_QuitOnClose, False)

        # 设置标题
        self.setWindowTitle(self.tr("个人信息"))
        self.setFixedSize(743, 579)

        self.initUI()  # UI设置

        # 移动到屏幕中央
        self.resize(self.sizeHint())
        rect = self.frameGeometry()
        rect.moveCenter(QApplication.desktop().availableGeometry().center())
        self.move(rect.topLeft())

    def initUI(self):
        font = QFont("微软雅黑", 16, 20)

        # 控件
        self.lab=QLabel('背景图片',self)
        self.lab.setGeometry(0,0,1024,768)
        pixmap =QPixmap('image/background/register.jpg')
        self.lab.setPixmap(pixmap)

        nicknameLabel = QLabel(self)
        nicknameLabel.setGeometry(QRect(40, 20, 81, 31))
        nicknameLabel.setFont(font)
        nicknameLabel.setText(self.tr("昵称："))

        self.nameLineEdit = QLineEdit(self)
        self.nameLineEdit.setValidator(
            QRegExpValidator(QRegExp(r"\S+"), self.nameLineEdit))
        self.nameLineEdit.setGeometry(QRect(120, 20, 220, 30))
        self.nameLineEdit.setFont(font)
        self.nameLineEdit.setText(self.myInfo.nick_name)
        self.nameLineEdit.setStyleSheet("border:2px groove gray;border-radius:10px;padding:2px 4px")

        phoneLabel = QLabel(self)
        phoneLabel.setGeometry(QRect(20, 70, 81, 31))
        phoneLabel.setFont(font)
        phoneLabel.setText(self.tr("手机号："))

        self.phoneLineEdit = QLineEdit(self)
        self.phoneLineEdit.setValidator(
            QRegExpValidator(QRegExp(r"[0-9]{7,11}"), self.phoneLineEdit))
        self.phoneLineEdit.setGeometry(QRect(120, 70, 220, 30))
        self.phoneLineEdit.setFont(font)
        self.phoneLineEdit.setText(self.myInfo.phone)
        self.phoneLineEdit.setStyleSheet("border:2px groove gray;border-radius:10px;padding:2px 4px")

        mailLabel = QLabel(self)
        mailLabel.setGeometry(QRect(40, 120, 63, 22))
        mailLabel.setFont(font)
        mailLabel.setText(self.tr("邮箱："))

        self.mailLineEdit = QLineEdit(self)
        self.mailLineEdit.setValidator(
            QRegExpValidator(QRegExp(r"^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"), self.mailLineEdit))
        self.mailLineEdit.setGeometry(QRect(120, 120, 220, 30))
        self.mailLineEdit.setFont(font)
        self.mailLineEdit.setText(self.myInfo.mail)
        self.mailLineEdit.setStyleSheet("border:2px groove gray;border-radius:10px;padding:2px 4px")


        signLabel = QLabel(self)
        signLabel.setGeometry(QRect(385, 10, 111, 51))
        signLabel.setFont(font)
        signLabel.setText(self.tr("个性签名："))

        self.signTextEdit = QTextEdit(self)
        self.signTextEdit.setGeometry(QRect(390, 70, 321, 381))
        self.signTextEdit.setFont(font)
        self.signTextEdit.setText(self.myInfo.signature)
        self.signTextEdit.setStyleSheet("border:4px groove gray;border-radius:10px;padding:0px 0px")

        genderLabel = QLabel(self)
        genderLabel.setGeometry(QRect(40, 170, 63, 22))
        genderLabel.setFont(font)
        genderLabel.setText(self.tr("性别："))

        self.manradioButton = QRadioButton(self)
        self.manradioButton.setGeometry(QRect(130, 170, 51, 28))
        # self.manradioButton.setCheckable(True)
        # self.manradioButton.setChecked(True)
        self.manradioButton.setFont(font)
        self.manradioButton.setText("男")

        self.femaleradioButton = QRadioButton(self)
        self.femaleradioButton.setGeometry(QRect(200, 170, 51, 28))
        self.femaleradioButton.setFont(font)
        self.femaleradioButton.setText("女")

        self.sradioButton = QRadioButton(self)
        self.sradioButton.setGeometry(QRect(270, 170, 70, 28))
        self.sradioButton.setFont(font)
        self.sradioButton.setText("保密")

        gender_id = self.myInfo.gender
        if gender_id == 1:
            self.manradioButton.setChecked(True)
        elif gender_id == 2:
            self.femaleradioButton.setChecked(True)
        elif gender_id == 3:
            self.sradioButton.setChecked(True)

        ageLabel = QLabel(self)
        ageLabel.setGeometry(QRect(40, 220, 63, 22))
        ageLabel.setFont(font)
        ageLabel.setText(self.tr("年龄："))

        self.ageLineEdit = QLineEdit(self)
        self.ageLineEdit.setValidator(QRegExpValidator(QRegExp(r"\S+"), self.ageLineEdit))
        self.ageLineEdit.setGeometry(QRect(120, 220, 220, 30))
        self.ageLineEdit.setFont(font)
        self.ageLineEdit.setReadOnly(True)
        self.ageLineEdit.setText(str(self.myInfo.age))
        self.ageLineEdit.setStyleSheet("border:2px groove gray;border-radius:10px;padding:2px 4px")

        birthLabel = QLabel(self)
        birthLabel.setGeometry(QRect(40, 260, 61, 41))
        birthLabel.setFont(font)
        birthLabel.setText(self.tr("生日："))

        self.birthLineEdit = QLineEdit(self)
        self.birthLineEdit.setValidator(QRegExpValidator(QRegExp(r"^\d{4}-\d{1,2}-\d{1,2}"), self.birthLineEdit))
        self.birthLineEdit.setGeometry(QRect(120, 270, 220, 30))
        self.birthLineEdit.setFont(font)
        self.birthLineEdit.setText(self.myInfo.birthday)
        self.birthLineEdit.setStyleSheet("border:2px groove gray;border-radius:10px;padding:2px 4px")

        vocationLabel = QLabel(self)
        vocationLabel.setGeometry(QRect(40, 320, 63, 22))
        vocationLabel.setFont(font)
        vocationLabel.setText(self.tr("职业："))

        self.vocationLineEdit = QLineEdit(self)
        self.vocationLineEdit.setValidator(QRegExpValidator(QRegExp(r"\S+"), self.vocationLineEdit))
        self.vocationLineEdit.setGeometry(QRect(120, 320, 220, 30))
        self.vocationLineEdit.setFont(font)
        self.vocationLineEdit.setText(self.myInfo.vocation)
        self.vocationLineEdit.setStyleSheet("border:2px groove gray;border-radius:10px;padding:2px 4px")

        cityLabel = QLabel(self)
        cityLabel.setGeometry(QRect(40, 370, 63, 22))
        cityLabel.setFont(font)
        cityLabel.setText(self.tr("城市："))

        self.cityLineEdit = QLineEdit(self)
        self.cityLineEdit.setValidator(QRegExpValidator(QRegExp(r"\S+"), self.cityLineEdit))
        self.cityLineEdit.setGeometry(QRect(120, 370, 220, 30))
        self.cityLineEdit.setFont(font)
        self.cityLineEdit.setText("北京")
        self.cityLineEdit.setReadOnly(True)
        self.cityLineEdit.setStyleSheet("border:2px groove gray;border-radius:10px;padding:2px 4px")

        timeLabel = QLabel(self)
        timeLabel.setGeometry(QRect(40, 420, 100, 22))
        timeLabel.setFont(font)
        timeLabel.setText(self.tr("注册时间："))

        self.timeLineEdit = QLineEdit(self)
        self.timeLineEdit.setGeometry(QRect(160, 420, 180, 30))
        self.timeLineEdit.setFont(font)
        self.timeLineEdit.setReadOnly(True)
        self.timeLineEdit.setText(self.myInfo.register_time)
        self.timeLineEdit.setStyleSheet("border:2px groove gray;border-radius:10px;padding:2px 4px")

        setButton = QPushButton(self)
        setButton.setText(self.tr("保存"))
        setButton.setGeometry(QRect(300, 500, 140, 40))
        setButton.setFont(font)
        setButton.clicked.connect(self.setButtonClicked)
        setButton.setStyleSheet("border:2px groove gray;border-radius:10px;padding:2px 4px")

    # 关闭界面的时候
    def closeEvent(self, QCloseEvent):
        self.closeSignal.emit()
        return super().closeEvent(QCloseEvent)

    # 单击保存按钮
    def setButtonClicked(self):
        my_info_dict = dict()
        my_info_dict['nick_name'] = self.nameLineEdit.text()
        my_info_dict['signature'] = self.signTextEdit.toPlainText()
        if self.manradioButton.isChecked():
            my_info_dict['gender_id'] = 1
        elif self.femaleradioButton.isChecked():
            my_info_dict['gender_id'] = 2
        elif self.sradioButton.isChecked():
            my_info_dict['gender_id'] = 3
        else:
            my_info_dict['gender_id'] = 3
        my_info_dict['birthday'] = self.birthLineEdit.text()
        my_info_dict['age'] = int(self.ageLineEdit.text())
        my_info_dict['telephone'] = self.phoneLineEdit.text()
        my_info_dict['email'] = self.mailLineEdit.text()
        my_info_dict['vocation'] = self.vocationLineEdit.text()
        self.setMyInfoSignal.emit(my_info_dict)

    # 返回修改是否成功
    def updateMyInfoStatusSlot(self, status):
        if status == '0':
            QMessageBox.information(self, self.tr("成功"), self.tr("保存成功！"))
            self.close()
        else:
            QMessageBox.critical(self, self.tr("失败"), self.tr("保存失败！请检查信息是否有误！"))


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = MyInfoGui()
    ui.show()
    app.exec()
