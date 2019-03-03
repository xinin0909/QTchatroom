
from PyQt5.QtCore import pyqtSlot, QTime, QDataStream, QFile
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtNetwork import QTcpSocket, QAbstractSocket
from filetrans.Ui_tcpclient import Ui_TcpClient


class TcpC(QDialog, Ui_TcpClient):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(TcpC, self).__init__(parent)
        self.setupUi(self)
        self.TotalBytes = 0
        self.bytesReceive = 0
        self.fileNameSize = 0
        self.bytesToReceive = 0
        self.fileName = ""
        self.tcpClient = QTcpSocket(self)
        self.tcpPort = 7788
        self.time = QTime()

        self.tcpClient.readyRead.connect(self.readMessage)
        self.tcpClient.error.connect(self.displayError)

    def setHostAddress(self, address):
        """
        设置服务器地址
        """
        self.hostAddress = address
        self.newConnect()

    def setFileName(self, file):
        """
        待接收文件的文件名
        """
        self.localFile = QFile(file)

    def closeEvent(self, event):
        """
        关闭事件
        """
        self.on_tcpClientCloseBtn_clicked()

    def newConnect(self):
        """
        连接服务器并开始计时
        """
        self.tcpClient.abort()
        self.tcpClient.connectToHost(self.hostAddress, self.tcpPort)
        self.time.start()

    def readMessage(self):
        """
        读取文件数据
        """
        receiver = QDataStream(self.tcpClient)
        receiver.setVersion(QDataStream.Qt_5_4)

        if self.bytesReceive <= 2:
            if self.tcpClient.bytesAvailable() >= 2 and self.fileNameSize == 0:
                self.TotalBytes = receiver.readInt64()
                self.fileNameSize = receiver.readInt64()
                self.bytesReceive += 2

            if self.tcpClient.bytesAvailable() >= self.fileNameSize and self.fileNameSize != 0:
                self.fileName = receiver.readQString()
                self.bytesReceive += self.fileNameSize
                if not(self.localFile.open(QFile.WriteOnly)):
                    QMessageBox.warning(self, "应用程序", "无法读取文件 {}：\n {}".format(self.fileName, self.localFile.errorString()))
                    return
            else:
                return

        if self.bytesReceive < self.TotalBytes:
            self.bytesReceive += self.tcpClient.bytesAvailable()
            inBlock = self.tcpClient.readAll()
            self.localFile.write(inBlock)
            inBlock.resize(0)

        useTime = self.time.elapsed() / 1000
        
        bytesReceived = self.bytesReceive / (1024*1024)
        speed = bytesReceived / useTime
        total = self.TotalBytes / (1024*1024)
        left = (total - bytesReceived) / speed

        if bytesReceived < 0.01:
            bytesReceived = self.bytesReceive / 1024
            speed = bytesReceived / useTime / 1024
            total = self.TotalBytes / 1024
            if left > 0:
                msg = "已接收 {0:.2f} KB ({1:.2f}KB/s)\n共{2:.2f}KB.已用时：{3:.1f}秒\n估计剩余时间：{4:.1f}秒".format(bytesReceived, speed, total, useTime, left)
            else:
                msg = "已接收 {0:.2f} KB ({1:.2f}KB/s)\n共{2:.2f}KB.已用时：{3:.1f}秒\n".format(bytesReceived, speed, total, useTime)

        else:
            if left > 0:
                msg = "已接收 {0:.2f} MB ({1:.2f}MB/s)\n共{2:.2f}MB.已用时：{3:.1f}秒\n估计剩余时间：{4:.1f}秒".format(bytesReceived, speed, total, useTime, left)
            else:
                msg = "已接收 {0:.2f} MB ({1:.2f}MB/s)\n共{2:.2f}MB.已用时：{3:.1f}秒\n".format(bytesReceived, speed, total, useTime)

        self.progressBar.setMaximum(total)
        self.progressBar.setValue(bytesReceived)

        self.tcpClientStatuslabel.setText(msg)
        
        if self.bytesReceive == self.TotalBytes:
            self.localFile.close()
            self.tcpClient.close()
            self.tcpClientStatuslabel.setText("接收文件{}完毕".format(self.fileName))
            self.tcpClientBtn.setEnabled(False)


    def displayError(self, socketError):
        """
        显示错误
        """
        if socketError == QAbstractSocket.RemoteHostClosedError:
            pass
        else:
            errorMsg = self.tcpClient.errorString()
            QMessageBox.warning(self, "应用程序", errorMsg)
            return

    @pyqtSlot()
    def on_tcpClientBtn_clicked(self):
        """
        取消接收
        """
        self.tcpClient.abort()
        if self.localFile.isOpen():
            self.localFile.close()
        
        self.tcpClientBtn.setEnabled(False)
    
    @pyqtSlot()
    def on_tcpClientCloseBtn_clicked(self):
        """
        关闭
        """
        self.tcpClient.abort()
        if self.localFile.isOpen():
            self.localFile.close()
        self.close()
        self.tcpClientBtn.setEnabled(True)
