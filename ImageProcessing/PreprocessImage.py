'''
This module is used to preprocess the image before running the Omnipose analysis.
Uses Fiji/ImageJ to turn images in a folder to stack.
Uses SplitStack.py to split the stack into individual frames and store them in folders according to channel.
'''

from ImageJ import SavePlugin, RunPlugin
from Utilities import System, Memory
from ImageProcessing import SplitStack
from Tkinter import ui

import os

'''
path to the folder where the newly preprocessed images are saved.
This will be accessed by ui.py, method OmniposeUI().
'''
savePath = ''

def preprocess(): 
    '''
    Preprocess the raw image stack/folder before running the Omnipose analysis. 

    1. If the selected raw image path is a folder, call plugin "images_To_Stack" stored in Fiji's plugin folder. This plugin turns images inside a folder to stack.

    2. Split the image stack into individual frames and store them in folders according to channel.

    3. Open the splitted image folder in explorer.
    '''
    global savePath

    print('\nPreprocessImage.py: preprocessing image...')
    ui.updateStatus("Preprocessing image...")

    fijiPath = Memory.getFijiPath()
    rawImagePath = Memory.getRawImagePath()
    savePath = Memory.getSavePath()

    if fijiPath != '' and rawImagePath != '' and savePath != '':
        processingFolder = rawImagePath
        savePath = System.createTimeFolder(savePath)

        '''
        1. If the selected raw image path is a folder, call plugin "images_To_Stack" stored in Fiji's plugin folder. This plugin turns images inside a folder to stack.
        '''
        if os.path.isdir(rawImagePath):
            fijiPath = Memory.getFijiPath()
            for script in os.listdir("ImageJ/Plugins"):
                scriptPath = "ImageJ/Plugins/" + script
                SavePlugin.saveToPlugins(fijiPath, scriptPath)

            RunPlugin.RefreshPlugin(processingFolder, savePath, fijiPath, 'Images_To_Stack.py')
            RunPlugin.runPlugin(fijiPath, 'Images_To_Stack.py')
            processingFolder = savePath + "/" + os.path.basename(rawImagePath) + ".tif"
        
        '''
        2. Split the image stack into individual frames and store them in folders according to channel.
        '''
        SplitStack.splitStack(processingFolder, savePath)

        print('PreprocessImage.py: Image preprocessing done.')
        ui.updateStatus("Image preprocessing done.")

        '''
        3. Open the splitted image folder in explorer.
        '''
        System.openInExplorer(savePath)
        
    else: 
        print("ERROR: PreprocessImage.py: One or more paths are empty.")
        ui.updateStatus("ERROR: One or more paths are empty.")