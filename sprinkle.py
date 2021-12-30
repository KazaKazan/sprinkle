#!/usr/bin/env python3

import sys, os, math
from PIL import Image

verbose = True

def getImages():
    if verbose:
        print("Finding image files in the current directory.")
    fileList = os.listdir(os.path.abspath(os.getcwd()))
    files = []
    for file in fileList:
        if os.path.isfile(file):
            files.append(file)
    if files != []:
        images = []
        for file in files:
            try:
                with Image.open(file) as im:
                    images.append(file)
            except OSError:
                pass
        if images != []:
            if verbose:
                print("Found " + str(len(images)) + " image files in the current directory.")
            return images
        else:
            sys.exit("No image files found!")
    else:
        sys.exit("No image files found!")

def calculateSetSize(imageFiles, spriteSize = 32, compactMode = True):
    if verbose:
        print("Calculating sprite sheet size. Compact mode is set to " + str(compactMode))
    sheetSize = 0
    if compactMode:
        tileCount = 0
        for image in imageFiles:
            with Image.open(image) as im:
                tileCount += math.ceil(im.size[0] / spriteSize)
                tileCount += math.ceil(im.size[1] / spriteSize)
        sheetSize = math.ceil(math.sqrt(tileCount)) * spriteSize
    else:
        pass
    if verbose:
        print("Sprite sheet size calculated as " + str(sheetSize) + "x" + str(sheetSize))
    return sheetSize