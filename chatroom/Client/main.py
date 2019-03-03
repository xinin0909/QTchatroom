from PyQt5.QtWidgets import QApplication, QDialog
import sys
from Data import Data
from LoginGui import LoginGui
from MainGui import MainGui

app = QApplication(sys.argv)
if len(sys.argv) == 3:
    srv_host = sys.argv[1]
    srv_port = int(sys.argv[2])
else:
    srv_host = "10.8.44.178"
    srv_port = 8888
data = Data(srv_host, srv_port)
loginGui = LoginGui()
data.addSignalSlot(loginGui)
if loginGui.exec() == QDialog.Accepted:
    mainGui = MainGui()
    data.addSignalSlot(mainGui)
    mainGui.show()
    app.exec()
