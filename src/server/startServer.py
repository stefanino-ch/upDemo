import sys
import threading

from fileserver import RunFileServer
from fileserver import WaitForFileServerToStart
from fileserver import ShutDownFileServer
from utils import GetEphemeralPort

def StartFileServer(fileServerDir):
    if not fileServerDir:
        print('Fileserver dir not set.')
        return None

    fileServerPort = GetEphemeralPort()
    thread = threading.Thread(target=RunFileServer,
                              args=(fileServerDir, fileServerPort))
    thread.start()
    WaitForFileServerToStart(fileServerPort)
    return fileServerPort

def Run(argv, clientConfig=None):
    
    fileServerPort = StartFileServer('C:\\Users\\user\\git\\upDemo\\pyu-data\\deploy')
    
    if fileServerPort:
        print('Fileserver Port is: ' + str(fileServerPort) )
    else:
        print('Unable to start fileserver')

if __name__ == "__main__":
    Run(sys.argv)