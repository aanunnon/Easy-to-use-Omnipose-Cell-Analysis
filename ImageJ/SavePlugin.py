'''
This module saves the scripts inside the Plugins folder into FIJI's "/scripts/Plugins" folder.

By saving the scripts into FIJI's "/scripts/Plugins" folder, the script can be used directly as a plugin. This allows calling PyimageJ's run_plugin('PluginName') and run the script in FIJI remotely. 

Note: 
- The script should have "_" in its name, so FIJI recognizes it as plugin.
'''

from Tkinter import ui

import os

def readScript(scriptPath): 
    '''
    Reads the script file and returns its content.
    '''
    with open(scriptPath, "r") as s:
        script = s.readlines()
    return script

def saveToPlugins(fijiPath, scriptPath):
    '''
    Saves the script file into the given fijiPath's "/scripts/Plugins" folder.
    If the folder does not exist, print an error message.
    '''
    script = readScript(scriptPath)
    pluginName = os.path.basename(scriptPath)
    plugins_folder = fijiPath + '/scripts/Plugins/'

    if os.path.exists(plugins_folder):
        with open(plugins_folder + pluginName, "w") as file:
            file.write(''.join(script))
            print("SavePlugin.py: Saved", pluginName, "in plugins folder.")

    else:
        print("ERROR: SavePlugin.py:", plugins_folder, "does not exist.")
        ui.updateStatus("ERROR: " + plugins_folder + " does not exist.")