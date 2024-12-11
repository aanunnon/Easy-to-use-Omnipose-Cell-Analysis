'''
This module is used to run Omnipose on a single channel image folder.
'''

from Utilities import System, Memory
from Tkinter import ui
from ImageJ import RunPlugin, SavePlugin

import os
import subprocess

def runOmnipose(channelFolder, omniposeOption, builtInModel, commandLine, stackResult):
    '''
    Run Omnipose on the given channelFolder. The channelFolder should contain only one channel of images.
    The Omnipose can be run using built-in model, custom model, or through given command line, depending on the omniposeOption.
    '''
    print('\nOmnipose.py: Running Omnipose...')
    ui.updateStatus("Running Omnipose...")

    if (channelFolder == '' or channelFolder is None):
        print('\nERROR: Omnipose.py: Channel folder is empty.')
        ui.updateStatus("ERROR: Channel folder is empty.")
        return
    print('Channel folder:', channelFolder)
    

    if (omniposeOption == 1): #Built-in model
        print('Using built-in model:', builtInModel)
        command = ['omnipose', '--dir', channelFolder, '--use_gpu', '--pretrained_model', builtInModel, '--save_outlines', '--save_txt', '--in_folders', '--no_npy', '--exclude_on_edges']
        subprocess.run(command)


    if (omniposeOption == 2): #Custom model
        customModel = Memory.getCustomModelPath()
        if (customModel == ''):
            print('\nERROR: Omnipose.py: Custom model path is empty.')
            return
        command = ['omnipose', '--dir', channelFolder, '--use_gpu', '--pretrained_model', customModel, '--save_outlines', '--save_txt', '--in_folders', '--no_npy', '--exclude_on_edges']
        subprocess.run(command)


    if (omniposeOption == 3): #Command line
        os.system(commandLine)

    if (stackResult == 1):
        print('\nOmnipose.py: Stacking result...')
        fijiPath = Memory.getFijiPath()
        processingFolder = channelFolder + '/outlines'
        savePath = channelFolder
        if fijiPath!='' and os.path.isdir(processingFolder):
            SavePlugin.saveToPlugins(fijiPath, 'ImageJ/Plugins/Images_To_Stack.py')
            RunPlugin.RefreshPlugin(processingFolder, savePath, fijiPath, 'Images_To_Stack.py')
            RunPlugin.runPlugin(fijiPath, 'Images_To_Stack.py')
        else:
            if fijiPath=='':
                print('\nERROR: Omnipose.py: Path to FIJI/ImageJ is empty, cannot stack outlines')
                ui.updateStatus('ERROR: Path to FIJI/ImageJ is empty, cannot stack outlines')
            else:
                print('\nERROR: Omnipose.py: Path to outlines is empty, cannot stack outlines')
                ui.updateStatus('ERROR: Path to outlines is empty, cannot stack outlines')

    print('Omnipose.py: Omnipose done.')
    ui.updateStatus("Omnipose done.")
    System.openInExplorer(channelFolder)