from PyQt5.QtNetwork import QTcpServer, QHostAddress
from ClientThread import ClientThread
from user_info import User
from friend import Friend
from group_info import Group
from GroupUser import GroupUser
from sen_word import sense_words
from ai import ai_answer


# 服务器类
class Server(QTcpServer):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.threadPool = []  # 线程池

        self.listen(QHostAddress.Any, 8888)
        print("开始监听本地端口8888...")

    # 重写父类方法，重写当一个连接到来时的行为
    def incomingConnection(self, voidptr):
        print("a new connection from %s and the num of client is %s" % (str(voidptr), len(self.threadPool) + 1))

        clientThread = ClientThread(voidptr)
        clientThread.disconnectToClientSignal.connect(self.disconnectToClientSlot)  # 断开连接后的资源释放
        clientThread.getMsgFromClientSignal.connect(self.getMsgFromClientSlot)  # 从客户端获取消息
        self.threadPool.append(clientThread)  # 线程池添加
        clientThread.run()  # 开启线程

    # 和客户端断开连接之后的资源释放
    def disconnectToClientSlot(self):
        self.sender().exit()
        self.threadPool.remove(self.sender())
        print("a connection was disconnected with id %s, now the num of the client is %s"
              % (self.sender().id, len(self.threadPool)))

    # 从客户端获取消息
    def getMsgFromClientSlot(self, msg):
        sender = self.sender()  # 获取发送方

        print("id %s send msg %s" % (str(sender.id), msg))  # 打印客户端发送的消息

        # 获取消息列表
        msgList = msg.split(' ')
        # 登陆请求
        if msgList[0] == "LoginRequest":
            self.loginRequestHandle(sender, msgList)
        # 注册请求
        elif msgList[0] == "RegisterRequest":
            self.registerRequestHandle(sender, msgList)
        # 获取自己的用户信息请求
        elif msgList[0] == "MyInfoRequest":
            self.myInfoRequestHandle(sender, msgList)
        # 好友列表请求
        elif msgList[0] == "FriendListRequest":
            self.friendListRequestHandle(sender, msgList)
        # 添加好友请求
        elif msgList[0] == "AddFriendRequest":
            self.addFriendRequestHandle(sender, msgList)
        # 删除好友请求
        elif msgList[0] == "DelFriendRequest":
            self.delFriendRequestHandle(sender, msgList)
        # 给好友发送聊天消息
        elif msgList[0] == "Message":
            self.messageHandle(sender, msgList)
        # 给群发送消息
        elif msgList[0] == "GroupMessage":
            self.groupMessageHandle(sender, msgList)
        # 修改好友备注请求
        elif msgList[0] == "SetFriendNameRequest":
            self.setFriendNameRequestHandle(sender, msgList)
        # 创建群请求
        elif msgList[0] == "CreateGroupRequest":
            self.createGroupRequestHandle(sender, msgList)
        # 解散群请求
        elif msgList[0] == "DelGroupRequest":
            self.delGroupRequestHandle(sender, msgList)
        # 加群请求
        elif msgList[0] == "AddGroupRequest":
            self.addGroupRequestHandle(sender, msgList)
        # 退群请求
        elif msgList[0] == "QuitGroupRequest":
            self.quitGroupRequestHandle(sender, msgList)
        # 获取好友id请求
        elif msgList[0] == "GetFriendHostRequest":
            self.getFriendHostRequestHandle(sender, msgList)
        # 发送文件请求
        elif msgList[0] == "SendFileRequest":
            self.sendFileRequestHandle(sender, msgList)
        # 拒绝接收文件
        elif msgList[0] == "RefuseRecvFile":
            self.refuseRecvFileHandle(sender, msgList)
        # 修改个人信息请求
        else:  # msgList[0] == "SetMyInfoRequest"
            self.setMyInfoRequestHandle(sender, msg)

    # 登陆请求处理函数，传入发送方和消息列表
    def loginRequestHandle(self, sender, msgList):
        username = msgList[1]
        password = msgList[2]
        # 判断是否重复登陆
        for i in self.threadPool:
            if i.id == User.name_to_id(username):
                sender.sendMsgToClientSignal.emit("LoginRepeat")
                return
        # 判断用户名和密码是否正确
        user = User(username, password)
        user_id = user.login()
        if user_id:
            sender.sendMsgToClientSignal.emit("LoginSuccess")
            sender.id = user_id
            sender.name = user.name
            sender.nick_name = user.nick_name
            print("LoginSuccess")
        else:
            sender.sendMsgToClientSignal.emit("LoginFailed")
            print("LoginFailed")

    # 注册请求处理函数
    def registerRequestHandle(self, sender, msgList):
        # 获取要注册的昵称和密码
        username = msgList[1]
        password = msgList[2]
        mail = msgList[3]
        # 创建新用户
        user = User(username, password, mail)
        result = user.register()
        if result:
            # 获取新id
            new_id = User.name_to_id(username)
            sender.sendMsgToClientSignal.emit("RegisterSuccess" + " " + str(new_id))
            print("RegisterSuccess")
        else:
            sender.sendMsgToClientSignal.emit("RegisterFail")
            print("RegisterFail")

    # 自己的用户信息请求处理函数
    def myInfoRequestHandle(self, sender, msgList):
        my_info_dict = User.get_user_info(sender.id)
        sender.sendMsgToClientSignal.emit("MyInfo %s %s %s" % (sender.id, sender.host, my_info_dict))

    # 好友列表请求处理函数
    def friendListRequestHandle(self, sender, msgList):
        # 查询请求方好友列表
        friend_list = eval(Friend.get_friend_list(sender.id))
        # 查询请求方群列表
        group_list = GroupUser.get_group_list(sender.id)
        group_info_list = []
        for group_id in group_list:
            group_info = eval(GroupUser.get_group_info(group_id))
            group_info_list.append("Group~`~{}~`~{}~`~{}".format(group_info[0], group_info[1], group_info[2]))
        # 整理格式并发送
        sendMsg = "FriendList"
        for friend in friend_list:
            sendMsg += "~~~~~~"
            sendMsg += str(friend[0])
            sendMsg += "~`~"
            sendMsg += friend[1]
            sendMsg += "~`~"
            sendMsg += friend[2]
            sendMsg += "~`~"
            sendMsg += User.get_user_info(friend[0])
        for group_info in group_info_list:
            sendMsg += "~~~~~~"
            sendMsg += group_info
        sender.sendMsgToClientSignal.emit(sendMsg)
        print(sendMsg)

    # 添加好友请求处理函数
    def addFriendRequestHandle(self, sender, msgList):
        friend_name = msgList[2]  # 获取要添加的好友用户名
        # 检测是否存在这个ID
        friend = Friend(sender.id, friend_name)
        result = friend.add_friend()
        # 存在
        if result:
            # 给请求方更新好友列表
            sender.sendMsgToClientSignal.emit("NoThisUser 0")
            self.friendListRequestHandle(sender, "FriendListRequest".split(' '))
            # 如果被请求方在线的话，给被请求方更新好友列表
            for clientThread in self.threadPool:
                if clientThread.id == User.name_to_id(friend_name):
                    self.friendListRequestHandle(clientThread, "FriendListRequest".split(' '))
        # 如果不存在
        else:
            sender.sendMsgToClientSignal.emit("NoThisUser 1")

    # 删除好友请求处理函数
    def delFriendRequestHandle(self, sender, msgList):
        friendID = msgList[2]  # 获取要删除的好友的ID
        friend_name = User.id_to_name(friendID)
        friend = Friend(sender.id, friend_name)
        friend.del_friend()
        # 如果被删除方也在线的话就给被删除方更新好友列表
        for clientThread in self.threadPool:
                if clientThread.id == int(friendID):
                    self.friendListRequestHandle(clientThread, "FriendListRequest".split(' '))

    # 发送聊天消息处理函数
    def messageHandle(self, sender, msgList):
        friendID = msgList[2]
        msgList[3] = sense_words(' '.join(msgList[3:]))
        # 如果接收方在线上的话
        for clientThread in self.threadPool:
            if clientThread.id == int(friendID):
                msg = " ".join(msgList[0:4])
                clientThread.sendMsgToClientSignal.emit(msg)
                return
        # 不在的话
        sender.sendMsgToClientSignal.emit("Message %s %s %s" % (friendID, sender.id,
                                                                "该用户不在线上，你的消息可能无法到达！"))

    # 发送群消息处理函数
    def groupMessageHandle(self, sender, msgList):
        sender_name = msgList[1]
        group_name = msgList[2]
        msgList[4] = ' '.join(msgList[4:])
        ai_answer_msg = ""
        if msgList[4][-3:] == "@小i":
            ai_answer_msg = ai_answer(msgList[4][:-3])
            ai_answer_msg = "GroupMessage 小i " + group_name + " 0 " + ai_answer_msg + "@" + sender_name
            print(ai_answer_msg)
        msgList[4] = sense_words(' '.join(msgList[4:]))
        group_id = GroupUser.group_name_to_id(group_name)
        group_user_list = GroupUser.get_all_user_id(group_id)
        # 如果接收方在线上的话
        for clientThread in self.threadPool:
            if clientThread.id in group_user_list:
                if clientThread.id != sender.id:
                    clientThread.sendMsgToClientSignal.emit(" ".join(msgList[0:5]))
                if ai_answer_msg:
                    clientThread.sendMsgToClientSignal.emit(ai_answer_msg)

    # 修改好友备注请求处理函数
    def setFriendNameRequestHandle(self, sender, msgList):
        friend_name = msgList[2]  # 好友用户名
        friend_mark_name = msgList[3]  # 好友备注
        friend = Friend(sender.id, friend_name, friend_mark_name)
        result = friend.set_remark_name(friend_mark_name)
        if result:
            print("setFriendNameSuccess")
            # 给请求方更新好友列表
            self.friendListRequestHandle(sender, "FriendListRequest".split(' '))
        else:
            print("setFriendNameFail")

    # 创建群处理函数
    def createGroupRequestHandle(self, sender, msgList):
        group_name = msgList[2]  # 群名称
        group = Group(sender.id, group_name)
        result = group.create_group()
        if result:
            print("CreateSuccess")
            # 给请求方更新好友列表
            self.friendListRequestHandle(sender, "FriendListRequest".split(' '))
        else:
            print("CreateFail")

    # 解散群处理函数
    def delGroupRequestHandle(self, sender, msgList):
        group_name = msgList[2]
        # 获取群中的成员列表
        group_id = GroupUser.group_name_to_id(group_name)
        member_list = GroupUser.get_all_user_id(group_id)
        group = Group(sender.id, group_name)
        result = group.del_group()
        if result:
            print("DeleteGroupSuccess")
            # 给请求方更新好友列表
            self.friendListRequestHandle(sender, "FriendListRequest".split(' '))
            # 如果解散的群成员在线的话就给这些成员更新好友列表
            for clientThread in self.threadPool:
                if clientThread.id in member_list:
                    self.friendListRequestHandle(clientThread, "FriendListRequest".split(' '))
        else:
            print("DeleteGroupFail")

    # 加群处理函数
    def addGroupRequestHandle(self, sender, msgList):
        group_name = msgList[2]
        group_user = GroupUser(sender.id, group_name)
        result = group_user.add_group()
        if result:
            print("AddGroupSuccess")
            # 给请求方更新好友列表
            self.friendListRequestHandle(sender, "FriendListRequest".split(' '))
        else:
            print("AddGroupFail")

    # 退群处理函数
    def quitGroupRequestHandle(self, sender, msgList):
        group_name = msgList[2]
        group_user = GroupUser(sender.id, group_name)
        result = group_user.quit_group()
        if result:
            print("QuitGroupSuccess")
            # 给请求方更新好友列表
            self.friendListRequestHandle(sender, "FriendListRequest".split(' '))
        else:
            print("QuitGroupFail")

    # 修改个人信息处理函数
    def setMyInfoRequestHandle(self, sender, msg):
        user_id = sender.id
        user_info_dict = eval(msg.split("~`~")[2])
        friend_id_list = eval(Friend.get_friend_id_list(sender.id))
        result = User.set_user_info(user_id, user_info_dict)
        if result or result == 0:
            self.myInfoRequestHandle(sender, msg)
            # 如果好友在线的话就给这些成员更新好友列表
            for clientThread in self.threadPool:
                if clientThread.id in friend_id_list:
                    self.friendListRequestHandle(clientThread, "FriendListRequest".split(' '))
            sender.sendMsgToClientSignal.emit("UpdateMyInfo 0")
            print("UpdateSuccess")
        else:
            sender.sendMsgToClientSignal.emit("UpdateMyInfo 1")
            print("UpdateFail")

    # 获取好友ip地址请求处理
    def getFriendHostRequestHandle(self, sender, msgList):
        friend_host = ""
        friend_id = int(msgList[2])
        # 如果接收方在线上的话
        for clientThread in self.threadPool:
            if friend_id == clientThread.id:
                friend_host = clientThread.host
        sender.sendMsgToClientSignal.emit("GetFriendHost %s" % friend_host)

    # 发送文件请求处理函数
    def sendFileRequestHandle(self, sender, msgList):
        recv_id = int(msgList[2])
        filename = msgList[3]
        # 如果接收方在线上的话
        for clientThread in self.threadPool:
            if clientThread.id == recv_id:
                send_masg = "RecvFile %s %s %s %s" % (sender.name, sender.host, clientThread.host, filename)
                clientThread.sendMsgToClientSignal.emit(send_masg)

    # 拒绝接收文件
    def refuseRecvFileHandle(self, sender, msgList):
        user_name = msgList[2]
        # 如果接收方在线上的话
        for clientThread in self.threadPool:
            if clientThread.name == user_name:
                send_masg = "RefuseRecvFile %s %s" % (sender.name, user_name)
                clientThread.sendMsgToClientSignal.emit(send_masg)
