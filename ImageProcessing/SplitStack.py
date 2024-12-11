''' 
author: johnmallon
Improved by Min

This module splits a stacked tiff to many single tiffs and stores them in corresponding channel folder.
Also creates a stacked tiff of each channel, for easy viewing.
It can process maximum of 5 channels.
'''

from Tkinter import ui
import os
import sys
import numpy as np
import tifffile

def splitStack(inputPath, outputPath):

    print("\nSplitStack.py: Starting...")
    outputPath = outputPath + r'/Split Stack'

    if os.path.isdir(inputPath):
        files = [f for f in os.listdir(inputPath) if f.endswith(".tif") or f.endswith(".tiff")]
    else:
        files = [os.path.basename(inputPath)]

    inputDir = os.path.dirname(inputPath)

    os.makedirs(outputPath, exist_ok=True)
    # Name list of channel folders
    channelFolders = [outputPath+ r'/Channel 0', outputPath+ r'/Channel 1', outputPath+ r'/Channel 2', outputPath+ r'/Channel 3', outputPath+ r'/Channel 4']

    for filename in files:
        countFrames = 0
        filenameNoExt = os.path.splitext(filename)[0]
        # print("filenameNoExt: ", filenameNoExt)

        print("Processing: ", filename)

        filepath = os.path.join(inputDir, filename)
        print("Filepath: ", filepath)
        array, numberOfChannels, arrayDimensions = arraylize(filepath)
        
        print("Number of channels: ", numberOfChannels)
        print("Array dimension: ", arrayDimensions)

        if (numberOfChannels == 1): 
            channelFolder = channelFolders[0]
            os.makedirs(channelFolder, exist_ok=True)

            if (len(arrayDimensions) == 2): # The file only has a single frame and single channel
                saveChannel(array, 0, outputPath, filenameNoExt)
                saveFrame(array, countFrames, channelFolder, filenameNoExt)

            else: # The file has multiple frames and a single channel
                saveChannel(array, 0, outputPath, filenameNoExt)
                for frame in array:
                    saveFrame(frame, countFrames, channelFolder, filenameNoExt)
                    countFrames += 1

        else: # The file has multiple channels
            
            """
            The array is a list of stacks, and each stack is a list of channels, and each channel is a 2D numpy array of image.
            The array dimension is ordered as (T, C, X, Y).
            We want to get the stack with each individual channel, and save it as stacked tiff.
            We also want to save each frame of each channel as single tiff.
            """
            for i in range(numberOfChannels):
                channelArray = [] # This extra dimension will be removed later
                channelFolder = channelFolders[i]
                os.makedirs(channelFolder, exist_ok=True)

                countFrames = 0
                for stack in array:
                    
                    frame = stack[i]
                    saveFrame(frame, countFrames, channelFolder, filenameNoExt)
                    channelArray.append(frame)
                    countFrames += 1

                channelArray = np.squeeze(channelArray) # Remove the first dimension of the array
                saveChannel(channelArray, i, outputPath, filenameNoExt)
    print("SplitStack.py: Done.")




def arraylize(filepath):
    ''' 
    Return the Numpy array of the given tiff file.
    Also return the number of channels in the tiff file, and the dimensions in its array. 
    Quit the program if the tiff file has more than 4 dimensions. '''
    with tifffile.TiffFile(filepath) as tiffFile:
        tiffArray = tiffFile.asarray()
        arrayDimensions = tiffArray.shape
        numberOfChannels = 1

        if len(tiffArray.shape) == 4:
            numberOfChannels = tiffArray.shape[1] # tifffile ordering of dimensions in a array is (T,C,X,Y)
        elif len(tiffArray.shape) > 4:
            print("Does your image have more than 4 dimensions (X,Y,Time,Channels)? This program is not equiped to deal with this complexity. \nTerminating program now.")
            ui.updateStatus("ERROR: Does your image have more than 4 dimensions (X,Y,Time,Channels)? This program is not equiped to deal with this complexity.")
            sys.exit()

    return tiffArray, numberOfChannels, arrayDimensions


def saveFrame(frame, countFrames, channelFolder, filenameNoExt):
    ''' Save the frame as single tiff in the channelFolders. '''
    name = f"{countFrames}_{filenameNoExt}.tiff"
    path = os.path.join(channelFolder, name)
    tifffile.imwrite(path, frame, photometric='minisblack')


def saveChannel(channel, channelCount, outputPath, filenameNoExt):
    ''' Save the channel array as stacked tiffs in the output folder. '''
    print("Saving channel", channelCount, "...")
    name = f"Channel{channelCount}_{filenameNoExt}.tiff"
    print("Channel name:", name)
    path = os.path.join(outputPath, name)
    print("Channel path:", path)
    tifffile.imwrite(path, channel, photometric='minisblack')
