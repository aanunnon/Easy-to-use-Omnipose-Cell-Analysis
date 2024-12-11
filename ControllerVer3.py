'''
By Min
Co-author: johnmallon

A FIJI/ImageJ dependent program that generates outlines from images of cell shape. 
Only processes tiff images.
Uses FIJI/ImageJ for creating image stack. 
Uses Omnipose to find outline of cell shape.
Uses tkinter for ui.
'''

from Tkinter import ui

import os
from tkinter import *

def main():
    '''
    Main function of the OmniposeCellAnalysis program.
    '''

    # Set current working directory to the OmniposeCellAnalysis folder
    workingDir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(workingDir)
    print("Current working directory:", workingDir)

    # Set up tkinter ui
    root = Tk()
    ui.setUp(root)
    root.mainloop()

if __name__ == "__main__":
    main()