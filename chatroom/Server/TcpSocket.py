# 这一版的socket发送消息的时候的包头内容仅为后面的发送信息的大小，其实改成整个包的大小的话可扩展性更好，但是懒得改了
from PyQt5.QtNetwork import QTcpSocket
from PyQt5.QtCore import QDataStream, QByteArray, pyqtSignal, QIODevice


# 和客户端连接的socket
class TcpSocket(QTcpSocket):
    getMsgSignal = pyqtSignal(str)  # 获取到一条消息（粘包处理后）

    def __init__(self,parent=None):
        super().__init__(parent)

        self.buffer = QByteArray()  # 接收消息的缓冲区
        self.headLen = 4  # 包头大小
        self.msgLen = 0  # 包身大小

        self.readyRead.connect(self.getMsg)

    # 发送消息
    def writeMsg(self, msg):
        if type(msg) == str:
            sendMsg = QByteArray()
            out = QDataStream(sendMsg, QIODevice.WriteOnly)
            out.setVersion(QDataStream.Qt_5_9)  # 注意发送和接收的版本的一致
            out.writeInt32(len(msg) * 2)  # QDataStream写入的QByteArray一个字符占两个字节，双字节占位
            out.writeQString(msg)
            self.write(sendMsg)

    # 获取消息（粘包处理）
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
                        # 注意4个字节是QDataStream操作QByteArray写入的时候默认写入头部的QByteArray大小，占4个字节
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
