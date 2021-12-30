#!/usr/bin/env python3

import sys, os
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
            print("No image files found!")
    else:
        print("No image files found!")