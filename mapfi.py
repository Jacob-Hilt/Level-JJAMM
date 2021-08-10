#Joint effort by: Jerry Smedley, Jacob Hilt, Melissa Barnes, Mark Montes, Anthony Chin
#This work is made available under the "MIT License". Please see the file LICENSE in this distribution for license terms.

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
    exitArr = []
    startY = 0
    startX = 0
    enemyArr = []
    # stdscr
    
    def printInitLets(self):
        for y in range(self.maxY):
            #print(y)
            for x in range(self.maxX):
                self.stdscr.addstr(self.maxY + 2 + y, 0 + x, self.objArr[y][x], curses.color_pair(10))
                # print(self.initArr[y][x], end = '')
            print()

    def printObjLets(self):
        for y in range(self.maxY):
            #print(y)
            for x in range(self.maxX):
                self.stdscr.addstr(self.maxY + 2 + y, self.maxX + 3 + x, self.initArr[y][x], curses.color_pair(10))
                # print(self.objArr[y][x], end = ' ')
            print()

    def printExits(self):
        for y in range(self.maxY):
            #print(y)
            for x in range(self.maxX):
                print(self.exitArr[y][x], end = ', ')
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
        self.exitArr = [[-1 for y in range(self.maxX+1)] for x in range(self.maxY)] # https://stackoverflow.com/questions/2397141/how-to-initialize-a-two-dimensional-array-in-python
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
                        self.startY = y
                        self.startX = x

                    x += 1
                y += 1
            else:
                break

        for line in curFile:
            for character in line:
                if character != '\n':
                    self.winCond = character



        return self.startY, self.startX
    
    def loadExits(self):
        for y in range(self.maxY):
            for x in range(self.maxX):
                if self.initArr[y][x] == 'e':
                    self.initArr[y][x] = '-'
                    self.objArr[y][x] = '-'
                    ex = x + 1
                    exNum = ''
                    while self.initArr[y][ex] != 'e' and ex < self.maxX:
                        exNum += self.initArr[y][ex]
                        ex += 1
                    if exNum.isnumeric():
                        exNum = int(exNum)
                    x += 1
                    while self.objArr[y][x] != 'e' and ex < self.maxX:
                        self.exitArr[y][x] = exNum
                        x += 1
                    if self.objArr[y][x] == 'e':
                        self.objArr[y][x] = '-'
                        self.initArr[y][x] = '-'

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
    # has been updated to no longer reloads map
    def loadEnemy(self):
        enemies = []
        for y in range(self.maxY):
            for x in range(self.maxX):
                character = self.objArr[y][x]
                try:
                    character = int(character)
                except ValueError:
                    character = 0
                if(self.exitArr[y][x] >= 0):
                     character = 0
                if character != 0:
                    enemy = creature.creature()
                    enemy.typ = character
                    enemy.xpos = x 
                    enemy.ypos = y
                    enemies.append(enemy)
        self.enemyArr = enemies
        return enemies

    def mapSwitch(self, obj, y, x):
        if obj.isupper():
            return obj, 7
        elif obj.isnumeric() and self.exitArr[y][x] < 0:
            return 'X', 1

        elif obj == 's':
            return '|', 5

        elif obj == 'b':
            return 'M', 5

        elif obj == 'h':
            return '+', 5

        elif obj == 'b_u_atk':
            return '^', 5

        elif obj == 'b_d_atk':
            return 'v', 5

        elif obj == 'b_l_atk':
            return '<', 5

        elif obj == 'b_r_atk':
            return '>', 5

        elif obj == 'p':
            return ' ', 2

        elif obj == 'k':
            return ' ', 3

        elif obj == 'sh_atk':
            return '+', 5


        elif (obj.isnumeric() and self.exitArr[y][x] >= 0) or obj == 'q':
            return obj, 6

        elif obj == 'w':
            return ' ', 7

        elif obj == 'd':
            return 'X', 8

        else:
            return ' ', 4


    def setupMap(self):
        self.stdscr = curses.initscr()
        self.stdscr.nodelay(True)
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
                symbol, color = self.mapSwitch(self.objArr[y][x], y, x)
                self.stdscr.addstr(y, x, symbol, curses.color_pair(color))
        self.stdscr.refresh()

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
        playObj.key -= resKey
        
        self.enemyArr = []
        self.loadEnemy()
        
        self.displayMap()

    def winCheck(self, playObj):
        if self.winCond == 'T':
            return True
        elif self.winCond == 'E': 
            # check if all enemies defeated
            for y in range(self.maxY):
                for x in range(self.maxX):
                    if self.objArr[y][x].isnumeric() and self.exitArr[y][x] < 0:
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

