
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TcpServer(object):
    def setupUi(self, TcpServer):
        TcpServer.setObjectName("TcpServer")
        TcpServer.resize(422, 162)
        self.verticalLayout = QtWidgets.QVBoxLayout(TcpServer)
        self.verticalLayout.setObjectName("verticalLayout")
        self.serverStatuslabel = QtWidgets.QLabel(TcpServer)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.serverStatuslabel.setFont(font)
        self.serverStatuslabel.setAlignment(QtCore.Qt.AlignCenter)
        self.serverStatuslabel.setObjectName("serverStatuslabel")
        self.verticalLayout.addWidget(self.serverStatuslabel)
        self.progressBar = QtWidgets.QProgressBar(TcpServer)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.serverOpenBtn = QtWidgets.QPushButton(TcpServer)
        self.serverOpenBtn.setObjectName("serverOpenBtn")
        self.horizontalLayout.addWidget(self.serverOpenBtn)
        self.serverSendBtn = QtWidgets.QPushButton(TcpServer)
        self.serverSendBtn.setObjectName("serverSendBtn")
        self.horizontalLayout.addWidget(self.serverSendBtn)
        self.serverCloseBtn = QtWidgets.QPushButton(TcpServer)
        self.serverCloseBtn.setObjectName("serverCloseBtn")
        self.horizontalLayout.addWidget(self.serverCloseBtn)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(TcpServer)
        QtCore.QMetaObject.connectSlotsByName(TcpServer)

    def retranslateUi(self, TcpServer):
        _translate = QtCore.QCoreApplication.translate
        TcpServer.setWindowTitle(_translate("TcpServer", "发送端"))
        self.serverStatuslabel.setText(_translate("TcpServer", "请选择要发送的文件："))
        self.serverOpenBtn.setText(_translate("TcpServer", "打开"))
        self.serverSendBtn.setText(_translate("TcpServer", "发送"))
        self.serverCloseBtn.setText(_translate("TcpServer", "关闭"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    TcpServer = QtWidgets.QDialog()
    ui = Ui_TcpServer()
    ui.setupUi(TcpServer)
    TcpServer.show()
    sys.exit(app.exec_())

