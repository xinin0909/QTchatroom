from PyQt5.QtCore import QThread, pyqtSignal
from TcpSocket import TcpSocket


# 连接客户端的线程
class ClientThread(QThread):
    disconnectToClientSignal = pyqtSignal()  # 和某个客户端断开连接之后
    getMsgFromClientSignal = pyqtSignal(str)  # 从客户端获取消息
    sendMsgToClientSignal = pyqtSignal(str)  # 给客户端发送消息

    def __init__(self, voidptr, parent=None):
        super().__init__(parent)

        self.id = ""  # 本线程中运行的socket所连接的客户端
        self.voidptr = voidptr  # socket唯一描述符
        self.host = None

    def run(self):
        connectToClient = TcpSocket()
        connectToClient.setSocketDescriptor(self.voidptr)  # 设置socket标识符
        self.host = connectToClient.peerAddress().toString().split(':')[-1]
        connectToClient.disconnected.connect(self.disconnectToClientSignal)  # 断开连接之后的资源释放
        self.finished.connect(connectToClient.deleteLater)  # 退出线程之后删除socket
        connectToClient.getMsgSignal.connect(self.getMsgFromClientSignal)  # 获取从客户端发来的信息
        self.sendMsgToClientSignal.connect(connectToClient.writeMsg)  # 向客户端发送消息
        self.exec()
