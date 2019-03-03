from PyQt5.QtWidgets import QFrame, QTextEdit, QPushButton, QGridLayout
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QKeyEvent
from Extern import UserInfo


# 聊天面板
class GroupFrame(QFrame):
    sendGroupMsgSignal = pyqtSignal(str)  # 发送聊天消息

    def __init__(self, parent=None):
        super().__init__(parent)

        self.myInfo = UserInfo(0)  # 自己的用户信息
        self.friendInfo = UserInfo(1)  # 群信息

        self.initUI()  # UI设置

    def initUI(self):
        # 控件
        self.sendTextEdit = QTextEdit(self)
        self.sendTextEdit.setFont(QFont("微软雅黑", 14, 10))
        self.sendTextEdit.installEventFilter(self)  # 加装事件过滤器
        self.sendTextEdit.setStyleSheet("border:2px groove white;border-radius:10px;padding:0px 0px")

        self.recvTextEdit = QTextEdit(self)
        self.recvTextEdit.setFont(QFont("微软雅黑", 14, 10))
        self.recvTextEdit.setReadOnly(True)
        self.recvTextEdit.setStyleSheet("border:2px groove white;border-radius:10px;padding:0px 0px")

        self.sendButton = QPushButton(self)
        self.sendButton.setFont(QFont("微软雅黑", 16, 30))
        self.sendButton.setText(self.tr("发送"))
        self.sendButton.resize(self.sendButton.sizeHint())
        self.sendButton.clicked.connect(self.sendButtonClicked)
        self.sendButton.setStyleSheet("color:white ;border:2px groove gray;border-radius:10px;padding:2px 4px")

        # 布局
        self.layout = QGridLayout(self)
        self.layout.addWidget(self.recvTextEdit, 0, 0, 20, 10)
        self.layout.addWidget(self.sendTextEdit, 20, 0, 10, 10)
        self.layout.addWidget(self.sendButton, 30, 9, 1, 1)

    # 单击发送按钮
    def sendButtonClicked(self):
        msg = self.sendTextEdit.toPlainText()
        if msg != "":
            self.sendTextEdit.clear()
            self.recvTextEdit.append(self.tr("我") + "：" + msg)
            self.sendGroupMsgSignal.emit("{} {} {}".format(self.friendInfo.nick_name, self.myInfo.id, msg))
            filename = './cache/' + '-'.join(['g', self.myInfo.id, self.friendInfo.nick_name]) + '.txt'
            g_file = open(filename, 'a', encoding="utf8")
            g_file.write("我" + "：" + msg + '\n')
            g_file.close()

    # 获取聊天消息
    def getGroupMsgSlot(self, msgInfoList):
        # msgInfoList : group_name, user_name, msg_data
        print(msgInfoList)
        if msgInfoList[0] == self.friendInfo.nick_name:
            self.recvTextEdit.append("%s：%s" % (msgInfoList[1], msgInfoList[2]))
            filename = './cache/' + '-'.join(['g', self.myInfo.id, self.friendInfo.nick_name]) + '.txt'
            g_file = open(filename, 'a', encoding="utf8")
            g_file.write("%s：%s" % (msgInfoList[1], msgInfoList[2]) + '\n')
            g_file.close()

    # 使得回车能够发送消息，shift键+回车可以换行
    def eventFilter(self, watched, event):
        if watched == self.sendTextEdit:  # 如果目标对象为发送文本框
            if type(event) == QKeyEvent:  # 如果事件为按键事件
                if event.key() == Qt.Key_Return and event.modifiers() == Qt.NoModifier:  # 如果为单纯的回车按键
                    self.sendButtonClicked()  # 发送
                    return True  # 表示已经处理过这个事件
        return super().eventFilter(watched, event)
