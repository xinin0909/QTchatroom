from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QMenu, QAction, QMessageBox
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QCursor
from AddFriendGui import AddFriendGui
from SetFriendNameGui import setFriendNameGui
from CreateGroupGui import CreateGroupGui
from addGroupGui import AddGroupGui
from FriendInfoGui import FriendInfoGui
from Extern import FriendInfoIndex, UserInfo


# 好友列表
class FriendListWidget(QListWidget):
    friendItemClicked = pyqtSignal(QListWidgetItem)  # 把自己的itemClicked信号发送到外面去
    addFriendRequestSignal = pyqtSignal(str)  # 添加好友请求信号
    setFriendNameRequestSignal = pyqtSignal(str)  # 修改好友备注请求信号
    updateChatFrameSignal = pyqtSignal(list)  # 删除好友之后会更新好友列表，这个时候如果是被删除方则要和删除方进行相应的删除工作，删除相应的好友项和聊天面板
    addFriendRepeatSignal = pyqtSignal()  # 重复添加好友
    noThisUserSignal = pyqtSignal(str)  # 添加好友请求返回没有这个用户
    delFriendRequestSignal = pyqtSignal(str)  # 删除好友请求信号
    delChatFrameSignal = pyqtSignal(str)  # 删除相应的聊天面板
    createGroupRequestSignal = pyqtSignal(str)  # 创建群请求信号
    addGroupRequestSignal = pyqtSignal(str)  # 加入群请求信号
    quitGroupRequestSignal = pyqtSignal(str)  # 退群请求信号
    delGroupRequestSignal = pyqtSignal(str)  # 解散群请求信号

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet('border:10px groove white;border-radius:10px;padding:0px 0px')
        self.myInfo = UserInfo(0)  # 自己的用户信息
        self.addFriendGui = None  # 添加好友的界面
        self.setFriendNameGui = None  # 修改备注的界面
        self.createGroupGui = None  # 创建群的界面
        self.addGroupGui = None  # 加入群的界面
        self.friendInfoGui = None  # 查看好友详情界面
        font = QFont("微软雅黑", 12, 10)
        # 添加好友动作
        self.addFriendAction = QAction(self)
        self.addFriendAction.setText(self.tr("添加好友"))
        self.addFriendAction.setFont(font)
        self.addFriendAction.triggered.connect(self.addFriendActionTriggered)
        # 删除好友动作
        self.delFriendAction = QAction(self)
        self.delFriendAction.setText(self.tr("删除好友"))
        self.delFriendAction.setFont(font)
        self.delFriendAction.triggered.connect(self.delFriendActionTriggered)
        # 修改备注操作
        self.setFriendNameAction = QAction(self)
        self.setFriendNameAction.setText(self.tr("修改好友备注"))
        self.setFriendNameAction.setFont(font)
        self.setFriendNameAction.triggered.connect(self.setFriendNameActionTriggered)
        # 创建群操作
        self.createGroupAction = QAction(self)
        self.createGroupAction.setText(self.tr("创建群"))
        self.createGroupAction.setFont(font)
        self.createGroupAction.triggered.connect(self.createGroupActionTriggered)
        # 解散群操作
        self.delGroupAction = QAction(self)
        self.delGroupAction.setText(self.tr("解散该群"))
        self.delGroupAction.setFont(font)
        self.delGroupAction.triggered.connect(self.delGroupActionTriggered)
        # 加群操作
        self.addGroupAction = QAction(self)
        self.addGroupAction.setText(self.tr("加入群"))
        self.addGroupAction.setFont(font)
        self.addGroupAction.triggered.connect(self.addGroupActionTriggered)
        # 退群操作
        self.quitGroupAction = QAction(self)
        self.quitGroupAction.setText(self.tr("退出此群"))
        self.quitGroupAction.setFont(font)
        self.quitGroupAction.triggered.connect(self.quitGroupActionTriggered)
        # 查看好友信息操作
        self.seeFriendInfoAction = QAction(self)
        self.seeFriendInfoAction.setText(self.tr("查看该用户详情"))
        self.seeFriendInfoAction.setFont(font)
        self.seeFriendInfoAction.triggered.connect(self.seeFriendInfoActionTriggered)

        self.setFont(QFont("微软雅黑", 16))  # UI设置

        self.itemClicked.connect(self.friendItemClicked)  # 把自己的itemClicked信号发送到外面去

    # 获取并更新自己的好友列表
    def getFriendListSlot(self, friendInfoList):
        # 清空原好友列表的项，防止出现重复
        self.clear()
        # 用来更新聊天面板的list
        chatFrameIDList = []
        # 开始一项一项加
        for friendInfo in friendInfoList:
            if friendInfo.obj_type == 0:  # 类型为好友
                # 获取好友id和昵称
                friend_id = friendInfo.id
                friend_name = friendInfo.name
                friend_nick_name = friendInfo.nick_name
                friend_phone = friendInfo.phone
                friend_mail = friendInfo.mail
                friend_gender = friendInfo.gender
                friend_age = friendInfo.age
                friend_birthday = friendInfo.birthday
                friend_vocation = friendInfo.vocation
                friend_signature = friendInfo.signature
                friend_register_time = friendInfo.register_time
                friend_mark_name = friendInfo.mark_name
                # 压入id到更新的聊天面板的id列表
                chatFrameIDList.append(friend_id)
                # 新建项
                item = QListWidgetItem(self)
                if friend_mark_name:
                    item.setText("{}（{}）".format(friend_mark_name, friend_name))  # 设置显示文本
                else:
                    item.setText(friend_name)  # 设置显示文本
                # 设置项的相关id和昵称数据
                item.setData(Qt.UserRole + FriendInfoIndex.obj_type, 0)
                item.setData(Qt.UserRole + FriendInfoIndex.id, friend_id)
                item.setData(Qt.UserRole + FriendInfoIndex.name, friend_name)
                item.setData(Qt.UserRole + FriendInfoIndex.nick_name, friend_nick_name)
                # item.setData(Qt.UserRole + FriendInfoIndex.phone, friend_phone)
                item.setData(Qt.UserRole + FriendInfoIndex.mail, friend_mail)
                item.setData(Qt.UserRole + FriendInfoIndex.gender, friend_gender)
                item.setData(Qt.UserRole + FriendInfoIndex.age, friend_age)
                item.setData(Qt.UserRole + FriendInfoIndex.birthday, friend_birthday)
                item.setData(Qt.UserRole + FriendInfoIndex.vocation, friend_vocation)
                item.setData(Qt.UserRole + FriendInfoIndex.signature, friend_signature)
                item.setData(Qt.UserRole + FriendInfoIndex.register_time, friend_register_time)
                item.setData(Qt.UserRole + FriendInfoIndex.mark_name, friend_mark_name)

                # 好友列表添加
                self.addItem(item)
            elif friendInfo.obj_type == 1:  # 类型为群
                # 获取群ID，群主ID，群名称
                group_id = friendInfo.id
                group_admin_id = friendInfo.name
                group_name = friendInfo.nick_name
                # 压入id到更新的聊天面板的id列表
                chatFrameIDList.append(group_name)
                # 新建项
                item = QListWidgetItem(self)
                item.setText("群：{}".format(group_name))  # 设置显示文本
                # 设置项的相关群id和群名称数据
                item.setData(Qt.UserRole + FriendInfoIndex.obj_type, 1)
                item.setData(Qt.UserRole + FriendInfoIndex.id, group_id)
                item.setData(Qt.UserRole + FriendInfoIndex.name, group_admin_id)
                item.setData(Qt.UserRole + FriendInfoIndex.nick_name, group_name)
                # 群列表添加
                self.addItem(item)
        self.updateChatFrameSignal.emit(chatFrameIDList)

    # 右键菜单
    def contextMenuEvent(self, QContextMenuEvent):
        menu = QMenu(self)
        menu.setStyleSheet('border:2px solid blue;border-radius:0px;padding:0px 0px')
        menu.addAction(self.addFriendAction)
        menu.addAction(self.createGroupAction)
        menu.addAction(self.addGroupAction)
        if self.itemAt(self.mapFromGlobal(QCursor.pos())) is not None:
            if self.itemAt(self.mapFromGlobal(QCursor.pos())).data(Qt.UserRole + FriendInfoIndex.obj_type) == 0:
                menu.addAction(self.delFriendAction)
                menu.addAction(self.setFriendNameAction)
                menu.addAction(self.seeFriendInfoAction)
            elif self.itemAt(self.mapFromGlobal(QCursor.pos())).data(Qt.UserRole + FriendInfoIndex.obj_type) == 1:
                if self.itemAt(self.mapFromGlobal(QCursor.pos())).data(
                        Qt.UserRole + FriendInfoIndex.name) == self.myInfo.id:
                    menu.addAction(self.delGroupAction)
                else:
                    menu.addAction(self.quitGroupAction)
        menu.exec(QCursor.pos())
        return super().contextMenuEvent(QContextMenuEvent)

    # 添加好友动作响应
    def addFriendActionTriggered(self):
        if self.addFriendGui is None:
            self.addFriendGui = AddFriendGui()
            self.addFriendGui.closeSignal.connect(self.closeAddFriendGuiSlot)  # 关闭添加好友界面
            self.addFriendGui.addFriendRequestSignal.connect(self.addFriendRequestSlot)  # 添加好友请求
            self.addFriendRepeatSignal.connect(self.addFriendGui.friendExistedSlot)  # 已经添加了这个好友
            self.noThisUserSignal.connect(self.addFriendGui.noThisUserSlot)  # 添加好友请求返回没有这个用户
            self.addFriendGui.myInfo = self.myInfo
            self.addFriendGui.show()

    # 关闭添加好友界面之后
    def closeAddFriendGuiSlot(self):
        self.addFriendGui = None

    # 添加好友请求
    def addFriendRequestSlot(self, friendID):
        # 如果已经添加了这个好友
        for i in range(self.count()):
            if self.item(i).data(Qt.UserRole + FriendInfoIndex.obj_type) == 0:
                if self.item(i).data(Qt.UserRole + FriendInfoIndex.id) == friendID:
                    self.addFriendRepeatSignal.emit()
                    return
        # 否则发送好友添加请求
        self.addFriendRequestSignal.emit(friendID)

    # 删除好友动作响应
    def delFriendActionTriggered(self):
        # 获取当前选中好友项
        selectedItemList = self.selectedItems()
        # 如果有的话
        if len(selectedItemList) != 0:
            # 警告提示
            # 如果确认
            if QMessageBox.warning(
                    self, self.tr("警告"), self.tr("你真的要删除好友 %s 吗？" % selectedItemList[0].data(
                        Qt.UserRole + FriendInfoIndex.name)), QMessageBox.Yes | QMessageBox.No,
                    defaultButton=QMessageBox.No) == QMessageBox.Yes:
                # 发送删除好友请求
                self.delFriendRequestSignal.emit(selectedItemList[0].data(Qt.UserRole + FriendInfoIndex.id))
                # 删除好友列表中的项
                for i in range(self.count()):
                    if self.item(i).data(Qt.UserRole + FriendInfoIndex.id) == \
                            selectedItemList[0].data(Qt.UserRole + FriendInfoIndex.id):
                        self.takeItem(i)
                        break
                # 删除相应的聊天面板
                self.delChatFrameSignal.emit(selectedItemList[0].data(Qt.UserRole + FriendInfoIndex.id))

    # 设置好友备注动作响应
    def setFriendNameActionTriggered(self):
        if self.setFriendNameGui is None:
            self.setFriendNameGui = setFriendNameGui()
            self.setFriendNameGui.closeSignal.connect(self.closeSetFriendNameGuiSlot)  # 关闭添加好友界面
            self.setFriendNameGui.setFriendNameRequestSignal.connect(self.setFriendNameGuiSlot)  # 添加好友请求
            self.setFriendNameGui.myInfo = self.myInfo
            self.setFriendNameGui.show()

    # 设置好友备注窗口关闭
    def closeSetFriendNameGuiSlot(self):
        self.setFriendNameGui = None

    # 设置好友备注请求
    def setFriendNameGuiSlot(self, friend_mark_name):
        # 获取当前选中好友项
        selectedItemList = self.selectedItems()
        # 如果有的话
        if len(selectedItemList) != 0:
            # 发送修改好友备注请求
            friend_name = selectedItemList[0].data(Qt.UserRole + FriendInfoIndex.name)
            msg = friend_name + ' ' + friend_mark_name
            self.setFriendNameRequestSignal.emit(msg)
            # 修改好友列表中的项
            for i in range(self.count()):
                if self.item(i).data(Qt.UserRole + FriendInfoIndex.id) == selectedItemList[0].data(
                        Qt.UserRole + FriendInfoIndex.id):
                    if friend_mark_name:
                        self.item(i).setText("{}（{}）".format(friend_mark_name, friend_name))  # 设置显示文本
                    else:
                        self.item(i).setText("{}".format(friend_name))  # 设置显示文本
                    break

    # 创建群动作响应
    def createGroupActionTriggered(self):
        if self.createGroupGui is None:
            self.createGroupGui = CreateGroupGui()
            self.createGroupGui.closeSignal.connect(self.closeCreateGroupGuiSlot)  # 关闭添加好友界面
            self.createGroupGui.createGroupRequestSignal.connect(self.createGroupGuiSlot)  # 添加好友请求
            self.createGroupGui.myInfo = self.myInfo
            self.createGroupGui.show()

    # 创建群请求
    def createGroupGuiSlot(self, group_name):
        self.createGroupRequestSignal.emit(group_name)

    # 创建群窗口关闭
    def closeCreateGroupGuiSlot(self):
        self.createGroupGui = None

    # 解散群动作响应
    def delGroupActionTriggered(self):
        # 获取当前选中的群
        selectedItemList = self.selectedItems()
        # 如果有的话
        if len(selectedItemList) != 0:
            # 警告提示
            # 如果确认
            if QMessageBox.warning(self, self.tr("警告"), self.tr(
                    "你真的要解散群： %s 吗？这将会影响到群中所有成员！请谨慎！" % selectedItemList[0].data(
                            Qt.UserRole + FriendInfoIndex.nick_name)), QMessageBox.Yes | QMessageBox.No,
                                   defaultButton=QMessageBox.No) == QMessageBox.Yes:
                # 发送解散群请求
                self.delGroupRequestSignal.emit(selectedItemList[0].data(Qt.UserRole + FriendInfoIndex.nick_name))
                # 删除列表中的项
                for i in range(self.count()):
                    if self.item(i).data(Qt.UserRole + FriendInfoIndex.nick_name) == selectedItemList[0].data(
                            Qt.UserRole + FriendInfoIndex.nick_name):
                        self.takeItem(i)
                        break
                # 删除相应的聊天面板
                self.delChatFrameSignal.emit(selectedItemList[0].data(Qt.UserRole + FriendInfoIndex.id))

    # 加群动作响应
    def addGroupActionTriggered(self):
        if self.addGroupGui is None:
            self.addGroupGui = AddGroupGui()
            self.addGroupGui.closeSignal.connect(self.closeAddGroupGuiSlot)  # 关闭加群界面
            self.addGroupGui.addGroupRequestSignal.connect(self.addGroupGuiSlot)  # 加群请求
            self.addGroupGui.myInfo = self.myInfo
            self.addGroupGui.show()

    # 加群窗口关闭
    def closeAddGroupGuiSlot(self):
        self.addGroupGui = None

    # 加群请求
    def addGroupGuiSlot(self, group_name):
        self.addGroupRequestSignal.emit(group_name)

    # 退群动作响应
    def quitGroupActionTriggered(self):
        # 获取当前选中的群
        selectedItemList = self.selectedItems()
        # 如果有的话
        if len(selectedItemList) != 0:
            # 警告提示
            # 如果确认
            if QMessageBox.warning(self, self.tr("警告"), self.tr(
                    "你真的要退出群： %s 吗？" % selectedItemList[0].data(Qt.UserRole + FriendInfoIndex.nick_name)),
                                   QMessageBox.Yes | QMessageBox.No, defaultButton=QMessageBox.No) == QMessageBox.Yes:
                # 发送退群请求
                self.quitGroupRequestSignal.emit(selectedItemList[0].data(Qt.UserRole + FriendInfoIndex.nick_name))
                # 删除列表中的项
                for i in range(self.count()):
                    if self.item(i).data(Qt.UserRole + FriendInfoIndex.nick_name) == selectedItemList[0].data(
                            Qt.UserRole + FriendInfoIndex.nick_name):
                        self.takeItem(i)
                        break
                # 删除相应的聊天面板
                self.delChatFrameSignal.emit(selectedItemList[0].data(Qt.UserRole + FriendInfoIndex.id))

    # 查看好友详情动作响应
    def seeFriendInfoActionTriggered(self):
        # 获取当前选中好友项
        selectedItemList = self.selectedItems()
        # 如果有的话
        if len(selectedItemList) != 0:
            friend_id = selectedItemList[0].data(Qt.UserRole + FriendInfoIndex.id)
            friend_name = selectedItemList[0].data(Qt.UserRole + FriendInfoIndex.name)
            friend_nick_name = selectedItemList[0].data(Qt.UserRole + FriendInfoIndex.nick_name)
            # friend_phone = selectedItemList[0].data(Qt.UserRole + FriendInfoIndex.phone)
            friend_mail = selectedItemList[0].data(Qt.UserRole + FriendInfoIndex.mail)
            friend_gender = selectedItemList[0].data(Qt.UserRole + FriendInfoIndex.gender)
            friend_age = selectedItemList[0].data(Qt.UserRole + FriendInfoIndex.age)
            friend_birthday = selectedItemList[0].data(Qt.UserRole + FriendInfoIndex.birthday)
            friend_vocation = selectedItemList[0].data(Qt.UserRole + FriendInfoIndex.vocation)
            friend_signature = selectedItemList[0].data(Qt.UserRole + FriendInfoIndex.signature)
            friend_register_time = selectedItemList[0].data(Qt.UserRole + FriendInfoIndex.register_time)
            friend_mark_name = selectedItemList[0].data(Qt.UserRole + FriendInfoIndex.mark_name)
            friend_info = UserInfo(0, uid=friend_id, name=friend_name, mark_name=friend_mark_name,
                                   nick_name=friend_nick_name, mail=friend_mail, gender=friend_gender,
                                   age=friend_age, birthday=friend_birthday, vocation=friend_vocation,
                                   signature=friend_signature, register_time=friend_register_time)
            if self.friendInfoGui is None:
                self.friendInfoGui = FriendInfoGui(friend_info)
                self.friendInfoGui.closeSignal.connect(self.closeFriendInfoGuiSlot)  # 关闭好友信息界面
                self.friendInfoGui.show()

    # 好友详情窗口关闭
    def closeFriendInfoGuiSlot(self):
        self.friendInfoGui = None
