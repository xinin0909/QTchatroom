from PyQt5.QtNetwork import QTcpSocket
from PyQt5.QtCore import pyqtSignal, QByteArray, QDataStream, QIODevice


# 和服务器连接的socket
class TcpSocket(QTcpSocket):
    getMsgSignal = pyqtSignal(str)  # 粘包处理之后获取的一条完整信息发送出去的信号

    def __init__(self, parent=None):
        super().__init__(parent)

        self.buffer = QByteArray()  # 接收消息缓冲区
        self.headLen = 4  # 包头大小
        self.msgLen = 0  # 包身大小

        self.readyRead.connect(self.getMsg)

    # 发送信息（粘包处理）
    def writeMsg(self, msg):
        if type(msg) == str:
            sendMsg = QByteArray()
            out = QDataStream(sendMsg, QIODevice.WriteOnly)
            out.setVersion(QDataStream.Qt_5_9)
            out.writeInt32(len(msg) * 2)  # 写入包头，内容为后面的消息长
            out.writeQString(msg)  # 写入消息
            self.write(sendMsg)

    # 每当有消息在socket缓冲区内可读取的时候
    # 读取信息包括粘包处理
    def getMsg(self):
        self.buffer.append(self.readAll())
        totalLen = self.buffer.size()
        while totalLen:
            in_ = QDataStream(self.buffer, QIODevice.ReadOnly)
            in_.setVersion(QDataStream.Qt_5_9)

            if self.msgLen == 0:
                if totalLen >= self.headLen:
                    self.msgLen = in_.readInt32()
                    if totalLen >= self.headLen + self.msgLen:
                        msg = ""
                        msg = in_.readQString()
                        self.getMsgSignal.emit(msg)
                        self.buffer = self.buffer.right(totalLen - self.headLen - self.msgLen - 4)
                        self.msgLen = 0
                        totalLen = self.buffer.size()
                    else:
                        break
                else:
                    break
            else:
                if totalLen >= self.headLen + self.msgLen:
                    in_.readInt32()
                    msg = ""
                    msg = in_.readQString()
                    self.getMsgSignal.emit(msg)
                    self.buffer = self.buffer.right(totalLen - self.headLen - self.msgLen - 4)
                    self.msgLen = 0
                    totalLen = self.buffer.size()
                else:
                    break
