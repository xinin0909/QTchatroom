from PyQt5.QtCore import QObject, pyqtSignal, QThread
from LoginGui import LoginGui
from MainGui import MainGui
from TcpSocket import TcpSocket
from Extern import UserInfo


# 后台数据类
class Data(QObject):
    addSignalSlotForClassSignal = pyqtSignal([LoginGui], [MainGui])  # 添加界面的信号和槽的连接
    connectedFailedSignal = pyqtSignal()  # 连接服务器失败

    loginSuccessSignal = pyqtSignal()  # 登陆成功
    loginFailedSignal = pyqtSignal()  # 登陆失败
    loginRepeatSignal = pyqtSignal()  # 重复登陆
    registerSuccessSignal = pyqtSignal(str)  # 注册是否成功

    getMyInfoSignal = pyqtSignal(UserInfo)  # 获取自己的用户信息
    getFriendListSignal = pyqtSignal(list)  # 获取好友列表

    getMsgSignal = pyqtSignal(list)  # 获取聊天消息
    getGroupMsgSignal = pyqtSignal(list)  # 获取群消息

    noThisUserSignal = pyqtSignal(str)  # 添加好友请求返回没有这个用户
    updateMyInfoSignal = pyqtSignal(str)  # 修改个人信息是否成功 0为成功，1为失败
    getMyHostSignal = pyqtSignal(str)  # 获取自己的ip地址
    getFriendHostSignal = pyqtSignal(str)  # 获取好友ip地址
    recvFileSignal = pyqtSignal(list)  # 接收文件信号
    refuseRecvFileSignal = pyqtSignal(list)  # 拒绝接收文件

    def __init__(self, srv_host, srv_port, parent=None):
        super().__init__(parent)
        self.srv_host = srv_host
        self.srv_port = srv_port
        self.host = ""
        # 后台线程
        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self.init)  # 启动线程的初始化
        # 资源管理
        self.destroyed.connect(self.thread.quit)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()  # 启动

    # 后台线程开始的时候的初始函数
    def init(self):
        self.myInfo = UserInfo(0)   # 自己的用户信息

        # 这个信号是用来在调用了对外的添加信号和信号槽的函数之后，
        # 把传进来的gui参数传给真正用来连接信号和信号槽的函数的，
        # 此举旨在让这个连接动作也在另一个线程
        self.addSignalSlotForClassSignal.connect(self.addSignalSlotForClassSlot)

        # 和服务器的socket连接
        self.connectToServer = TcpSocket()
        self.connectToServer.connectToHost(self.srv_host, self.srv_port)
        self.is_connected = self.connectToServer.waitForConnected(3000)  # 判断连接服务器是否成功
        self.connectToServer.getMsgSignal.connect(self.getMsgFromServer)

    # 供这个类对象调对外调用的添s加信号和信号槽的函数
    def addSignalSlot(self, gui):
        self.addSignalSlotForClassSignal.emit(gui)

    # 连接数据类和界面类（登陆界面和主界面）的信号和信号槽
    def addSignalSlotForClassSlot(self, gui):
        # 如果gui是登陆界面
        if type(gui) == LoginGui:
            gui.loginRequestSignal.connect(self.loginRequestSlot)  # 登陆请求
            gui.registerRequestSignal.connect(self.registerRequestSlot)  # 注册请求

            self.connectedFailedSignal.connect(gui.connectedFailedSlot)  # 连接服务器失败
            if not self.is_connected:
                self.connectedFailedSignal.emit()  # 发送服务器连接失败信号

            self.loginSuccessSignal.connect(gui.accept)  # 登陆成功
            self.loginFailedSignal.connect(gui.loginFailedSlot)  # 登陆失败
            self.loginRepeatSignal.connect(gui.loginRepeatSlot)  # 重复登陆
            self.registerSuccessSignal.connect(gui.registerSuccessSignal)  # 注册是否成功
        # 如果gui是主界面
        elif type(gui) == MainGui:
            self.getMyInfoSignal.connect(gui.getMyInfoSlot)  # 传递自己的用户信息
            self.getMyHostSignal.connect(gui.getMyHostSlot)  # 传递自己的ip地址
            self.getFriendListSignal.connect(gui.getFriendListSignal)  # 传递好友列表
            self.getMsgSignal.connect(gui.getMsgSlot)  # 传递聊天消息
            self.getGroupMsgSignal.connect(gui.getGroupMsgSlot)  # 传递群消息
            self.noThisUserSignal.connect(gui.noThisUserSignal)  # 添加好友请求返回没有这个用户
            self.updateMyInfoSignal.connect(gui.updateMyInfoSignal)  # 修改个人信息是否成功
            self.getFriendHostSignal.connect(gui.getFriendHostSignal)  # 获取好友ip地址
            self.recvFileSignal.connect(gui.getFileSlot)  # 接收文件信息
            self.refuseRecvFileSignal.connect(gui.refuseRecvFileSignal)  # 拒绝接收文件

            gui.sendMsgSignal.connect(self.sendMsgSlot)  # 发送聊天消息
            gui.sendGroupMsgSignal.connect(self.sendGroupMsgSlot)  # 发送群消息
            gui.addFriendRequestSignal.connect(self.addFriendRequestSlot)  # 添加好友请求
            gui.delFriendRequestSignal.connect(self.delFriendRequestSlot)  # 删除好友请求
            gui.setFriendNameRequestSignal.connect(self.setFriendNameRequestSlot)  # 修改备注请求
            gui.createGroupRequestSignal.connect(self.createGroupRequestSlot)  # 创建群请求
            gui.addGroupRequestSignal.connect(self.addGroupRequestSlot)  # 加群请求
            gui.quitGroupRequestSignal.connect(self.quitGroupRequestSlot)  # 退群请求
            gui.delGroupRequestSignal.connect(self.delGroupRequestSlot)  # 解散群请求
            gui.setMyInfoRequestSignal.connect(self.setMyInfoRequestSlot)  # 修改个人信息请求
            gui.getFriendHostRequestSignal.connect(self.getFriendHostRequestSlot)  # 获取好友ip地址请求
            gui.sendFileRequestSignal.connect(self.sendFileRequestSlot)  # 发送文件请求
            gui.refuseRecvFile.connect(self.refuseRecvFileSlot)  # 拒绝接收文件

            self.connectToServer.writeMsg("MyInfoRequest")  # 自己的用户信息请求
            self.connectToServer.writeMsg("FriendListRequest")  # 好友列表请求

    # 从服务器收到了消息之后socket会给出一个信号，这个信号带有一个str参数，传给这个函数进行进一步的处理
    def getMsgFromServer(self, msg):
        print(msg)  # 输出调试信息

        # 获取消息列表
        msgList = msg.split(' ')
        # 登陆成功
        if msgList[0] == "LoginSuccess":
            self.loginSuccessSignal.emit()
        # 登陆失败
        elif msgList[0] == "LoginFailed":
            self.loginFailedSignal.emit()
        # 重复登陆
        elif msgList[0] == "LoginRepeat":
            self.loginRepeatSignal.emit()
        # 注册成功
        elif msgList[0] == "RegisterSuccess":
            self.registerSuccessSignal.emit(msgList[1])
        # 注册失败
        elif msgList[0] == "RegisterFail":
            self.registerSuccessSignal.emit(None)
        # 自己的用户信息
        elif msgList[0] == "MyInfo":
            # 获取自己的用户信息
            self.myInfo.id = msgList[1]
            self.host = msgList[2]
            my_info_dict = eval(' '.join(msgList[3:]))
            self.myInfo.name = my_info_dict['name']
            self.myInfo.nick_name = my_info_dict['nick_name']
            self.myInfo.age = my_info_dict['age']
            self.myInfo.birthday = my_info_dict['birthday']
            self.myInfo.gender = my_info_dict['gender_id']
            self.myInfo.mail = my_info_dict['email']
            self.myInfo.phone = my_info_dict['telephone']
            self.myInfo.register_time = my_info_dict['register_time']
            self.myInfo.signature = my_info_dict['signature']
            self.myInfo.vocation = my_info_dict['vocation']
            self.getMyInfoSignal.emit(self.myInfo)  # 传递自己的用户信息
            self.getMyHostSignal.emit(self.host)  # 传递自己的ip地址
        # 获取聊天消息
        elif msgList[0] == "Message":
            friendID = msgList[1]  # 获取发送方，即好友id
            # 弹出包头及无关信息
            msgList.reverse()
            msgList.pop()
            msgList.pop()
            msgList.pop()
            msgList.reverse()
            self.getMsgSignal.emit([friendID, " ".join(msgList)])  # 传递聊天消息
        # 获取群消息
        elif msgList[0] == "GroupMessage":
            sender_name = msgList[1]  # 获取发送方用户名
            group_name = msgList[2]  # 获取群名
            # 弹出包头及无关信息
            msgList.reverse()
            msgList.pop()
            msgList.pop()
            msgList.pop()
            msgList.pop()
            msgList.reverse()
            self.getGroupMsgSignal.emit([group_name, sender_name, " ".join(msgList)])  # 传递聊天消息
        # 添加好友请求返回没有这个用户
        elif msgList[0] == "NoThisUser":
            self.noThisUserSignal.emit(msgList[1])
        # 修改个人信息是否成功
        elif msgList[0] == "UpdateMyInfo":
            self.updateMyInfoSignal.emit(msgList[1])
        # 获得好友ip地址
        elif msgList[0] == "GetFriendHost":
            self.getFriendHostSignal.emit(msgList[1])
        elif msgList[0] == "RecvFile":
            self.recvFileSignal.emit(msgList)
        elif msgList[0] == "RefuseRecvFile":
            self.refuseRecvFileSignal.emit(msgList)
        # 好友列表
        else:  # msgList[0] == "FriendList":
            msgList = msg.split('~~~~~~')
            friendInfoList = []  # 好友及群列表
            # 整理好友列表的id和用户名好人备注封装成用户信息对象做成一个列表加到要发送的列表中，并且发送
            for friendInfo in msgList:
                if friendInfo != "FriendList":
                    friendInfoStrList = friendInfo.split('~`~')
                    if friendInfoStrList[0] == "Group":
                        friendInfoList.append(
                            UserInfo(1, friendInfoStrList[1], friendInfoStrList[2], friendInfoStrList[3]))
                    else:
                        friend_info_dict = eval(friendInfoStrList[3])
                        friendInfoList.append(
                            UserInfo(0, uid=friendInfoStrList[0], name=friendInfoStrList[1],
                                     nick_name=friend_info_dict['nick_name'], mail=friend_info_dict['email'],
                                     signature=friend_info_dict['signature'], gender=friend_info_dict['gender_id'],
                                     birthday=friend_info_dict['birthday'], vocation=friend_info_dict['vocation'],
                                     register_time=friend_info_dict['register_time'], age=friend_info_dict['age'],
                                     mark_name=friendInfoStrList[2]))
            self.getFriendListSignal.emit(friendInfoList)

    # 登陆请求
    def loginRequestSlot(self, acountInfo):
        acoutInfoList = acountInfo.split(' ')
        self.connectToServer.writeMsg("LoginRequest %s %s" % (acoutInfoList[0], acoutInfoList[1]))
    
    # 注册请求
    def registerRequestSlot(self, acountInfo):
        acoutInfoList = acountInfo.split(' ')
        self.connectToServer.writeMsg("RegisterRequest %s %s %s"
                                      % (acoutInfoList[0], acoutInfoList[1], acoutInfoList[2]))

    # 发送聊天消息
    def sendMsgSlot(self, msg):
        self.connectToServer.writeMsg("Message %s %s" % (self.myInfo.id, msg))

    # 发送群消息
    def sendGroupMsgSlot(self, msg):
        self.connectToServer.writeMsg("GroupMessage %s %s" % (self.myInfo.name, msg))

    # 添加好友请求
    def addFriendRequestSlot(self, friendID):
        self.connectToServer.writeMsg("AddFriendRequest %s %s" % (self.myInfo.id, friendID))

    # 删除好友请求
    def delFriendRequestSlot(self, friendID):
        self.connectToServer.writeMsg("DelFriendRequest %s %s" % (self.myInfo.id, friendID))

    # 修改好友备注请求
    def setFriendNameRequestSlot(self, msg):
        msgList = msg.split(' ')
        friend_name = msgList[0]
        friend_mark_name = msgList[1]
        self.connectToServer.writeMsg("SetFriendNameRequest %s %s %s" % (self.myInfo.id, friend_name, friend_mark_name))

    # 创建群请求
    def createGroupRequestSlot(self, group_name):
        self.connectToServer.writeMsg("CreateGroupRequest %s %s" % (self.myInfo.id, group_name))

    # 解散群请求
    def delGroupRequestSlot(self, group_name):
        self.connectToServer.writeMsg("DelGroupRequest %s %s" % (self.myInfo.id, group_name))

    # 加入群请求
    def addGroupRequestSlot(self, group_name):
        self.connectToServer.writeMsg("AddGroupRequest %s %s" % (self.myInfo.id, group_name))

    # 退群请求
    def quitGroupRequestSlot(self, group_name):
        self.connectToServer.writeMsg("QuitGroupRequest %s %s" % (self.myInfo.id, group_name))

    # 修改个人信息请求
    def setMyInfoRequestSlot(self, my_info_dict):
        self.connectToServer.writeMsg("SetMyInfoRequest~`~%s~`~%s" % (self.myInfo.id, str(my_info_dict)))

    # 获取好友ip地址请求
    def getFriendHostRequestSlot(self, friend_id):
        self.connectToServer.writeMsg("GetFriendHostRequest %s %s" % (self.myInfo.id, friend_id))

    def sendFileRequestSlot(self, msg):
        self.connectToServer.writeMsg("SendFileRequest %s %s" % (self.myInfo.id, msg))

    def refuseRecvFileSlot(self, user_name):
        self.connectToServer.writeMsg("RefuseRecvFile %s %s" % (self.myInfo.id, user_name))
