from contextlib import redirect_stdout
from io import StringIO

from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import QObject, QThread, pyqtSignal

class Terminal(QTextEdit):
    def __init__(self, parent):
        super(Terminal, self).__init__(parent)

    def keyPressEvent(self, e):
        # print(e.key())
        if e.key() == 16777216:  # Esc
            pass
        elif e.key() == 16777220:  # Enter
            pass
        else:
            self.insertPlainText(e.text())

    def run_func(self, func, *args, **kwargs):
        self.configure()

        self.thread = QThread()
        self.worker = TerminalWorker(func, args, kwargs)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.outputChanged.connect(self.update_terminal)
        self.thread.start()

    def update_terminal(self, text):
        print(text)
        self.setText(text)

    def configure(self):
        self.setReadOnly(True)
        self.setAcceptRichText(False)


class TerminalWorker(QObject):
    finished = pyqtSignal()
    outputChanged = pyqtSignal(str)

    def __init__(self, func, args, kwargs):
        QObject.__init__(self)
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        with redirect_stdout(StringIO()) as f:
            self.func(*self.args, **self.kwargs)
            print(f)
        self.outputChanged.emit(f.getvalue())

