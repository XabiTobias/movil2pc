import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import queue     #If you do not load this template, after pyinstaller is packaged, you may not be able to run the requests template.
import requests
################################################


################################################
class Widget(QWidget):
    def __init__(self, *args, **kwargs):
        super(Widget, self).__init__(*args, **kwargs)
        layout = QHBoxLayout(self)

        # Increase the progress bar
        self.progressBar = QProgressBar(self, minimumWidth=400)
        self.progressBar.setValue(0)
        layout.addWidget(self.progressBar)

        #Add download button
        self.pushButton = QPushButton(self, minimumWidth=100)
        self.pushButton.setText("download")
        layout.addWidget(self.pushButton)

        #binding button event
        self.pushButton.clicked.connect(self.on_pushButton_clicked)




    # Download button event
    def on_pushButton_clicked(self):
        the_url = 'https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user'
        the_filesize = requests.get(the_url, stream=True).headers['Content-Length']
        the_filepath ="D:/sogou_pinyin_93e.exe"
        the_fileobj = open(the_filepath, 'wb')
        #### Create a download thread
        self.downloadThread = downloadThread(the_url, the_filesize, the_fileobj, buffer=10240)
        self.downloadThread.download_proess_signal.connect(self.set_progressbar_value)
        self.downloadThread.start()



    # 
    def set_progressbar_value(self, value):
        self.progressBar.setValue(value)
        if value == 100:
            QMessageBox.information(self, "prompt", "download successful!")
            return






##################################################################
#Downloadthread
##################################################################
class downloadThread(QThread):
    download_proess_signal = pyqtSignal(int)                        #Create signal

    def __init__(self, url, filesize, fileobj, buffer):
        super(downloadThread, self).__init__()
        self.url = url
        self.filesize = filesize
        self.fileobj = fileobj
        self.buffer = buffer


    def run(self):
        try:
            rsp = requests.get(self.url, stream=True)                # download mode
            offset = 0
            for chunk in rsp.iter_content(chunk_size=self.buffer):
                if not chunk: break
                self.fileobj.seek(offset)                            #Set pointer position
                self.fileobj.write(chunk)                            #Write file
                offset = offset + len(chunk)
                proess = offset / int(self.filesize) * 100
                self.download_proess_signal.emit(int(proess))        # 
            #######################################################################
            self.fileobj.close()    #Close file
            self.exit(0)            # thread


        except Exception as e:
            print(e)





####################################
# 
####################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())
