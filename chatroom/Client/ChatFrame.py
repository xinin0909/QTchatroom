from PyQt5.QtWidgets import QFrame, QTextEdit, QPushButton, QGridLayout, QMessageBox
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QKeyEvent
from Extern import UserInfo
from filetrans.tcpserver_widget import TcpS


# 聊天面板
class ChatFrame(QFrame):
    sendMsgSignal = pyqtSignal(str)  # 发送聊天消息
    sendFileRequestSignal = pyqtSignal(str)  # 发送文件请求

    def __init__(self, parent=None):
        super().__init__(parent)

        self.myInfo = UserInfo(0)  # 自己的用户信息
        self.friendInfo = UserInfo(0)  # 好友信息
        self.my_host = ""
        self.friend_host = ""

        self.server = TcpS()
        self.server.sendFileName[str].connect(self.getFileName)

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
        self.sendButton.setStyleSheet("color:white;border:2px groove gray;border-radius:10px;padding:2px 4px")

        self.fileButton = QPushButton(self)
        self.fileButton.setFont(QFont("微软雅黑", 16, 30))
        self.fileButton.setText(self.tr("发送文件"))
        self.fileButton.resize(self.sendButton.sizeHint())
        self.fileButton.clicked.connect(self.fileButtonClicked)
        self.fileButton.setStyleSheet("color:white;border:2px groove gray;border-radius:10px;padding:2px 4px")

        # 布局
        self.layout = QGridLayout(self)
        self.layout.addWidget(self.recvTextEdit, 0, 0, 20, 10)
        self.layout.addWidget(self.sendTextEdit, 20, 0, 10, 10)
        self.layout.addWidget(self.sendButton, 30, 9, 1, 1)
        self.layout.addWidget(self.fileButton, 30, 0, 1, 2)

    # 单击发送按钮
    def sendButtonClicked(self):
        msg = self.sendTextEdit.toPlainText()
        if msg != "":
            self.sendTextEdit.clear()
            self.recvTextEdit.append(self.tr("我") + "：" + msg)
            self.sendMsgSignal.emit(self.friendInfo.id + " " + msg)
            filename = './cache/' + '-'.join(['f', self.myInfo.id, self.friendInfo.id]) + '.txt'
            f_file = open(filename, 'a', encoding="utf8")
            f_file.write("我" + "：" + msg + '\n')
            f_file.close()

    # 获取聊天消息
    def getMsgSlot(self, msgInfoList):
        if msgInfoList[0] == self.friendInfo.id:
            filename = './cache/' + '-'.join(['f', self.myInfo.id, self.friendInfo.id]) + '.txt'
            f_file = open(filename, 'a', encoding="utf8")
            if self.friendInfo.mark_name:
                self.recvTextEdit.append("%s：%s" % (self.friendInfo.mark_name, msgInfoList[1]))
                f_file.write("%s：%s" % (self.friendInfo.mark_name, msgInfoList[1]) + '\n')
            else:
                self.recvTextEdit.append("%s：%s" % (self.friendInfo.name, msgInfoList[1]))
                f_file.write("%s：%s" % (self.friendInfo.name, msgInfoList[1]) + '\n')
            f_file.close()


    # 使得回车能够发送消息，shift键+回车可以换行
    def eventFilter(self, watched, event):
        if watched == self.sendTextEdit:  # 如果目标对象为发送文本框
            if type(event) == QKeyEvent:  # 如果事件为按键事件
                if event.key() == Qt.Key_Return and event.modifiers() == Qt.NoModifier:  # 如果为单纯的回车按键
                    self.sendButtonClicked()  # 发送
                    return True  # 表示已经处理过这个事件
        return super().eventFilter(watched, event)

    # 点击发送文件按钮
    def fileButtonClicked(self):
        # self.server.exec()
        if self.friend_host == "":
            QMessageBox.information(self, "提示", "好友当前不在线，不能发送文件！")
        elif self.my_host == self.friend_host:
            QMessageBox.information(self, "提示", "不能发送给本机！")
        elif self.my_host == "127.0.0.1":
            QMessageBox.information(self, "提示", "通过127.0.0.1连接的客户端不能发送文件！")
        else:
            self.server.exec()

    # 获取好友ip地址请求
    def getFriendHostSlot(self, host):
        self.friend_host = host

    def getFileName(self, name):
        """
        待传输文件的文件名
        """
        self.filename = name
        self.sendFileRequestSignal.emit(self.friendInfo.id + " " + self.filename)

    # 拒绝接收文件
    def refuseRecvFileSlot(self, msgList):
        friend_name = msgList[1]
        user_name = msgList[2]
        if self.myInfo.name == user_name and self.friendInfo.name == friend_name:
            self.server.refused()

