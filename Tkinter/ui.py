'''
This module sets the User Interface for the Omnipose Cell Analysis program.
'''

from Utilities import Memory, System
from ImageProcessing import PreprocessImage
from ImageProcessing import Omnipose

from tkinter import *
from tkinter import filedialog
import tkinter.font
from cellpose_omni.models import MODEL_NAMES

global PATH_SELECTED
PATH_SELECTED = ''
statusLine = None
rootWindow = None

def askFile(initialdirectory=""):
    '''
    Pops up a file dialog to let user choose a file.
    - Because tkinter's button can't return variable, the file's path is stored in a global variable to be accessed by the calling function.
    '''
    global PATH_SELECTED
    PATH_SELECTED = ''
    selection = filedialog.askopenfilename(initialdir=initialdirectory)
    if selection:
        PATH_SELECTED = selection

def askDirectory(initialdirectory=""):
    '''
    Pops up a file dialog to let user choose a directory.
    - Because tkinter's button can't return variable, the file's path is stored in a global variable to be accessed by the calling function.
    '''
    global PATH_SELECTED
    PATH_SELECTED = ''
    selection = filedialog.askdirectory(initialdir=initialdirectory)
    if selection:
        PATH_SELECTED = selection

def changeText(label, text):
    ''' Change the label's text to the given text, if the given text is not empty. '''
    if (text != '' and text is not None): 
        label["text"] = text

def updateStatus(text):
    '''
    Change the status line with the given text, then updates the root window.
    '''
    global rootWindow
    global statusLine
    statusLine["text"] = text
    rootWindow.update()

def ImageJUI(frame):
    ''' 
    Create widgets in the given frame:
    - A label displaying the path to FIJI/ImageJ.
    - A button to let user to change the path.
    '''
    fijiPath = Memory.getFijiPath()

    title = Label(frame, text="ImageJ", width=40, background="lightgray", fg="gray0")
    title.pack(fill="x")

    pathDisplay = Label(frame, text=fijiPath, wraplength=400, bg="gray90", fg="gray15", justify="left")
    pathDisplay.pack(fill="both")

    buttonChooseFile = Button(frame, text="select FIJI/ImageJ", command=lambda: [askFile(), changeText(pathDisplay, PATH_SELECTED), Memory.changeMemory(PATH_SELECTED, "fijiPath")])
    buttonChooseFile.pack()
    
def rawImageUI(frame):
    ''' 
    Create widgets in the given frame:
    - A label displaying the path to the image stack/image folder/single image to be processed.
    - A button to let user to change the path to a new file.
    - A button to let user to change the path to a new directory.
    '''
    global PATH_SELECTED
    rawImagePath = Memory.getRawImagePath()

    title = Label(frame, text="Raw Image", background="lightgray", fg="gray0")
    title.pack(fill="x")

    pathDisplay = Label(frame, text=rawImagePath, wraplength=400, bg="gray90", fg="gray15", justify="left")
    pathDisplay.pack(fill="both")

    buttonChooseFile = Button(frame, text="choose image stack/single image", command=lambda: [askFile(), changeText(pathDisplay, PATH_SELECTED), Memory.changeMemory(PATH_SELECTED, "rawImagePath")])
    buttonChooseFile.pack()
    
    buttonChooseDirectory = Button(frame, text="choose image folder", command=lambda: [askDirectory(), changeText(pathDisplay, PATH_SELECTED), Memory.changeMemory(PATH_SELECTED, "rawImagePath")])
    buttonChooseDirectory.pack()

