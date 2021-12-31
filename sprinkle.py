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

class Tile:
    def __init__(self, name, path, spriteSize) -> None:
        self.name = name
        self.path = path
        self.image = Image.open(path)
        self.height = math.ceil(self.image.size[1] / spriteSize)
        self.width = math.ceil(self.image.size[0] / spriteSize)
        self.placed = False
        self.location = (0,0)

class Sheet: 
    def __init__(self, spriteSize) -> None:
        self.spriteSize = spriteSize
        self.height = 0
        self.width = 0
        self.rows = []
        self.unplaced = []
        self.placed = []

    def createInitialSheet(self, height, width):
        self.height = height
        self.width = width
        for i in range(self.height):
            self.addRow(True)
                
    def setup(self, forceSquare):
        global verbose
        if verbose:
            print("Optimizing sprite sheet...")
            print("     Creating the initial bounding box.")

        self.unplaced.sort(key=lambda x: x.height)
        firstTile = self.unplaced[-1]
        self.createInitialSheet(firstTile.height, firstTile.width)
        self.placeTile(firstTile)

        self.unplaced.sort(key=lambda x: x.width)
        secondTile = self.unplaced[-1]
        self.placeTile(secondTile)

        if verbose:
            print("     Finding optimal layout.")

        self.unplaced.sort(key=lambda x: x.height)
        while len(self.unplaced) > 0:
            tile = self.unplaced[-1]
            self.placeTile(tile)

        
        if verbose:
            print("     Creating sprite sheet canvas.")

        box = (self.width * self.spriteSize, self.height * self.spriteSize)
        if forceSquare:
            if verbose:
                print("     Forcing square sprite sheet.")
            longSide = self.width
            if self.height > self.width:
                longSide = self.height
            box = (longSide * self.spriteSize, longSide * self.spriteSize)
        sheet = Image.new("RGBA", box)

        if verbose:
            print("     Placing sprites onto the sprite sheet.")

        for tile in self.placed:
            sheet.paste(tile.image, (tile.location[1]*self.spriteSize,tile.location[0]*self.spriteSize))
        
        if verbose:
            print("     Sprite sheet created.\n")
        
        return sheet


    def createTiles(self, imageFiles):
        for i in range(len(imageFiles)):
            newTile = Tile(str(i), imageFiles[i], self.spriteSize)
            self.unplaced.append(newTile)

    def checkNext(self, row, column):
        try:
            if self.rows[row][column] == [0]:
                return True
            else:
                return False
        except IndexError:
            return False

    def findArea(self, height, width):
        for row in range(len(self.rows)):
            for column in range(len(self.rows[row])):
                if self.rows[row][column] == [0]:
                    rowIndex = row
                    columnIndex = column
                    isFree = True
                    for y in range(height):
                        columnIndex = column
                        for x in range(width):
                            isFree = self.checkNext(rowIndex, columnIndex)
                            if not isFree:
                                if columnIndex == column:
                                    return (-1,0)
                                else:
                                    return (0,-1)
                            columnIndex += 1
                        rowIndex += 1
                    return (row, column)
        return (-1,-1)

    def populateTiles(self, tile):
        row = tile.location[0]
        column = tile.location[1]
        for y in range(tile.height):
            column = tile.location[1]
            for x in range(tile.width):
                self.rows[row][column] = [1]
                column += 1
            row += 1

    def placeTile(self, tile):
        location = self.findArea(tile.height, tile.width)
        if location[0] >= 0 and location[1] >= 0:
            self.unplaced.remove(tile)
            self.placed.append(tile)
            tile.location = location
            self.populateTiles(tile)
            return True
        elif location != (-1,-1):
            if location[0] < 0:
                self.addRow()
            else:
                self.addColumn()
            self.placeTile(tile)
        else:
            self.addRow()
            self.addColumn()
            self.placeTile(tile)
        return False

    def addRow(self, initialSetup = False):
        newRow = []
        for i in range(self.width):
            newRow.append([0])
        self.rows.append(newRow)
        if not initialSetup:
            self.height += 1

    def addColumn(self):
        for row in self.rows:
            row.append([0])
        self.width += 1
    
    def printBoard(self):
        print("\nPrinting Board")
        for row in self.rows:
            print(row)

def calculateSetSize(imageFiles, spriteSize, forceSquare):
    if verbose:
        print("Calculating sprite sheet size...")
        print("     Square forcing is set to " + str(forceSquare))
    sheetSize = 0
    tileCount = 0
    for image in imageFiles:
        with Image.open(image) as im:
            tileCount += math.ceil(im.size[0] / spriteSize)
            tileCount += math.ceil(im.size[1] / spriteSize)
    sheetSize = math.ceil(math.sqrt(tileCount))
    sheetSize = (sheetSize, sheetSize)
    if not forceSquare:
        sheetSize = (sheetSize[0], int(tileCount / sheetSize[0]))
    if verbose:
        print("     Sprite sheet size calculated as " + str(sheetSize[0]*spriteSize) + "x" + str(sheetSize[1]*spriteSize) + ".")
    return sheetSize

def setRowColumn(cRow, cColumn, size):
    row = cRow
    column = cColumn
    if cRow + 1 == size[0]:
        row = 0
        column += 1
    else:
        row += 1
    return row, column

def createSheet(imageFiles, spriteSize, compactMode, forceSquare):

    if verbose:
        print("Creating sprite sheet...")
        print("     Compact mode is set to " + str(compactMode) + ".\n")
    
    if compactMode:
        size = calculateSetSize(imageFiles, spriteSize, forceSquare)
        if verbose:
            print("     Placing sprites onto the sprite sheet.")
        sheet = Image.new("RGBA", (size[0] * spriteSize, size[1] * spriteSize))
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
        sheet = Sheet(spriteSize)
        sheet.createTiles(imageFiles)
        sheet = sheet.setup(forceSquare)

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
        "-s, --square       Force square sprite sheet.\n"
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
    square = False

    if len(args) != 0:
        for argument in args:
            if argument == "compact":
                coMode = True
            elif argument == "intact":
                #print("Intact mode is still in development. Mode is set to compact instead.\n")
                coMode = False
            elif argument == "--verbose" or argument == "-v":
                verbose = True
            elif argument == "--square" or argument == "-s":
                square = True
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
    newSheet = createSheet(imList, spSize, coMode, square)

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