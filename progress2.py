import os, sys
from PyQt5 import QtWidgets, QtCore


class Extended(QtCore.QThread):
    """
    For running copy operation
    """
    copied_percent_signal= QtCore.pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.src_file = 'test.txt'
        self.dst_file = 'test_copy.txt'
        self.file_size = os.stat(self.src_file).st_size

    def run(self):
        self.copyfileobj(self.src_file, self.dst_file, self.my_callback)

    def my_callback(self, temp_file_size):
        percent = int(temp_file_size/self.file_size*100)
        print("Copiedd: {}".format(percent))
        self.copied_percent_signal.emit(percent)

    def copyfileobj(self, fsrc, fdst, callback, length=16*1024):
        copied = 0
        with open(fsrc, "rb") as fr, open(fdst, "wb") as fw:
            while True:
                buff = fr.read(length)
                if not buff:
                    break
                fw.write(buff)
                copied += len(buff)
                callback(copied)


class MyApp(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Instance attribute defined later in on_button_click()
        self.ext = None

        self.w = QtWidgets.QWidget()
        self.w.setWindowTitle("Progress bar copy test")

        # Add widgets on the window
        self.copy_button = QtWidgets.QPushButton("Copy", self)
        self.copy_button.sizeHint()
        self.progress_bar = QtWidgets.QProgressBar(self)
        self.progress_bar.setGeometry(0, 40, 300, 25)
        self.progress_bar.setMaximum(100)

        self.copy_button.clicked.connect(self.on_button_click)

    def on_button_click(self):
        self.copy_button.setDisabled(True)
        self.ext = Extended()
        self.ext.copied_percent_signal.connect(self.on_count_change)
        self.ext.start()
        self.ext.join()

    def on_count_change(self, value):
        self.progress_bar.setValue(value)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    prog = MyApp()
    prog.show()
    sys.exit(app.exec_())