def saveFolderUI(frame):
    ''' 
    Create widgets in the given frame:
    - A label displaying the path to the save folder.
    - A button to let user to change the path to a new directory.
    '''
    global PATH_SELECTED

    title = Label(frame, text="Save Folder", background="lightgray", fg="gray0")
    title.pack(fill="x")

    pathDisplay = Label(frame, text=Memory.getSavePath(), wraplength=400, bg="gray90", fg="gray15", justify="left")
    pathDisplay.pack(fill="both")

    buttonChooseDirectory = Button(frame, text="choose folder", command=lambda: [askDirectory(), changeText(pathDisplay, PATH_SELECTED), Memory.changeMemory(PATH_SELECTED, "savePath")])
    buttonChooseDirectory.pack()

    buttonChooseDirectory = Button(frame, text="Open folder", command=lambda: [System.openInExplorer(Memory.getSavePath())])
    buttonChooseDirectory.pack()

def preprocessImageButton(frame):
    ''' 
    Button to preprocess the image. 
    This splits the image stack into individual frames and store them in different channel folders.
    '''
    button_preprocessImage = Button(frame, text="Preprocess image", command= lambda: [PreprocessImage.preprocess()])
    button_preprocessImage.pack(fill="both", padx=20)

def OmniposeCommand(channelFolderPath):
    '''
    Returns the complete Omnipose command line.
    '''
    return 'omnipose --dir "' + channelFolderPath + '" ' + Memory.getCommandLine()

def OmniposeUI(frame):
    '''
    Spaghetti code that creates the Omnipose UI. It has the following widgets:
    - Select channel folder
        - A label displaying the path to the selected channel folder.
        - A button to let user to change the channel folder path to a new directory.
    - Select Omnipose model, built-in or custom, or manual command line
        - Radiobutton for Built-in model option
            - A dropdown menu to select the built-in model
        - Radiobutton for Custom model option
            - A label displaying the path to the custom model.
            - A button to let user to change the custom model path to a new file.
        - Radiobutton for Manual Command line option
            - A label displaying the command line.
            - An entry to let user to write the command line.
            - A button to let user to update the command line.
    - Run Omnipose Button
    '''
    global PATH_SELECTED

    # Select channel folder
    selectChannelFrame = Frame(frame, borderwidth=2, relief="groove")
    selectChannelFrame.pack(fill="both", expand=True)

    selectedChannelDisplay = Label(selectChannelFrame, wraplength=400, width=30, bg="gray90", fg="gray15", justify="left")
    selectedChannelDisplay.pack(fill="both")

    button_selectChannel = Button(selectChannelFrame, text="Select channel folder", command=lambda: [[askDirectory(PreprocessImage.savePath+"/Split Stack"), changeText(selectedChannelDisplay, PATH_SELECTED), changeText(commandLineDisplay, OmniposeCommand(PATH_SELECTED))] if PreprocessImage.savePath!='' else [askDirectory(Memory.getSavePath()), changeText(selectedChannelDisplay, PATH_SELECTED)], changeText(commandLineDisplay, OmniposeCommand(PATH_SELECTED))])
    button_selectChannel.pack()

    # Select Omnipose model, built-in or custom, or manual command line
    omniposeOption = IntVar(frame, 1)

    """ Built-in model option """
    buildInModelFrame = Frame(frame, borderwidth=2, relief="groove")
    buildInModelFrame.pack(fill="both", expand=True)
    
    Radiobutton_useBuiltInModel = Radiobutton(buildInModelFrame, text="Use built-in model", variable=omniposeOption, value=1, background="lightgray", fg="gray0")
    Radiobutton_useBuiltInModel.pack(fill="x")

    builtInModel = StringVar(frame, MODEL_NAMES[0])
    dropdown_builtInModel = OptionMenu(buildInModelFrame, builtInModel, *MODEL_NAMES)
    dropdown_builtInModel.pack()

    """ Custom model option """
    customModelFrame = Frame(frame, borderwidth=2, relief="groove")
    customModelFrame.pack(fill="both", expand=True)

    radiobutton_useCustomModel = Radiobutton(customModelFrame, text="Use custom model", variable=omniposeOption, value=2, background="lightgray", fg="gray0")
    radiobutton_useCustomModel.pack(fill="x")

    customModelDisplay = Label(customModelFrame, text=Memory.getCustomModelPath(), wraplength=400, bg="gray90", fg="gray15", justify="left")
    customModelDisplay.pack(fill="both")

    button_chooseCustomModel = Button(customModelFrame, text="Choose custom model", command=lambda: [askFile(), changeText(customModelDisplay, PATH_SELECTED), Memory.changeMemory(PATH_SELECTED, "customModelPath")])
    button_chooseCustomModel.pack()

    """ Manual Command line option """
    commandLineFont = tkinter.font.Font(family="Courier New", size=12, weight="bold")

    manualCommandLineFrame = Frame(frame, borderwidth=2, relief="groove")
    manualCommandLineFrame.pack(fill="both", expand=True)

    Radiobutton_useCommandLine = Radiobutton(manualCommandLineFrame, text="Use manual command line", variable=omniposeOption, value=3, background="lightgray", fg="gray0")
    Radiobutton_useCommandLine.pack(fill="x")

    commandLineDisplay = Label(manualCommandLineFrame, text=OmniposeCommand(selectedChannelDisplay["text"]), wraplength=400, bg="gray90", fg="gray15", justify="left")
    commandLineDisplay.pack(fill="both")

    entry_commandLine = Entry(manualCommandLineFrame)
    entry_commandLine.pack(fill="both")
    button_commandLine = Button(manualCommandLineFrame, text="Enter", command=lambda: [Memory.changeMemory(entry_commandLine.get(), "commandLine"), changeText(commandLineDisplay, OmniposeCommand(selectedChannelDisplay["text"]))])
    button_commandLine.pack()

    # Run Omnipose
    runOmniposeFrame = Frame(frame, borderwidth=2, relief="groove")
    runOmniposeFrame.pack(fill="both", expand=True)

    stackResult = IntVar(frame, 1)
    stackResultCheckbutton = Checkbutton(runOmniposeFrame, text="Also create a stacked version of outlines", variable=stackResult, onvalue=1, offvalue=0)
    stackResultCheckbutton.pack()

    button_runOmnipose = Button(runOmniposeFrame, text="Run Omnipose", command= lambda: [Omnipose.runOmnipose(selectedChannelDisplay["text"], omniposeOption.get(), builtInModel.get(), commandLineDisplay["text"], stackResult.get())])
    button_runOmnipose.pack(fill="both", padx=20)

