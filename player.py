import time #found sleep function at https://www.tutorialspoint.com/python3/time_sleep.htm

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

    #check inventory for sword
    def get_sword(self):
        return self.sword

    #insert sword into inventory
    def set_sword(self):
        self.sword = True
        self.equipped = 'sword'

    #check inventory for bow
    def get_bow(self):
        return self.bow

    #insert bow into inventory
    def set_bow(self):
        self.bow = True
        self.equipped = 'bow'

    #check inveentory for shurikens
    def get_shurikens(self):
        return self.shurikens

    #insert shurikens into inventory
    def set_shurikens(self):
        self.shurikens = True
        self.equipped = 'shurikens'

    #check for equipped item
    def get_equipped(self):
        return self.equipped

    #swap equipped item
    def swap_equipped(self, swap):
        self.equipped = swap

    #check for enemy in destination cell
    def enemy_there(self, mapObj, desy, desx):
        if mapObj.objArr[desy][desx].isnumeric() and mapObj.exitArr[desy][desx] < 0:
            # print('you died')
            self.deaths += 1
            return True
        else:
            return False

    #check for item in destination cell
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

    def move(self, keystroke, mapObj):
        desx = 0
        desy = 0
        # moving up
        if keystroke == 'w':
            desy = self.y_pos-1
            desx = self.x_pos

        #moving left
        elif keystroke == 'a':
            desy = self.y_pos
            desx = self.x_pos-1

        # moving down
        elif keystroke == 's':
            desy = self.y_pos+1
            desx = self.x_pos

        #moving right
        elif keystroke == 'd':
            desy = self.y_pos
            desx = self.x_pos+1

        

        #check for out of bounds movement
        if desx >= mapObj.maxX or desx < 0 or desy >= mapObj.maxY or desy < 0:
            return
            
        dest = mapObj.objArr[desy][desx]

        if dest == 'w' or dest.isupper():
             return
        elif self.enemy_there(mapObj, desy, desx):
            # print('You died') # If we include quotes like this,
            # we'll want to print them at a specific location in
            # menu. Perhaps we could create menu functions to
            # call here, and when an item is picked up?
            mapObj.objArr[desy][desx] = 'd'
            mapObj.displayMap()
            # mapObj.stdscr.refresh()
            time.sleep(1)
            mapObj.reset(self)
            mapObj.displayMap()
            return
        elif self.item_there(dest):
            print()
            # print('You picked up the item!')

        elif mapObj.exitArr[desy][desx] == 'q':
            if mapObj.winCheck(self):
                mapObj.objArr[self.y_pos][self.x_pos] = '-'
                dest = 'p'
                mapObj.displayMap()
                dest = mapObj.objArr[desy][desx]
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
        elif mapObj.exitArr[desy][desx] >= 0: #Previously:  elif dest == 'e'
            if mapObj.winCheck(self):
                mapObj.objArr[self.y_pos][self.x_pos] = '-'
                dest = 'p'
                mapObj.displayMap()
                dest = mapObj.objArr[desy][desx]
                mapObj.startY = self.y_pos
                mapObj.startX = self.x_pos
                mapObj.objArr[self.y_pos][self.x_pos] = 'p'
                time.sleep(1)

                for y in range(mapObj.maxY):
                    for x in range(mapObj.maxX):
                        mapObj.initArr[y][x] = mapObj.objArr[y][x]
                return mapObj.exitArr[desy][desx]


                        

        #updates objArr for map
        mapObj.objArr[desy][desx] = 'p'
        if mapObj.exitArr[self.y_pos][self.x_pos] < 0:
            mapObj.objArr[self.y_pos][self.x_pos] = '-'
        else:
            mapObj.objArr[self.y_pos][self.x_pos] = mapObj.initArr[self.y_pos][self.x_pos]
        self.x_pos = desx
        self.y_pos = desy


        mapObj.displayMap()
