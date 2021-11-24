# Joint effort by: Jerry Smedley, Jacob Hilt, Melissa Barnes, Mark Montes, Anthony Chin
# This work is made available under the "MIT License". Please see the file LICENSE in this distribution for license terms.

# found sleep function at https://www.tutorialspoint.com/python3/time_sleep.htm
import time


class Player:
    inventory = []

    def __init__(self):
        self.x_pos = 0
        self.y_pos = 0
        self.sword = False
        self.bow = False
        self.shurikens = False
        self.debug = False
        self.key = 0
        self.deaths = 0
        self.equipped = None

    # check inventory for sword
    def get_sword(self):
        return self.sword

    # insert sword into inventory
    def set_sword(self):
        self.sword = True
        self.equipped = 'sword'

    # check inventory for bow
    def get_bow(self):
        return self.bow

    # insert bow into inventory
    def set_bow(self):
        self.bow = True
        self.equipped = 'bow'

    # check inventory for shurikens
    def get_shurikens(self):
        return self.shurikens

    # insert shurikens into inventory
    def set_shurikens(self):
        self.shurikens = True
        self.equipped = 'shurikens'

    # check for equipped item
    def get_equipped(self):
        return self.equipped

    # swap equipped item
    def swap_equipped(self, swap):
        self.equipped = swap

    # check for enemy in destination cell
    def enemy_there(self, mapObj, y_destination, x_destination):
        if mapObj.objArr[y_destination][x_destination].isnumeric() and mapObj.exitArr[y_destination][x_destination] < 0:
            # print('you died')
            self.deaths += 1
            return True
        else:
            return False

    # check for item in destination cell
    def item_there(self, dest):
        if dest == 's':
            self.set_sword()
            return True
        elif dest == 'b':
            self.set_bow()
            return True
        elif dest == 'h':
            self.set_shurikens()
            return True
        elif dest == 'k':
            self.key += 1
            return True
        else:
            return False

    def move(self, keystroke, mapObj, fileNum):
        x_destination = 0
        y_destination = 0
        # moving up
        if keystroke == 'w':
            y_destination = self.y_pos - 1
            x_destination = self.x_pos

        # moving left
        elif keystroke == 'a':
            y_destination = self.y_pos
            x_destination = self.x_pos - 1

        # moving down
        elif keystroke == 's':
            y_destination = self.y_pos + 1
            x_destination = self.x_pos

        # moving right
        elif keystroke == 'd':
            y_destination = self.y_pos
            x_destination = self.x_pos + 1

        # check for out of bounds movement
        if x_destination >= mapObj.maxX or x_destination < 0 or y_destination >= mapObj.maxY or y_destination < 0:
            return

        dest = mapObj.objArr[y_destination][x_destination]

        if dest == 'w' or dest.isupper():
            return
        elif self.enemy_there(mapObj, y_destination, x_destination):
            # print('You died') # If we include quotes like this,
            # we'll want to print them at a specific location in
            # menu. Perhaps we could create menu functions to
            # call here, and when an item is picked up?
            mapObj.objArr[y_destination][x_destination] = 'd'
            mapObj.displayMap()
            # mapObj.stdscr.refresh()
            time.sleep(1)
            mapObj.reset(self)
            mapObj.displayMap()
            return
        elif self.item_there(dest):
            print()
            # print('You picked up the item!')

        # Previously:  elif dest == 'e'
        elif mapObj.exitArr[y_destination][x_destination] >= 0:
            '''
            if mapObj.exitArr[y_destination][x_destination] < fileNum:
                for y in range(mapObj.maxY):
                    for x in range(mapObj.maxX):
                        mapObj.initArr[y][x] = mapObj.objArr[y][x]
                return mapObj.exitArr[y_destination][x_destination]
            '''

            if mapObj.winCheck(self) or mapObj.exitArr[y_destination][x_destination] < fileNum:
                '''
                mapObj.objArr[self.y_pos][self.x_pos] = '-'
                dest = 'p'
                mapObj.displayMap()
                dest = mapObj.objArr[y_destination][x_destination]
                '''
                mapObj.startY = self.y_pos
                mapObj.startX = self.x_pos
                '''
                mapObj.objArr[self.y_pos][self.x_pos] = 'p'
                time.sleep(1)
                '''

                for y in range(mapObj.maxY):
                    for x in range(mapObj.maxX):
                        mapObj.initArr[y][x] = mapObj.objArr[y][x]
                return mapObj.exitArr[y_destination][x_destination]

        '''
        elif mapObj.exitArr[y_destination][x_destination] == 'q':
            if mapObj.winCheck(self):
                mapObj.objArr[self.y_pos][self.x_pos] = '-'
                dest = 'p'
                mapObj.displayMap()
                dest = mapObj.objArr[y_destination][x_destination]
                mapObj.startY = self.y_pos
                mapObj.startX = self.x_pos
                time.sleep(1)

                for y in range(mapObj.maxY):
                    for x in range(mapObj.maxX):
                        mapObj.initArr[y][x] = mapObj.objArr[y][x]
                # I tried just using initArr = objArr here,
                # but that results in the init array updating with
                # every player input

                return -1
        '''

        # updates objArr for map
        mapObj.objArr[y_destination][x_destination] = 'p'
        if mapObj.exitArr[self.y_pos][self.x_pos] < 0:
            mapObj.objArr[self.y_pos][self.x_pos] = '-'
        else:
            mapObj.objArr[self.y_pos][self.x_pos] = mapObj.initArr[self.y_pos][self.x_pos]
        self.x_pos = x_destination
        self.y_pos = y_destination

        mapObj.displayMap()