def setUp(root):
    '''
    Set up the UI.
    '''
    global statusLine
    global rootWindow
    rootWindow = root

    root.title("Omnipose Cell Analysis")
    root.minsize(550, 500)

    statusBar = Frame(root, borderwidth=2, relief="groove", background="lightgray", height=30)
    statusBar.pack(side="bottom", fill="both")
    statusLine = Label(statusBar, text="", background="lightgray", padx=15)
    statusLine.pack(side="left")
    
    sideBar = Frame(root)
    sideBar.pack(side="left", fill="both", expand=True)

    fijiFrame = Frame(sideBar, borderwidth=2, relief="groove")
    fijiFrame.pack(fill="both", expand=True)
    ImageJUI(fijiFrame)

    rawImageSelectionFrame = Frame(sideBar, borderwidth=2, relief="groove")
    rawImageSelectionFrame.pack(fill="both", expand=True)
    rawImageUI(rawImageSelectionFrame)

    saveFolserSelectionFrame = Frame(sideBar, borderwidth=2, relief="groove")
    saveFolserSelectionFrame.pack(fill="both", expand=True)
    saveFolderUI(saveFolserSelectionFrame)

    preprocessImageFrame = Frame(sideBar, borderwidth=2, relief="groove")
    preprocessImageFrame.pack(fill="both", expand=True)
    preprocessImageButton(preprocessImageFrame)

    OmniposeBar = Frame(root)
    OmniposeBar.pack(side="right", fill="both", expand=True)
    OmniposeUI(OmniposeBar)