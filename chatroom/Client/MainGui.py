from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QLabel, QToolButton, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt, pyqtSignal, QRect, QSize
from PyQt5.QtNetwork import QHostAddress
from PyQt5.QtGui import QFont, QIcon, QPixmap
from FriendListWidget import FriendListWidget
from ChatFrame import ChatFrame
from GroupFrame import GroupFrame
from MyInfoGui import MyInfoGui
from filetrans.tcpclient_widget import TcpC
from Extern import UserInfo, FriendInfoIndex
import sys

# 主界面
class MainGui(QWidget):
    getFriendListSignal = pyqtSignal(list)  # 获取并更新自己的好友列表

    sendMsgSignal = pyqtSignal(str)  # 发送聊天消息
    getMsgSignal = pyqtSignal(list)  # 获取聊天消息

    sendGroupMsgSignal = pyqtSignal(str)  # 发送群信息
    getGroupMsgSignal = pyqtSignal(list)  # 获取群信息

    addFriendRequestSignal = pyqtSignal(str)  # 添加好友请求
    noThisUserSignal = pyqtSignal(str)  # 添加好友请求返回没有这个用户
    delFriendRequestSignal = pyqtSignal(str)  # 删除好友请求
    setFriendNameRequestSignal = pyqtSignal(str)  # 修改好友备注请求信号
    createGroupRequestSignal = pyqtSignal(str)  # 创建群请求信号
    addGroupRequestSignal = pyqtSignal(str)  # 加入群请求
    quitGroupRequestSignal = pyqtSignal(str)  # 退群请求
    delGroupRequestSignal = pyqtSignal(str)  # 解散群请求

    setMyInfoRequestSignal = pyqtSignal(dict)  # 修改个人详情
    updateMyInfoSignal = pyqtSignal(str)  # 修改个人信息是否成功

    getFriendHostRequestSignal = pyqtSignal(str)  # 获取好友ip地址请求
    getFriendHostSignal = pyqtSignal(str)  # 获取好友ip地址

    sendFileRequestSignal = pyqtSignal(str)  # 发送文件请求
    refuseRecvFile = pyqtSignal(str)  # 拒绝接收文件
    refuseRecvFileSignal = pyqtSignal(list)  # 拒绝接收文件

    def __init__(self):
        super().__init__()

        self.myInfo = UserInfo(0)  # 自己的用户信息
        self.host = ""  # 自己的ip地址
        self.chatFrameList = []  # 已经启动显示的聊天面板
        self.myInfoGui = None

        # 界面基本设置
        self.setAttribute(Qt.WA_DeleteOnClose,True)
        self.setAttribute(Qt.WA_QuitOnClose,True)

        # 设置标题和大小
        self.setWindowTitle(self.tr("i Chat"))
        # 自适应屏幕大小
        screen = QApplication.desktop().availableGeometry()
        self.resize(screen.width() / 5 * 3,screen.height() / 3 * 2)
        self.setMinimumSize(self.size())

        # 移动到屏幕中央
        frame = self.frameGeometry()
        frame.moveCenter(QApplication.desktop().availableGeometry().center())
        self.move(frame.topLeft())

        # UI设置
        self.initUI()
        
    def initUI(self):
        # 内部控件
        self.lab=QLabel('背景图片',self)
        self.lab.setGeometry(0,0,1920,1080)
        pixmap =QPixmap('image/background/maingui.jpg')
        self.lab.setPixmap(pixmap)		

        self.toolButton = QToolButton(self)
        self.toolButton.setGeometry(QRect(15, 15, 50, 50))
        self.toolButton.setText("")
        self.head_icon = QIcon()
        self.toolButton.setIcon(self.head_icon)
        self.toolButton.setIconSize(QSize(70, 70))
        self.toolButton.setObjectName("toolButton")
        self.toolButton.clicked.connect(self.seeMyInfoSlot)

        self.nameLabel = QLabel(self)
        self.nameLabel.setGeometry(QRect(80, 35, 250, 20))
        self.nameLabel.setFont(QFont("微软雅黑", 16, 30))
        self.nameLabel.setText(self.myInfo.nick_name)
        self.nameLabel.setStyleSheet('color:white')

        listLabel = QLabel(self)
        listLabel.setGeometry(QRect(10, 70, 100, 20))
        listLabel.setFont(QFont("微软雅黑", 12, 20))
        listLabel.setText(self.tr("联系人列表"))
        listLabel.setStyleSheet('color:white')

        # 外部控件
        self.friendListWidget = FriendListWidget(self)
        self.friendListWidget.myInfo = self.myInfo
        self.friendListWidget.friendItemClicked.connect(self.friendListWidgetItemClicked)  # 双击好友项出现聊天面板
        self.getFriendListSignal.connect(self.friendListWidget.getFriendListSlot)  # 获取并更新自己的好友列表
        self.friendListWidget.addFriendRequestSignal.connect(self.addFriendRequestSignal)  # 添加好友请求
        self.friendListWidget.setFriendNameRequestSignal.connect(self.setFriendNameRequestSignal)  # 修改备注请求
        self.noThisUserSignal.connect(self.friendListWidget.noThisUserSignal)  # 添加好友请求返回没有这个用户
        self.friendListWidget.delFriendRequestSignal.connect(self.delFriendRequestSignal)  # 删除好友请求
        self.friendListWidget.delChatFrameSignal.connect(self.delChatFrameSlot)  # 在删除好友的时候删除相应的聊天面板
        self.friendListWidget.updateChatFrameSignal.connect(self.updateChatFrameSlot)  # 根据新的聊天面板的id列表更新聊天面板
        self.friendListWidget.createGroupRequestSignal.connect(self.createGroupRequestSignal)  # 创建群请求
        self.friendListWidget.addGroupRequestSignal.connect(self.addGroupRequestSignal)  # 加入群请求
        self.friendListWidget.quitGroupRequestSignal.connect(self.quitGroupRequestSignal)  # 退群请求
        self.friendListWidget.delGroupRequestSignal.connect(self.delGroupRequestSignal)  # 解散群请求

        # 布局
        self.layout = QGridLayout(self)
        self.layout.addWidget(self.friendListWidget, 14, 0, -1, 4)
        self.widget = QWidget(self)
        self.layout.addWidget(self.widget, 0, 4, -1, 12)

    # 获取并设置自己的用户信息和窗口标题
    def getMyInfoSlot(self, myInfo):
        self.myInfo = myInfo
        self.friendListWidget.myInfo = self.myInfo
        title_info = "i Chat（当前用户ID：{}   用户名：{}）".format(self.myInfo.id, self.myInfo.name)
        head_path = r"image/head/{}.bmp".format(int(self.myInfo.id) % 133 + 1)
        self.head_icon.addPixmap(QPixmap(head_path), QIcon.Normal, QIcon.Off)
        self.toolButton.setIcon(self.head_icon)
        self.nameLabel.setText(self.myInfo.nick_name)
        self.setWindowTitle(title_info)

    # 获取自己的ip地址
    def getMyHostSlot(self, host):
        self.host = host

    # 点击头像显示个人详情
    def seeMyInfoSlot(self):
        if self.myInfoGui is None:
            self.myInfoGui = MyInfoGui(self.myInfo)
            self.updateMyInfoSignal.connect(self.myInfoGui.updateMyInfoStatusSlot)
            self.myInfoGui.closeSignal.connect(self.closeMyInfoGuiSlot)  # 关闭个人详情界面
            self.myInfoGui.setMyInfoSignal.connect(self.setMyInfoRequestSlot)  # 修改个人信息请求
            self.myInfoGui.show()

    # 个人详情界面关闭
    def closeMyInfoGuiSlot(self):
        self.myInfoGui = None

    # 修改个人信息请求
    def setMyInfoRequestSlot(self, my_info_dict):
        self.setMyInfoRequestSignal.emit(my_info_dict)

    # 点击好友项显示聊天面板
    def friendListWidgetItemClicked(self, item):
        if item.data(Qt.UserRole + FriendInfoIndex.obj_type) == 0:  # 如果是好友
            # 判定是否相应的聊天面板是否已经打开
            for chatFrame in self.chatFrameList:
                # 如果打开了
                if chatFrame.friendInfo.id == item.data(Qt.UserRole + FriendInfoIndex.id):
                    self.getFriendHostSignal.connect(chatFrame.getFriendHostSlot)  # 获取好友ip地址
                    self.getFriendHostRequestSignal.emit(item.data(Qt.UserRole + FriendInfoIndex.id))
                    self.refuseRecvFileSignal.connect(chatFrame.refuseRecvFileSlot)
                    chatFrame.raise_()  # 放到最前面
                    return
            # 如果没有打开
            # 打开
            chatFrame = ChatFrame(self.widget)
            chatFrame.sendMsgSignal.connect(self.sendMsgSignal)  # 发送聊天消息
            chatFrame.sendFileRequestSignal.connect(self.sendFileRequestSignal)  # 发送文件请求
            self.getMsgSignal.connect(chatFrame.getMsgSlot)  # 获取聊天消息
            self.getFriendHostSignal.connect(chatFrame.getFriendHostSlot)  # 获取好友ip地址
            self.refuseRecvFileSignal.connect(chatFrame.refuseRecvFileSlot)
            # 更新聊天界面的自己的用户信息和该好友的用户信息
            chatFrame.myInfo = self.myInfo
            chatFrame.my_host = self.host
            chatFrame.friendInfo = UserInfo(0, uid=item.data(Qt.UserRole + FriendInfoIndex.id),
                                            name=item.data(Qt.UserRole + FriendInfoIndex.name),
                                            mark_name=item.data(Qt.UserRole + FriendInfoIndex.mark_name))
            self.getFriendHostRequestSignal.emit(item.data(Qt.UserRole + FriendInfoIndex.id))
            chatFrame.resize(self.widget.size())
            f_msg_filename = './cache/' + '-'.join(['f', self.myInfo.id,
                                                    item.data(Qt.UserRole + FriendInfoIndex.id)]) + '.txt'
            try:
                f_file = open(f_msg_filename, 'r', encoding="utf8")
                chatFrame.recvTextEdit.append(''.join(f_file.readlines()))
            except OSError as err:
                print(err)
                f_file = open(f_msg_filename, 'x', encoding="utf8")
                f_file.close()
            else:
                f_file.close()
            chatFrame.show()
            self.chatFrameList.append(chatFrame)  # 加入聊天面板列表
        elif item.data(Qt.UserRole + FriendInfoIndex.obj_type) == 1:  # 如果是群
            # 判定是否相应的聊天面板是否已经打开
            for chatFrame in self.chatFrameList:
                # 如果打开了
                if chatFrame.friendInfo.nick_name == item.data(Qt.UserRole + FriendInfoIndex.nick_name):
                    chatFrame.raise_()  # 放到最前面
                    return
            # 如果没有打开
            # 打开
            chatFrame = GroupFrame(self.widget)
            chatFrame.sendGroupMsgSignal.connect(self.sendGroupMsgSignal)  # 发送聊天消息
            self.getGroupMsgSignal.connect(chatFrame.getGroupMsgSlot)  # 获取聊天消息
            # 更新聊天界面的自己的用户信息和该好友的用户信息
            chatFrame.myInfo = self.myInfo
            chatFrame.friendInfo = UserInfo(1, item.data(Qt.UserRole + FriendInfoIndex.id),
                                            item.data(Qt.UserRole + FriendInfoIndex.name),
                                            item.data(Qt.UserRole + FriendInfoIndex.nick_name))
            chatFrame.resize(self.widget.size())
            g_msg_filename = './cache/' + '-'.join(['g', self.myInfo.id,
                                                    item.data(Qt.UserRole + FriendInfoIndex.nick_name)]) + '.txt'
            try:
                g_file = open(g_msg_filename, 'r', encoding="utf8")
                chatFrame.recvTextEdit.append(''.join(g_file.readlines()))
            except OSError as err:
                print(err)
                g_file = open(g_msg_filename, 'x', encoding="utf8")
                g_file.close()
            else:
                g_file.close()
            chatFrame.show()
            self.chatFrameList.append(chatFrame)  # 加入聊天面板列表

    # 使得在界面大小变化的时候聊天面板的大小能够跟着变化
    def resizeEvent(self, QResizeEvent):
        for chatFrame in self.chatFrameList:
            chatFrame.resize(self.widget.size())
        return super().resizeEvent(QResizeEvent)

    # 获取聊天消息
    def getMsgSlot(self, msgInfoList):
        friendChatFrame = None
        # 如果该好友的聊天面板已经打开
        for chatFrame in self.chatFrameList:
            if chatFrame.friendInfo.id == msgInfoList[0]:
                friendChatFrame = chatFrame
                # 设置好友列表当前选中项
                for i in range(self.friendListWidget.count()):
                    if self.friendListWidget.item(i).data(Qt.UserRole + FriendInfoIndex.id) == friendChatFrame.friendInfo.id:
                        self.friendListWidget.setCurrentRow(i)
                break
        # ...没有打开则打开
        if friendChatFrame is None:
            for i in range(self.friendListWidget.count()):
                if self.friendListWidget.item(i).data(Qt.UserRole + FriendInfoIndex.id) == msgInfoList[0]:
                    self.friendListWidgetItemClicked(self.friendListWidget.item(i))
                    self.friendListWidget.setCurrentRow(i)  # 设置好友列表当前选中项
                    for chatFrame in self.chatFrameList:
                        if chatFrame.friendInfo.id == msgInfoList[0]:
                            friendChatFrame = chatFrame
                            break
                    break
        friendChatFrame.raise_()  # 放到最前面
        # 发送获取聊天信息的信号
        self.getMsgSignal.emit(msgInfoList)

    # 获取群消息
    def getGroupMsgSlot(self, msgInfoList):
        groupChatFrame = None
        # 如果该群的聊天面板已经打开
        for chatFrame in self.chatFrameList:
            if chatFrame.friendInfo.nick_name == msgInfoList[0]:
                groupChatFrame = chatFrame
                # 设置好友列表当前选中项
                for i in range(self.friendListWidget.count()):
                    if self.friendListWidget.item(i).data(
                            Qt.UserRole + FriendInfoIndex.nick_name) == groupChatFrame.friendInfo.nick_name:
                        self.friendListWidget.setCurrentRow(i)
                break
        # ...没有打开则打开
        if groupChatFrame is None:
            for i in range(self.friendListWidget.count()):
                if self.friendListWidget.item(i).data(Qt.UserRole + FriendInfoIndex.nick_name) == msgInfoList[0]:
                    self.friendListWidgetItemClicked(self.friendListWidget.item(i))
                    self.friendListWidget.setCurrentRow(i)  # 设置好友列表当前选中项
                    for chatFrame in self.chatFrameList:
                        if chatFrame.friendInfo.nick_name == msgInfoList[0]:
                            groupChatFrame = chatFrame
                            break
                    break
        groupChatFrame.raise_()  # 放到最前面
        # 发送获取聊天信息的信号
        self.getGroupMsgSignal.emit(msgInfoList)

    # 在删除好友的时候删除相应的聊天面板
    def delChatFrameSlot(self, friendID):
        for chatFrame in self.chatFrameList:
            if chatFrame.friendInfo.id == friendID:
                chatFrame.close()
                self.chatFrameList.remove(chatFrame)
                chatFrame.deleteLater()

    # 根据新的聊天面板的id列表更新聊天面板
    def updateChatFrameSlot(self, chatFrameIDList):
        for chatFrame in self.chatFrameList:
            if chatFrame.friendInfo.id not in chatFrameIDList:
                chatFrame.close()
                self.chatFrameList.remove(chatFrame)
                chatFrame.deleteLater()
        # 重置界面标题
        if len(self.chatFrameList) != 0:
            for i in range(self.friendListWidget.count()):
                if self.friendListWidget.item(i).data(Qt.UserRole + FriendInfoIndex.id) == \
                        self.chatFrameList[0].friendInfo.id:
                    self.friendListWidget.setCurrentRow(i)
                    self.chatFrameList[0].raise_()
                    break

    def getFileSlot(self, msgList):
        userName = msgList[1]
        serverAddress = msgList[2]
        fileName = msgList[4]
        isreceive = "来自{}的文件：{}，是否接收？".format(userName, fileName)
        btn = QMessageBox.information(self, "接收文件", isreceive, QMessageBox.Yes, QMessageBox.No)
        if btn == QMessageBox.Yes:
            name = QFileDialog.getSaveFileName(self, "保存文件", fileName)
            if name[0]:
                client = TcpC(self)
                client.setFileName(name[0])
                client.setHostAddress(QHostAddress(serverAddress))
                client.exec()
        else:
            self.refuseRecvFile.emit(userName)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainGui()
    ui.show()
    sys.exit(app.exec_())