#!/usr/bin/env python3

import sys, os, math
from PIL import Image

verbose = False

def getImages():
    if verbose:
        print("Finding image files in the current directory...")
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
            sys.exit("      No image files found! Exiting...\n")
    else:
        sys.exit("      No image files found! Exiting...\n")

def calculateSetSize(imageFiles, spriteSize, compactMode):
    if verbose:
        print("Calculating sprite sheet size...")
        print("     Compact mode is set to " + str(compactMode) + ".")
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
        print("     Sprite sheet size calculated as " + str(sheetSize) + "x" + str(sheetSize) + ".\n")
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

def createSheet(imageFiles, spriteSize, compactMode):
    size = calculateSetSize(imageFiles, spriteSize, compactMode)
    if verbose:
        print("Creating sprite sheet...")
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
            print("     Sprite sheet created.\n")
    else:
        pass
    return sheet

def usage():
    message = (
        "Usage: sprinkle [options] [arguments]\n"
        "\nOptions and arguments may be passed in any order.\n"
        "\nHelp option will always be checked first, if it's passed, the program will display this message and exit regardless of other arguments.\n"
        "\nAll arguments are optional and will fallback to defaults if not passed.\n"
        "\nArguments are parsed in the order they're passed, if the same type of argument is passed more than once, the last argument will override the former arguments of its type.\n"
        "\nCheck pillow documentation for supported file formats.\n"
        "\nhttps://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html\n"
        "\nOPTIONS\n\n"
        "-v, --verbose      Set verbose mode on.\n"
        "-h, --help         Show this message.\n"
        "\nARGUMENTS\n\n"
        "Name               Format/Options              Default\n"
        "------------------------------------------------------\n"
        "Sprite Sheet Mode  compact/intact              compact\n"
        "Sprite Size        <integer>                   32\n"
        'Output File        <filename>.<format>         sheet.png\n'
        "\nCheck the documentation for detailed explanations.\n"
        "https://github.com/KazaKazan/sprinkle"
    )
    sys.exit(message)

def main():
    global verbose

    if "--help" in sys.argv or "-h" in sys.argv:
        usage()

    args = sys.argv
    args.pop(0)

    spSize = 32
    output = "sheet.png"
    coMode = True

    if len(args) != 0:
        for argument in args:
            if argument == "compact":
                coMode = True
            elif argument == "intact":
                print("Intact mode is still in development. Mode is set to compact instead.\n")
            elif argument == "--verbose" or argument == "-v":
                verbose = True
            else:
                argumentCheck = argument.split(".")
                try:
                    hasExtension = argumentCheck[1]
                    output = argument
                except IndexError:
                    try:
                        spSize = int(argument)
                    except ValueError:
                        message = 'Cannot parse argument "' + argument + '". Check "sprinkle --help" for help.'
                        sys.exit(message)

    imList = getImages()
    newSheet = createSheet(imList, spSize, coMode)

    if verbose:
        print("Checking if output dir exists...")
    outputExists = os.path.isdir("output")
    if outputExists:
        if verbose:
            print("     Output dir exists.\n")
        pass
    else:
        if verbose:
            print("     Output dir doesn't exist, creating dir...")
        os.makedirs("output")
        if verbose:
            print("     Output dir created.\n")

    if verbose:
        print("Saving sheet...")

    newSheet.save("output/" + output)

    if verbose:
        print('     Sprite sheet saved to "' + output + '".\n')

main()
if verbose:
    print("Done!")