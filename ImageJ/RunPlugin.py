'''
This module is used to remotely run plugin in FIJI/ImageJ.
Relies on the imagej library.
'''

from Tkinter import ui
import os
import imagej

def RefreshPlugin(rawImagePath, savePath, fijiPath, plugin_filename):
    '''
    Refresh the plugin's local input paths of the raw image and save folder.
    Detects the paths variables in the plugin script and replaces them with the new paths.
    '''
    plugin_path = fijiPath + '/scripts/Plugins/' + plugin_filename
    if os.path.isfile(plugin_path):

        with open(plugin_path, "r") as p:
            script = p.readlines()

            # This is a silly way to detect the paths variables in the script, but it works:
            # It looks for the line that contains the flag "Flag: rawImagePath" and the line that contains the flag "Flag: savePath", 
            # then it replaces the next line with the new path.
            for index, line in enumerate(script):
                if "Flag: rawImagePath" in line:
                    script[index+1] = "\tloadFolder ='" + rawImagePath + "'\n"
                
                if "Flag: savePath" in line:
                    script[index+1] = "\tsavePath ='" + savePath + "'\n"

        with open(plugin_path, "w") as p:
            p.write(''.join(script))
        
    else:
        print("\nERROR: RunFijiPlugin.py: plugin "+plugin_filename+" not found in Fiji/ImageJ's Plugins folder")
        ui.updateStatus("ERROR: plugin "+plugin_filename+" not found in Fiji/ImageJ's Plugins folder")

def runPlugin(fijiPath, plugin_filename):
    '''
    Run a plugin in FIJI.
    Relies on the imagej library.
    '''
    # Change the underscore to space and remove the '.py' at the end. 
    # This should end up to be the name that shows up in FIJI's plugin menu tab.
    plugin_name = plugin_filename.replace("_", " ")
    plugin_name = plugin_name[:-3]

    print('\nRunFijiPlugin.py: Initiating FIJI...')
    fiji = imagej.init(fijiPath)
    print('\nRunFijiPlugin.py: Running plugin ' + plugin_filename)
    fiji.py.run_plugin(plugin_name)
    print('\nRunFijiPlugin.py: disposing FIJI...')
    fiji.dispose()