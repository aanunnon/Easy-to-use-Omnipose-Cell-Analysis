''' 
This module contains functions that deals with operating system.
'''

import os
import platform
import subprocess
from datetime import datetime

def createTimeFolder(path):
    ''' 
    Creates a folder named by date and time at creation in the given path.
    Returns the path of the folder.
    '''
    folder = path + "/" + datetime.today().strftime('%Y-%m-%d %Hh%Mm%Ss')
    os.makedirs(folder)
    print('System.py: folder created: ' + folder)
    return folder

def openInExplorer(path):
    '''
    Open the given path in the system's explorer.
    '''
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])