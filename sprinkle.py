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
                print("     Found " + str(len(images)) + " image files in the current directory.\n")
            return images
        else:
            sys.exit("      No image files found!\n")
    else:
        sys.exit("      No image files found!\n")

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
        sheetSize = math.ceil(math.sqrt(tileCount))
    else:
        pass
    if verbose:
        print("     Sprite sheet size calculated as " + str(sheetSize) + "x" + str(sheetSize) + "\n")
    return sheetSize

def setRowColumn(cRow, cColumn, size):
    row = cRow
    column = cColumn
    if cRow + 1 == size:
        row = 0
        column += 1
    else:
        row += 1
    return row, column

def createSheet(imageFiles, size, spriteSize = 32, compactMode = True):
    if verbose:
        print("Creating sprite sheet.")
    sheet = Image.new("RGBA", (size * spriteSize, size * spriteSize))
    if verbose:
        print("     Placing sprites onto the sprite sheet.")
    if compactMode:
        row = 0
        column = 0
        for i in range(len(imageFiles)):
            with Image.open(imageFiles[i]) as im:
                if im.size[0] > spriteSize or im.size[1] > spriteSize:
                    rowTotal = math.ceil(im.size[0] / spriteSize)
                    columnSection = 0
                    columnTotal = math.ceil(im.size[1] / spriteSize)
                    columnEnd = spriteSize
                    while columnSection < columnTotal:
                        rowSection = 0
                        rowEnd = spriteSize
                        while rowSection < rowTotal:
                            box = (rowSection * spriteSize, columnSection * spriteSize, rowEnd, columnEnd)
                            section = im.crop(box)
                            rowSection += 1
                            rowEnd = (rowSection + 1) * spriteSize
                            if rowEnd > im.size[0]:
                                rowEnd = im.size[0]
                            if len(section.getcolors()) == 1 and section.getcolors()[0][1] == (0, 0, 0, 0):
                                pass
                            else:
                                sheet.paste(section, (spriteSize * row, spriteSize * column))
                            row, column = setRowColumn(row, column, size)
                        columnSection += 1
                        columnEnd = (columnSection + 1) * spriteSize
                        if columnEnd < im.size[1]:
                            columnEnd = im.size[1]
                else:
                    sheet.paste(im, (spriteSize * row, spriteSize * column))
                    row, column = setRowColumn(row, column, size)
        if verbose:
            print("     Sprite sheet created.")
    else:
        pass
    sheet.show()
