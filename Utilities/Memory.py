'''
This module contains functions that process the memory.txt file.
'''

def getFijiPath():
    '''
    Returns the path to FIJI stored in the memory.txt file.
    '''
    with open("memory.txt", "r") as m:
        memory = m.read().splitlines()
        fijiPath = memory[1]
    return fijiPath

def getRawImagePath():
    '''
    Returns the path to the raw image stored in the memory.txt file.
    '''
    with open("memory.txt", "r") as m:
        memory = m.read().splitlines()
        rawImagePath = memory[3]
    return rawImagePath

def getSavePath():
    '''
    Returns the path to the save folder stored in the memory.txt file.
    '''
    with open("memory.txt", "r") as m:
        memory = m.read().splitlines()
        savePath = memory[5]
    return savePath

def getCustomModelPath():
    '''
    Returns the path to the custom model stored in the memory.txt file.
    '''
    with open("memory.txt", "r") as m:
        memory = m.read().splitlines()
        customModelPath = memory[7]
    return customModelPath

def getCommandLine():
    '''
    Returns the command line stored in the memory.txt file.
    '''
    with open("memory.txt", "r") as m:
        memory = m.read().splitlines()
        commandLine = memory[9]
    return commandLine

def changeMemory(newPath, pathName):
    '''
    Changes the path in the memory.txt file.
    '''
    if (newPath != '' and newPath is not None):
        indexDict = {"fijiPath": 1, "rawImagePath": 3, "savePath": 5, "customModelPath": 7, "commandLine": 9}
        index = indexDict[pathName]
        with open("memory.txt", "r") as f:
            memory = f.readlines()
            memory[index] = newPath + "\n"
        with open("memory.txt", "w") as f:
            f.write(''.join(memory))
