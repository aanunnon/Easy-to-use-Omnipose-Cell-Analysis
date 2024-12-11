"""
author: johnmallon

This script takes individual images a creates a stack of them. You should MANUALLY save the stack after inspecting it.

This script should be run in the imageJ macro window.
"""

'''
Edited by Min

A copy of this script will be saved to FIJI's scripts/Plugins folder by Controller.py.
The empty variables will be changed by RunPlugin.py with its RefreshPlugin() method.
The script should not be run on itself. The RunPlugin.py will call it as FIJI plugin.
'''

from ij import IJ, ImagePlus, ImageStack
import os
import re


def main():
	#Flag: timelapse
	timelapse = False
	#Flag: rawImagePath
	loadFolder = ''
	#Flag: savePath
	savePath = ''

	savePath = savePath + "/" + os.path.basename(loadFolder)

	if loadFolder == '':
		print("ERROR: [Plugin]Images_To_Stack.py: no raw images directory. ")
	elif savePath == '':
		print("ERROR: [Plugin]Images_To_Stack.py: no saving directory. ")
	else:
		print("\n[Plugin]Images_To_Stack.py: Starting...")
		print("[Plugin info]")
		print("load folder: "+loadFolder)

		files = [f for f in os.listdir(loadFolder) if not f.endswith('.DS_Store')]  # ignore .DS_Store file

		if timelapse:
			files.sort(key=lambda x: int(re.search(r'^(\d+)_', x).group(1)))
		stack = ImageStack()

		for frame in files:
			file_path = os.path.join(loadFolder, frame)
			imp = IJ.openImage(file_path)
			stack.addSlice(frame, imp.getProcessor())
			imp.close()


		# output_image = ImagePlus(os.path.dirname(loadFolder), stack)
		output_image = ImagePlus(os.path.dirname(loadFolder), stack)
		output_image.setDimensions(1,1,len(files)) #set channels, Z, and T appropriately
		IJ.save(output_image, savePath)
		print("Stack saved to " + savePath)

main()
