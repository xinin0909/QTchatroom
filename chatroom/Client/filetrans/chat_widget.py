
import json
import sys
import codecs
from PyQt5.QtCore import pyqtSlot, Qt, QByteArray, QDataStream, QIODevice, QProcess, QFile, QTextStream, QDateTime, QTimer
from PyQt5.QtGui import QFont, QColor, QTextCharFormat, QTextCursor
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QMessageBox, QFileDialog, QColorDialog, QMenu, QApplication, QHeaderView, QAction
from PyQt5.QtNetwork import QUdpSocket, QHostInfo, QNetworkInterface, QAbstractSocket, QHostAddress
from Ui_widget import Ui_Widget
from tcpserver_widget import TcpS
from tcpclient_widget import TcpC


class Chat(QWidget, Ui_Widget):
    """
    Class documentation goes here.
    """

    Message, NewParticipant, ParticipantLeft, FileName, Refuse = range(5)

    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(Chat, self).__init__(parent)
        self.setupUi(self)
        self.networkInit()
        self.userTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.splitter.setStretchFactor(0, 7)
        self.splitter.setStretchFactor(1, 3)
        self.splitter_2.setStretchFactor(0, 6)
        self.splitter_2.setStretchFactor(1, 5)
        self.fileName = ""

    def network(self):
        #若接收数据正常，udpsocket->bytesAvailable()的值将为0，接收不到数据则为非零值，这样就可用个定时器，是不是的检测下，若不为零，将SOCKET重启即可。
        self.udpSocket = QUdpSocket(self)
        self.port = 12345
        self.udpSocket.bind(self.port,QUdpSocket.ShareAddress | QUdpSocket.ReuseAddressHint)
        self.udpSocket.readyRead.connect(self.processPendingDatagrams)

    def networkInit(self):
        """
        网络环境初始化配置
        """
        self.network()
        self.sendMessage(Chat.NewParticipant)
        self.server = TcpS(self)
        self.server.sendFileName[str].connect(self.getFileName)
        currentUser = "局域网聊天小工具 | 当前用户：{} | IP：{}".format(self.getUserName(), self.getIP())
        self.setWindowTitle(currentUser)

    def newParticipant(self, userName, localHostName, ipAddress):
        """
        新用户上线
        """
        isEmpty = self.userTableWidget.findItems(ipAddress, Qt.MatchExactly)

        if not(isEmpty):
            user = QTableWidgetItem(userName)
            host = QTableWidgetItem(localHostName)
            ip = QTableWidgetItem(ipAddress)

            self.userTableWidget.insertRow(0)
            self.userTableWidget.setItem(0, 0, user)
            self.userTableWidget.setItem(0, 1, host)
            self.userTableWidget.setItem(0, 2, ip)

            self.messageBrowser.setTextColor(Qt.gray)
            self.messageBrowser.setCurrentFont(QFont("Times New Roman", 10))
            online_user = "{}在线".format(userName)
            self.messageBrowser.append(online_user)
            online_user_cnt = "在线人数：{}".format(self.userTableWidget.rowCount())
            self.userNumLabel.setText(online_user_cnt)
            self.sendMessage(Chat.NewParticipant)
    
    def participantLeft(self, username, ipAddress, time):
        """
        剩余用户
        """
        findItem = self.userTableWidget.findItems(ipAddress, Qt.MatchExactly)
        if findItem:
            rowNum = findItem[0].row()
            self.userTableWidget.removeRow(rowNum)
            self.messageBrowser.setTextColor(Qt.gray)
            self.messageBrowser.setCurrentFont(QFont("Times New Roman",10))
            offline_user = "{} 于 {} 离开！".format(username, time)
            self.messageBrowser.append(offline_user)
            online_user_cnt = "在线人数：{}".format(self.userTableWidget.rowCount())
            self.userNumLabel.setText(online_user_cnt)

    def saveFile(self, fileName):
        """
        保存文件
        """
        SuffixFileName = fileName.split(".")[1]
        if SuffixFileName in ("htm", "html"):
            content = self.messageBrowser.toHtml()
        else:
            content = self.messageBrowser.toPlainText()
        try:
            with codecs.open(fileName, 'w', encoding="gbk") as f:
                f.write(content)
            return True
        except IOError:
            QMessageBox.critical(self, "保存错误", "聊天记录保存失败！")
            return False


    def closeEvent(self, event):
        """
        关闭程序
        """
        self.sendMessage(Chat.ParticipantLeft)

    def hasPendingFile(self, userName, serverAddress, clientAddress, fileName):
        ipAddress = self.getIP()
        if ipAddress == clientAddress:
            isreceive = "来自{}({})的文件：{}，是否接收？".format(userName, serverAddress, fileName)
            btn = QMessageBox.information(self, "接收文件", isreceive, QMessageBox.Yes, QMessageBox.No)
            if btn == QMessageBox.Yes:
                name = QFileDialog.getSaveFileName(self, "保存文件", fileName)
                if name[0]:
                    client = TcpC(self)
                    client.setFileName(name[0])
                    client.setHostAddress(QHostAddress(serverAddress))
                    client.exec()
            else:
                self.sendMessage(Chat.Refuse, serverAddress)
                self.udpSocket.close()
                self.network()

    def processPendingDatagrams(self):
        """
        处理数据
        """
        while self.udpSocket.hasPendingDatagrams():
            data, host, port = self.udpSocket.readDatagram(self.udpSocket.pendingDatagramSize())

            datagram = str(data, encoding='utf-8')

            datagramDict = json.loads(datagram)

            messageType = datagramDict["messageType"]
            userName = datagramDict["userName"]
            localHostName = datagramDict["localHostName"]
            ipAddress = datagramDict["ipAddress"]

            time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")

            if messageType == Chat.Message:
                message = datagramDict["message"]
                isAtUsername = self.findAt(message)
                if isAtUsername == self.getUserName():
                    QApplication.alert(self, 0)
                
                self.messageBrowser.setTextColor(Qt.blue)
                self.messageBrowser.setCurrentFont(QFont("Times New Roman", 12))
                self.messageBrowser.append("[" + userName + "]" + time)
                self.messageBrowser.append(message)

            elif messageType == Chat.NewParticipant:
                self.newParticipant(userName, localHostName, ipAddress)

            elif messageType == Chat.ParticipantLeft:
                self.participantLeft(userName, ipAddress, time)

            elif messageType == Chat.FileName:
                clientAddress = datagramDict["clientAddress"]
                fileName = datagramDict["sendFileName"]
                self.hasPendingFile(userName, ipAddress, clientAddress, fileName)

            elif messageType == Chat.Refuse:
                serverip = ipAddress
                ipAddress = self.getIP()
                if ipAddress == serverip:
                    self.server.refused()

    def getFileName(self, name):
        """
        待传输文件的文件名
        """
        self.fileName = name
        self.sendMessage(Chat.FileName)

    def findAt(self, message):
        """
        找到@的人
        """
        for row in range(self.userTableWidget.rowCount()):
            username = self.userTableWidget.item(row, 0).text()
            Atusername = "@" + username
            if message.find(Atusername) >= 0:
                return username
        return "NotFound"

    def sendMessage(self, messageType, serverAddress = ""):
        """
        发送消息
        """
        localHostName = QHostInfo.localHostName()
        ipAddress = self.getIP()

        username = self.getUserName()
        data = {"messageType":messageType, "userName":username, "localHostName":localHostName}
        
        if messageType == Chat.Message:
            if self.messageTextEdit.toPlainText() == "":
                QMessageBox.warning(self, "警告", "发送内容不能为空", QMessageBox.Ok)
                return

            message = self.getMessage()
            data["ipAddress"] = ipAddress
            data["message"] = message

        elif messageType in (Chat.NewParticipant, Chat.ParticipantLeft):
            data["ipAddress"] = ipAddress

        elif messageType == Chat.FileName:
            row = self.userTableWidget.currentRow()
            clientAddress= self.userTableWidget.item(row, 2).text()
            # message = self.getMessage()
            data["ipAddress"] = ipAddress
            data["clientAddress"] = clientAddress
            data["sendFileName"] = self.fileName
        
        elif messageType == Chat.Refuse:
            data["ipAddress"] = serverAddress

        jdata = json.dumps(data)
        encodeData = bytes(jdata, encoding="utf-8")

        self.udpSocket.writeDatagram(encodeData, QHostAddress.Broadcast, self.port)

    def getIP(self):
        """
        获得用户IP
        """
        addressList = QNetworkInterface.allAddresses()
        for address in addressList:
            if address.protocol() == QAbstractSocket.IPv4Protocol and address != QHostAddress.LocalHost and address.toString()[:3] != "169" and address.toString().split(".")[-1] != "1":
                return address.toString()
        return "0.0.0.0"

    def getMessage(self):
        """
        获得消息
        """
        msg = self.messageTextEdit.toHtml()
        self.messageTextEdit.clear()
        self.messageTextEdit.setFocus()
        return msg

    def getUserName(self):
        """
        获得用户名
        """
        envVariables = ["USERNAME" , "USER" , "HOSTNAME" , "DOMAINNAME"]
        environment = QProcess.systemEnvironment()
        for var in environment:
            varlist = var.split("=")
            isfide = varlist[0] in envVariables
            if isfide:
                return varlist[1]
        return "unKnow"
    
    def mergeFormatDocumentOrSelection(self, format):
        """
        格式处理，改变即可见到效果，不需要选中文字。
        """
        cursor = self.messageTextEdit.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.Document)

        cursor.mergeCharFormat(format)
        self.messageTextEdit.mergeCurrentCharFormat(format)

    def contextMenuEvent(self, event):
        """
        @TA
        """
        items = self.userTableWidget.selectedItems()
        if items:
            selectedUserName = self.userTableWidget.selectedItems()[0].text()
            if selectedUserName != self.getUserName():
                pmenu = QMenu(self)
                pContact = QAction('@TA', self.userTableWidget)
                pmenu.addAction(pContact)
                pmenu.popup(self.mapToGlobal(event.pos()))
                pContact.triggered.connect(lambda :self.ContactTA(selectedUserName))
    
    def ContactTA(self, username):
        """
        @TA的格式
        """
        userAt = "<font color=\'#FF0000\' size='5'>@{} </font>".format(username)
        self.messageTextEdit.append(userAt)
        self.messageTextEdit.setFocus()

    @pyqtSlot(str)
    def on_SizeComboBox_currentIndexChanged(self, p0):
        """
        字体大小下拉框选择变化
        """
        fmt = QTextCharFormat()
        fmt.setFontPointSize(int(p0))
        self.mergeFormatDocumentOrSelection(fmt)
        self.messageTextEdit.setFocus()
    
    @pyqtSlot(str)
    def on_fontComboBox_currentIndexChanged(self, p0):
        """
        字体下拉框选择变化
        """
        fmt = QTextCharFormat()
        fmt.setFontFamily(p0)
        self.mergeFormatDocumentOrSelection(fmt)

        self.messageTextEdit.setFocus()
    
    @pyqtSlot(bool)
    def on_boldToolBtn_clicked(self, checked):
        """
        是否字体加粗
        """
        fmt = QTextCharFormat()
        fmt.setFontWeight(checked and QFont.Bold or QFont.Normal)
        self.mergeFormatDocumentOrSelection(fmt)

        self.messageTextEdit.setFocus()
    
    @pyqtSlot(bool)
    def on_italicToolBtn_clicked(self, checked):
        """
        斜体
        """
        fmt = QTextCharFormat()
        fmt.setFontItalic(checked)
        self.mergeFormatDocumentOrSelection(fmt)
        self.messageTextEdit.setFocus()
    
    @pyqtSlot(bool)
    def on_underlineToolBtn_clicked(self, checked):
        """
        下划线
        """
        fmt = QTextCharFormat()
        fmt.setFontUnderline(checked)
        self.mergeFormatDocumentOrSelection(fmt)
        self.messageTextEdit.setFocus()

    @pyqtSlot(bool)
    def on_colorToolBtn_clicked(self):
        """
        颜色选择
        """
        col = QColorDialog.getColor(self.messageTextEdit.textColor(), self)
        if not col.isValid():
            return
        fmt = QTextCharFormat()
        fmt.setForeground(col)
        self.mergeFormatDocumentOrSelection(fmt)
        self.messageTextEdit.setFocus()
    
    @pyqtSlot()
    def on_saveToolBtn_clicked(self):
        """
        保存聊天记录
        """
        if self.messageBrowser.document().isEmpty():
            QMessageBox.warning(self, "警告", "聊天记录为空,无法保存!", QMessageBox.Ok)
        else:
            fileName = QFileDialog.getSaveFileName(self, "保存聊天记录", "./聊天记录", ("ODT files (*.odt);;HTML-Files (*.htm *.html)"))
            if fileName[0]:
                if self.saveFile(fileName[0]):
                    QMessageBox.information(self, "聊天记录保存", "保存成功！")
    
    @pyqtSlot()
    def on_clearToolBtn_clicked(self):
        """
        清空聊天记录
        """
        self.messageBrowser.clear()
    
    @pyqtSlot()
    def on_sendButton_clicked(self):
        """
        发送消息
        """
        self.sendMessage(Chat.Message)
    
    @pyqtSlot()
    def on_exitButton_clicked(self):
        """
        退出
        """
        self.close()

    @pyqtSlot()
    def on_sendToolBtn_clicked(self):
        """
        选择文件发送对象
        """
        userlist = self.userTableWidget.selectedItems()

        if not(userlist):
            QMessageBox.warning(self, "选择用户", "请先从用户列表选择要传送的用户!", QMessageBox.Ok)
            return
 
        row = userlist[0].row()

        if self.userTableWidget.item(row, 2).text() == self.getIP():
            QMessageBox.information(self, "提示", "不能发给自己哦！")
        else:
            self.server.exec()