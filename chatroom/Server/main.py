from PyQt5.QtWidgets import QApplication
import sys
from Server import Server


app = QApplication(sys.argv)

server = Server()

app.exec()