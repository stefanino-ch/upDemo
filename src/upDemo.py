from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

import sys
import up
import time
import argparse

import logging
logger = logging.getLogger(__name__)
STDERR_HANDLER = logging.StreamHandler(sys.stderr)
STDERR_HANDLER.setFormatter(logging.Formatter(logging.BASIC_FORMAT))

# pyupdater
from pyupdater.client import Client
# Be careful here. This import work only if "pyupdater init" was run before.
from client_config import ClientConfig

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.buildWindow()
    
    def checkForUpdates(self):
        '''
        Checks if there are updates available
        @return: True if there are updates
        '''
        sys.stdout.write('Check for Updates. Current version %s\n' % up.__version__)
        
        client = Client(ClientConfig(), refresh=True, progress_hooks=[self.log_progress])
        client.refresh()
        
        app_update = client.update_check( ClientConfig.APP_NAME,
                                          ClientConfig.APP_VERSION,
                                          channel='stable')
        
        if app_update: 
            sys.stdout.write('Uptdates found\n')
            return True
        else:
            return False
            sys.stdout.write('NO uptdates found\n')
            
    def downloadNewVersion(self):
        ''' Checks if there is a new version. Does immediately a download if so. 
        '''
        client = Client(ClientConfig(), refresh=True, progress_hooks=[self.log_progress])
        client.refresh()
        
        app_update = client.update_check( ClientConfig.APP_NAME,
                                          ClientConfig.APP_VERSION,
                                          channel='stable')
        if app_update:
            sys.stdout.write('Uptdates found\n')
            if hasattr(sys, "frozen"):
                sys.stdout.write('App is frozen\n')
                
                downloaded = app_update.download()
                sys.stdout.write('App Update downloaded\n')
                if downloaded:
                    sys.stdout.write('Extracting update and restarting...')
                    time.sleep(10)
                    app_update.extract_restart()
            else:
                sys.stdout.write('App is NOT frozen\n')
        else:
            sys.stdout.write('NO uptdates found')
    
    def buildWindow(self):
        self.setWindowTitle("Hello World")
        l = QtWidgets.QLabel("My simple app.")
        l.setMargin(10)
        self.setCentralWidget(l)
        self.show()
        l.setText('checking for updates')
        updateAv = self.checkForUpdates()

        if updateAv:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Update available")
            msgBox.setText("New version available. \n\nWanna update\nPress Cancel to abort.")
            msgBox.setIcon(QMessageBox.Warning)        
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            answer = msgBox.exec()            
            
            if answer == QMessageBox.Ok:
                # User wants to update
                l.setText('downloading....')
                self.downloadNewVersion()
            else: 
                l.setText('Update aborted')
        else: 
            l.setText('No updates found')

    def log_progress(data):
        # Progress hooks get passed a dict with the below keys.
        # total: total file size
        # downloaded: data received so far
        # status: will show either downloading or finished
        # percent_complete: Percentage of file downloaded so far
        # time: Time left to complete download
        # {'total': 40431556, 'downloaded': 40431556, 'status': 'finished', 'percent_complete': '100.0', 'time': '00:00'}
        dataTot = data['total']
        downlded = data['downloaded']
        percCompl = data['percent_complete']
        timeRem = data['time']
        sys.stdout.write(data)
        sys.stdout.write('Data tot:      ' + dataTot +'\n' )
        sys.stdout.write('Downloaded:    ' + downlded +'\n' )
        sys.stdout.write('Perc complete: ' + percCompl +'\n' )
        sys.stdout.write('Time remaining:' + timeRem  +'\n' )
    
    
def ParseArgs(argv):
    """
    Parse command-line args.
    """
    usage = ("%(prog)s [options]\n")
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument("--debug", help="increase logging verbosity", action="store_true")
    parser.add_argument("--version", action='store_true', help="displays version")
    return parser.parse_args(argv[1:])

def InitializeLogging(debug=False):
    """
    Initialize logging.
    """
    logger.addHandler(STDERR_HANDLER)
    if debug:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logger.setLevel(level)
    logging.getLogger("upDemo").addHandler(STDERR_HANDLER)
    logging.getLogger("upDemo").setLevel(level)


    
if __name__ == '__main__':
    
    args = ParseArgs(sys.argv)
    InitializeLogging(args.debug)
    
    sys.stdout.write('Initialized...\n')
    
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    app.exec()