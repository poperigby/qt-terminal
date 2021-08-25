import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        loadUi("test.ui", self)
        self.pushButton.pressed.connect(self.pushButtonPushed)

    def pushButtonPushed(self):
        self.embeddedTerminal.run_func(input, "test")


app = QApplication(sys.argv)
window = UI()
window.show()

sys.exit(app.exec_())
