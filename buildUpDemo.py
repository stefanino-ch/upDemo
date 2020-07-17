# Does execute all commands needed to build the upDemo app.
# The version number is read from the source code.

import os
import src.up

cmds = [ "pyupdater build --console --app-version " + src.up.__version__ +" src/upDemo.py",\
      "pyupdater pkg --process",\
      "pyupdater pkg --process --sign" ]
      

for cmd in cmds:
    print('\n')
    print(cmd)
    os.system('cmd /c ' + cmd)

