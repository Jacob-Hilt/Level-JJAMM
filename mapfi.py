import curses
from curses import wrapper
import creature
#import os

class Map:
    initArr = []
    objArr = []
    maxY = 0
    maxX = 0
    winCond = 'L'
    # stdscr
    
    def printInitLets(self):
        for y in range(self.maxY):
            #print(y)
            for x in range(self.maxX):
                print(self.initArr[y][x], end = '')
            print()

    def printObjLets(self):
        for y in range(self.maxY):
            #print(y)
            for x in range(self.maxX):
                print(self.objArr[y][x], end = '')
            print()


    def loadMap(self, inFile):
        curFile = open(inFile, 'r')
        self.maxX = len(curFile.readline()) - 1
        self.maxY = 0
        for line in curFile:
            if line != '\n':
                self.maxY += 1
            else:
                break
        self.maxY += 1
        self.initArr = [[0 for y in range(self.maxX+1)] for x in range(self.maxY)] # https://stackoverflow.com/questions/2397141/how-to-initialize-a-two-dimensional-array-in-python
        self.objArr = [[0 for y in range(self.maxX+1)] for x in range(self.maxY)] # https://stackoverflow.com/questions/2397141/how-to-initialize-a-two-dimensional-array-in-python
        y = 0
        x = 0
        curFile.seek(0) # https://www.tutorialspoint.com/How-to-use-seek-method-to-reset-a-file-read-write-position-in-Python
        for line in curFile:
            x = 0
            if line != '\n':
                for character in line:
                    self.initArr[y][x] = character
                    self.objArr[y][x] = character
                    if character == 'p':
                        yPos = y
                        xPos = x
                    x += 1
                y += 1
            else:
                break

        for line in curFile:
            for character in line:
                if character != '\n':
                    self.winCond = character
        return yPos, xPos
        '''
        y = 0
        for line in curFile:
            x = 0
            if line != '\n':
                for character in line:
                    self.objArr[y][x] = character
                    x += 1
                y += 1
            else:
                break
        '''

    #Jerry wrote loadEnemy which is a modified loadMap
    def loadEnemy(self, inFile):
        curFile = open(inFile, 'r')
        self.maxX = len(curFile.readline()) - 1
        self.maxY = 0
        for line in curFile:
            if line != '\n':
                self.maxY += 1
            else:
                break
        self.maxY += 1
        self.initArr = [[0 for y in range(self.maxX+1)] for x in range(self.maxY)] # https://stackoverflow.com/questions/2397141/how-to-initialize-a-two-dimensional-array-in-python
        self.objArr = [[0 for y in range(self.maxX+1)] for x in range(self.maxY)] # https://stackoverflow.com/questions/2397141/how-to-initialize-a-two-dimensional-array-in-python
        y = 0
        x = 0
        enemies = []
        curFile.seek(0) # https://www.tutorialspoint.com/How-to-use-seek-method-to-reset-a-file-read-write-position-in-Python
        for line in curFile:
            x = 0
            if line != '\n':
                for character in line:
                    self.initArr[y][x] = character
                    self.objArr[y][x] = character
                    try:
                        character = int(character)
                    except ValueError:
                        character = 0
                    if character != 0:
                        enemy = creature.creature(character, x, y)
                        enemies.append(enemy)
                    x += 1
                y += 1
            else:
                break
        return enemies

    def mapSwitch(self, obj):
        if obj.isupper():
            return obj, 7
        elif obj == '1':
            return 'X', 1

        elif obj == 's':
            return '|', 5

        elif obj == 'b':
            return 'M', 5

        elif obj == 'p':
            return ' ', 2

        elif obj == 'k':
            return ' ', 3

        elif obj == 'e':
            return ' ', 6

        elif obj == 'w':
            return ' ', 7

        elif obj == 'd':
            return 'X', 8

        else:
            return ' ', 4


    def setupMap(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)

        winY = curses.LINES - 1
        winX = curses.COLS - 1

        win = curses.newwin(winY, winX, 0, 0)
        curses.start_color()
        curses.init_pair(8, curses.COLOR_RED, curses.COLOR_GREEN)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLUE)
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
        curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)

    def displayMap(self):
        for y in range(self.maxY):
            for x in range(self.maxX):
                symbol, color = self.mapSwitch(self.objArr[y][x])
                self.stdscr.addstr(y, x, symbol, curses.color_pair(color))

    def reset(self, playObj):
        resKey = 0
        for y in range(self.maxY):
            for x in range(self.maxX):
                if self.initArr[y][x] == 'p':
                    playObj.y_pos = y
                    playObj.x_pos = x
                if self.initArr[y][x] == 'k' and self.objArr[y][x] != 'k':
                    resKey += 1
                self.objArr[y][x] = self.initArr[y][x]
        if self.winCond == 'S':
            playObj.sword = False
        elif self.winCond == 'B':
            playObj.bow = False
        elif self.winCond == 'K':
            playObj.key -= resKey

        self.displayMap()

    def winCheck(self, playObj):
        if self.winCond == 'T':
            return True
        elif self.winCond == 'E': 
            # check if all enemies defeated
            for y in range(self.maxY):
                for x in range(self.maxX):
                    if self.objArr[y][x].isnumeric():
                        return False
            return True
        elif self.winCond == 'S':
            return playObj.sword
        elif self.winCond == 'B':
            return playObj.bow
        elif self.winCond == 'K':
            if playObj.key > 0:
                playObj.key -= 1
                return True


    def game(self, creature, player, menu):
        print('temp')

