

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TcpClient(object):
    def setupUi(self, TcpClient):
        TcpClient.setObjectName("TcpClient")
        TcpClient.resize(458, 180)
        self.verticalLayout = QtWidgets.QVBoxLayout(TcpClient)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tcpClientStatuslabel = QtWidgets.QLabel(TcpClient)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.tcpClientStatuslabel.setFont(font)
        self.tcpClientStatuslabel.setAlignment(QtCore.Qt.AlignCenter)
        self.tcpClientStatuslabel.setObjectName("tcpClientStatuslabel")
        self.verticalLayout.addWidget(self.tcpClientStatuslabel)
        self.progressBar = QtWidgets.QProgressBar(TcpClient)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.tcpClientBtn = QtWidgets.QPushButton(TcpClient)
        self.tcpClientBtn.setObjectName("tcpClientBtn")
        self.horizontalLayout.addWidget(self.tcpClientBtn)
        self.tcpClientCloseBtn = QtWidgets.QPushButton(TcpClient)
        self.tcpClientCloseBtn.setObjectName("tcpClientCloseBtn")
        self.horizontalLayout.addWidget(self.tcpClientCloseBtn)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(TcpClient)
        QtCore.QMetaObject.connectSlotsByName(TcpClient)

    def retranslateUi(self, TcpClient):
        _translate = QtCore.QCoreApplication.translate
        TcpClient.setWindowTitle(_translate("TcpClient", "接收端"))
        self.tcpClientStatuslabel.setText(_translate("TcpClient", "等待接收文件......"))
        self.tcpClientBtn.setText(_translate("TcpClient", "取消"))
        self.tcpClientCloseBtn.setText(_translate("TcpClient", "关闭"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    TcpClient = QtWidgets.QDialog()
    ui = Ui_TcpClient()
    ui.setupUi(TcpClient)
    TcpClient.show()
    sys.exit(app.exec_())

