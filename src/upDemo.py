from PyQt5 import QtWidgets

import sys
import up
import time

# pyupdater
from pyupdater.client import Client
from config import ClientConfig

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Hello World")
        l = QtWidgets.QLabel("My simple app.")
        l.setMargin(10)
        self.setCentralWidget(l)
        self.show()
        

def print_status_info(info):
    total = info.get(u'total')
    downloaded = info.get(u'downloaded')
    status = info.get(u'status')
    sys.stdout.write(downloaded, total, status)
    
if __name__ == '__main__':
    
    # pyupdater
    print("version %s\n" % up.__version__)
    client = Client(ClientConfig())
    client.refresh()
    client.add_progress_hook(print_status_info)
    
    
    app_update = client.update_check( ClientConfig.APP_NAME,
                                      ClientConfig.APP_VERSION,
                                      channel='stable')
    if app_update:
        print('app_update')
        if hasattr(sys, "frozen"):
            downloaded = app_update.download()
            if downloaded:
                sys.stdout.write('Extracting update and restarting...')
                time.sleep(10)
                app_update.extract_restart()
        else:
            sys.stdout.write('not frozen')
    else:
        print('sorry, no app_update')
    
    # normal app
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    app.exec()