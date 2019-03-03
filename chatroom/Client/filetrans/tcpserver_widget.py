from PyQt5.QtCore import pyqtSlot, pyqtSignal, QFile, QDataStream, QIODevice, QTime, QByteArray
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox, qApp
from PyQt5.QtNetwork import QTcpServer, QHostAddress, QTcpSocket
from filetrans.Ui_tcpserver import Ui_TcpServer


class TcpS(QDialog, Ui_TcpServer):
    """
    Class documentation goes here.
    """

    sendFileName = pyqtSignal(str)

    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(TcpS, self).__init__(parent)
        self.setupUi(self)
        self.payloadSize = 64*1024
        self.totalBytes = 0
        self.bytesWritten = 0
        self.bytesToWrite = 0
        self.theFileName = ""
        self.fileName = ""
        self.localFile = QFile()
        self.outBlock = QByteArray()
        self.time = QTime()
        self.initServer()

    def initServer(self):
        """
        网络设置初始化
        """
        self.tcpPort = 7788
        self.tcpServer = QTcpServer(self)
        self.clientConnection = QTcpSocket(self)
        self.tcpServer.newConnection.connect(self.sendMessage)
        self.serverStatuslabel.setText("请选择要传送的文件")
        self.progressBar.reset()
        self.serverOpenBtn.setEnabled(True)
        self.serverSendBtn.setEnabled(False)
        self.tcpServer.close()   

    def refused(self):
        """
        对端拒绝接收文件
        """
        self.tcpServer.close()
        self.serverStatuslabel.setText("对方拒绝接收")

    def closeEvent(self, event):
        """
        关闭事件
        """
        self.on_serverCloseBtn_clicked()

    def sendMessage(self):
        """
        发送文件
        """
        self.serverSendBtn.setEnabled(False)
        self.clientConnection = self.tcpServer.nextPendingConnection()
        self.clientConnection.bytesWritten.connect(self.updateClientProgress)
        self.serverStatuslabel.setText("开始传送文件 {} ！".format(self.theFileName))

        self.localFile = QFile(self.fileName)
        if not(self.localFile.open(QFile.ReadOnly)):
            errorMsg = "无法读取文件 {}:\n {}".format(self.fileName, self.localFile.errorString())
            QMessageBox.warning(self, "应用程序", errorMsg)
            return

        self.serverCloseBtn.setText("取消")

        self.totalBytes = self.localFile.size()#单位：字节
        sendOut = QDataStream(self.outBlock, QIODevice.WriteOnly)
        sendOut.setVersion(QDataStream.Qt_5_4)
        self.time.start()
        currentFile = self.fileName.split("/")[-1]
        sendOut.writeInt64(0)
        sendOut.writeInt64(0)
        sendOut.writeQString(currentFile)
        self.totalBytes += self.outBlock.size()
        sendOut.device().seek(0)
        sendOut.writeInt64(self.totalBytes)
        sendOut.writeInt64(self.outBlock.size()-2)
        self.bytesToWrite = self.totalBytes - self.clientConnection.write(self.outBlock)
        self.outBlock.resize(0)

    def updateClientProgress(self, numBytes):
        """
        发送进度显示
        """
        qApp.processEvents()
        self.bytesWritten += numBytes
        if self.bytesWritten > 0:
            self.block = self.localFile.read(min(self.bytesToWrite, self.payloadSize))
            self.bytesToWrite -= self.clientConnection.write(self.block)
        else:
            self.localFile.close()

        byteSent = self.bytesWritten / (1024*1024)
        useTime = self.time.elapsed() / 1000
        speed = self.bytesWritten / useTime / (1024*1024)
        total = self.totalBytes / (1024*1024)
        left = (total - byteSent) / speed
        
        if byteSent < 0.01:
            byteSent = self.bytesWritten / 1024
            speed = self.bytesWritten / useTime / 1024
            total = self.totalBytes / 1024
            if left > 0:
                sendInfo = "已发送 {0:.2f}KB（{1:.2f}KB/s)\n共{2:.2f}KB 已用时：{3:.1f}秒\n 估计剩余时间:{4:.1f}秒".format(byteSent, speed, total, useTime, left)
            else:
                sendInfo = "已发送 {0:.2f}KB（{1:.2f}KB/s)\n共{2:.2f}KB 用时：{3:.1f}秒\n".format(byteSent, speed, total, useTime)
        else:
            if left > 0:
                sendInfo = "已发送 {0:.2f}MB（{1:.2f}MB/s)\n共{2:.2f}MB 已用时：{3:.1f}秒\n 估计剩余时间:{4:.1f}秒".format(byteSent, speed, total, useTime, left)
            else:
                sendInfo = "已发送 {0:.2f}MB（{1:.2f}MB/s)\n共{2:.2f}MB 用时：{3:.1f}秒\n".format(byteSent, speed, total, useTime)

        self.progressBar.setMaximum(total)
        self.progressBar.setValue(byteSent)
        
        if self.bytesWritten == self.totalBytes:
            self.serverCloseBtn.setText("关闭")

        self.serverStatuslabel.setText(sendInfo)

    @pyqtSlot()
    def on_serverOpenBtn_clicked(self):
        """
        打开文件
        """
        self.fileName = QFileDialog.getOpenFileName(self, '打开文件', './')[0]
        if self.fileName:
            self.theFileName = self.fileName.split("/")[-1]
            self.serverStatuslabel.setText("要传送的文件为：{}".format(self.theFileName))
            self.serverSendBtn.setEnabled(True)
            self.serverOpenBtn.setEnabled(False)
    
    @pyqtSlot()
    def on_serverSendBtn_clicked(self):
        """
        发送文件
        """
        if not(self.tcpServer.listen(QHostAddress.Any, self.tcpPort)):
            errorMsg = self.tcpServer.errorString()
            QMessageBox.warning(self, "错误", "发送失败：\n {}".format(errorMsg))
            self.TcpServer.close()
            return

        self.serverStatuslabel.setText("等待对方接收... ...")
        self.serverSendBtn.setEnabled(False)
        self.sendFileName.emit(self.theFileName)
    
    @pyqtSlot()
    def on_serverCloseBtn_clicked(self):
        """
        取消或者关闭
        """
        if self.tcpServer.isListening():
            self.tcpServer.close()
            if self.localFile.isOpen():
                self.localFile.close()
            self.clientConnection.abort()

        if self.serverCloseBtn.text() == "取消":
            self.serverCloseBtn.setText("关闭")
        else:
            self.close()
            self.serverOpenBtn.setEnabled(True)
            self.serverSendBtn.setEnabled(False)
            self.progressBar.reset()
            self.totalBytes = 0
            self.bytesWritten = 0
            self.bytesToWrite = 0
            self.serverStatuslabel.setText("请选择要传送的文件")
