from src.start_menu import *
import src.menu
import src.player
import re
import time
from src.endscreen import *

# copied exactly from: https://stackoverflow.com/questions/5967500/how-to-correctly-sort-a-string-with-a-number-inside
def atoi(text):
    return int(text) if text.isdigit() else text


# copied exactly from: https://stackoverflow.com/questions/5967500/how-to-correctly-sort-a-string-with-a-number-inside
def natural_keys(text):
    return [atoi(command) for command in re.split(r'(\d+)', text)]


def check_enemy_type(xPos, yPos, mapArr, fileNum):
    for enemy in mapArr[fileNum].enemyArr:
        if enemy.xpos == xPos and enemy.ypos == yPos:
            return enemy.typ
    return -1


def kill_enemy(xPos, yPos, mapArr, fileNum, enemyType):
    for enemy in mapArr[fileNum].enemyArr:
        if enemy.xpos == xPos and enemy.ypos == yPos and enemy.typ == enemyType:
            enemy.dead()


def use_sword(command, playObj, mapObj, mapArr, fileNum):
    if not playObj.get_sword():
        # display 'no sword' message in menu
        return
    x_destination = playObj.x_pos
    y_destination = playObj.y_pos
    if command == curses.KEY_LEFT:
        if playObj.x_pos > 0:
            x_destination -= 1
    if command == curses.KEY_RIGHT:
        if playObj.x_pos < mapObj.maxX - 1:
            x_destination += 1
    if command == curses.KEY_UP:
        if playObj.y_pos < mapObj.maxY - 1:
            y_destination -= 1
    if command == curses.KEY_DOWN:
        if playObj.y_pos > 0:
            y_destination += 1

    if x_destination >= mapObj.maxX or x_destination < 0 or y_destination >= mapObj.maxY or y_destination < 0:
        return
    enemyTyp = check_enemy_type(x_destination, y_destination, mapArr, fileNum)
    if (mapObj.objArr[y_destination][x_destination].isnumeric() and mapObj.exitArr[y_destination][x_destination] >= 0) or \
            mapObj.objArr[y_destination][x_destination] == '-' or \
            (mapObj.objArr[y_destination][x_destination].isnumeric() and mapObj.exitArr[y_destination][x_destination] < 0 and enemyTyp == 1):
        previous = mapObj.objArr[y_destination][x_destination]
        mapObj.objArr[y_destination][x_destination] = 's'
        mapObj.displayMap()
        kill_enemy(x_destination, y_destination, mapArr, fileNum, enemyTyp)
        if previous == '-' or \
                (previous.isnumeric() and mapObj.exitArr[y_destination][x_destination] < 0 and check_enemy_type(x_destination, y_destination, mapArr, fileNum) == 1):
            mapObj.objArr[y_destination][x_destination] = '-'
            time.sleep(0.2)
            mapObj.displayMap()
        elif previous.isnumeric() and mapObj.exitArr[y_destination][x_destination] >= 0:
            mapObj.objArr[y_destination][x_destination] = mapObj.initArr[y_destination][x_destination]
            time.sleep(0.2)
            mapObj.displayMap()

    curses.flushinp()




def use_bow(command, playObj, mapObj, mapArr, fileNum):
    if not playObj.get_bow():
        # display 'no bow' message in menu
        return
    x_destination = playObj.x_pos
    y_destination = playObj.y_pos
    if command == curses.KEY_LEFT:
        if playObj.x_pos > 0:
            sign = -1
            x_destination = x_destination + sign
            while x_destination >= 0:
                checkBreak,x_destination,y_destination = arrowDirectionBow(mapObj, x_destination, y_destination, mapArr, fileNum, "b_l_atk", sign)
                if checkBreak == 0:
                    break

    if command == curses.KEY_RIGHT:
        if playObj.x_pos < mapObj.maxX - 1:
            sign = 1
            x_destination = x_destination + sign
            while x_destination <= mapObj.maxX - 1:
                checkBreak,x_destination,y_destination = arrowDirectionBow(mapObj, x_destination, y_destination, mapArr, fileNum, "b_r_atk", sign)
                if checkBreak == 0:
                    break

    if command == curses.KEY_UP:
        if playObj.y_pos < mapObj.maxY - 1:
            sign = -1
            y_destination = y_destination + sign
            while y_destination >= 0:
                checkBreak,x_destination,y_destination = arrowDirectionBow(mapObj, x_destination, y_destination, mapArr, fileNum, "b_u_atk", sign)
                if checkBreak == 0:
                    break

    if command == curses.KEY_DOWN:
        if playObj.y_pos > 0:
            sign = +1
            y_destination = y_destination + sign
            while y_destination <= mapObj.maxY - 1:
                checkBreak,x_destination,y_destination = arrowDirectionBow(mapObj, x_destination, y_destination, mapArr, fileNum, "b_d_atk", sign)
                if checkBreak == 0:
                    break
    curses.flushinp()




def use_shurikens(playObj, mapObj, mapArr, fileNum):
    if not playObj.get_shurikens():
        return
    x_destination = playObj.x_pos
    y_destination = playObj.y_pos

    if (x_destination - 1) >= 0 and (y_destination + 1) <= mapObj.maxY - 1:
        previous = checkAttackHitShurikens(mapObj, x_destination - 1, y_destination + 1, mapArr, fileNum)
    if (x_destination - 1) >= 0 and (y_destination - 1) >= 0:
        previous = checkAttackHitShurikens(mapObj, x_destination - 1, y_destination - 1, mapArr, fileNum)
    if (x_destination + 1) <= mapObj.maxX - 1 and (y_destination + 1) <= mapObj.maxY - 1:
        previous = checkAttackHitShurikens(mapObj, x_destination + 1, y_destination + 1, mapArr, fileNum)
    if (x_destination + 1) <= mapObj.maxX - 1 and (y_destination - 1) >= 0:
        previous = checkAttackHitShurikens(mapObj, x_destination + 1, y_destination - 1, mapArr, fileNum)

    mapObj.displayMap()

    if (x_destination - 1) >= 0 and (y_destination + 1) <= mapObj.maxY - 1:
        clearFieldShurikens(mapObj, x_destination - 1, y_destination + 1, previous)
    if (x_destination - 1) >= 0 and (y_destination - 1) >= 0:
        clearFieldShurikens(mapObj, x_destination - 1, y_destination - 1, previous)
    if (x_destination + 1) <= mapObj.maxX - 1 and (y_destination + 1) <= mapObj.maxY - 1:
        clearFieldShurikens(mapObj, x_destination + 1, y_destination + 1, previous)
    if (x_destination + 1) <= mapObj.maxX - 1 and (y_destination - 1) >= 0:
        clearFieldShurikens(mapObj, x_destination + 1, y_destination - 1, previous)

    time.sleep(0.2)
    mapObj.displayMap()
    curses.flushinp()


def game(command, playObj, mapObj, mapArr, fileNum):
    newMap = None
    if command == ord('w'):
        newMap = playObj.move('w', mapObj, fileNum)

    elif command == ord('a'):
        newMap = playObj.move('a', mapObj, fileNum)

    elif command == ord('s'):
        newMap = playObj.move('s', mapObj, fileNum)

    elif command == ord('d'):
        newMap = playObj.move('d', mapObj, fileNum)

    elif command == curses.KEY_LEFT or command == curses.KEY_RIGHT or command == curses.KEY_UP or command == curses.KEY_DOWN:
        equipped = playObj.get_equipped()
        if equipped == 'sword':
            use_sword(command, playObj, mapObj, mapArr, fileNum)
        elif equipped == 'bow':
            use_bow(command, playObj, mapObj, mapArr, fileNum)
        elif equipped == 'shurikens':
            use_shurikens(playObj, mapObj, mapArr, fileNum)

    elif command == ord('r'):
        mapObj.reset(playObj)

    elif command == ord('1'):
        playObj.swap_equipped('sword')

    elif command == ord('2'):
        if playObj.get_bow():
            playObj.swap_equipped('bow')

    elif command == ord('3'):
        if playObj.get_shurikens():
            playObj.swap_equipped('shurikens')

    mapObj.displayMap()
    # menuObj.display_menu(mapObj.maxX+2, playObj, mapObj)

    return newMap


def arrowDirectionBow(mapObj, x_destination, y_destination, mapArr, fileNum, direction, sign):

    if mapObj.objArr[y_destination][x_destination] == '-' or \
            (mapObj.objArr[y_destination][x_destination].isnumeric() and mapObj.exitArr[y_destination][x_destination] >= 0):
        previous = mapObj.objArr[y_destination][x_destination]
        mapObj.objArr[y_destination][x_destination] = direction
        mapObj.displayMap()
        mapObj.objArr[y_destination][x_destination] = previous
        mapObj.stdscr.refresh()
        time.sleep(0.1)
        mapObj.displayMap()
        if direction == 'b_l_atk' or direction == 'b_r_atk':
            x_destination = x_destination + sign
        else:
            y_destination = y_destination + sign

        return 1,x_destination,y_destination
    else:
        if mapObj.objArr[y_destination][x_destination].isnumeric() and mapObj.exitArr[y_destination][x_destination] < 0:
            enemyType = check_enemy_type(x_destination, y_destination, mapArr, fileNum)
            if enemyType == 2:
                kill_enemy(x_destination, y_destination, mapArr, fileNum, enemyType)
                mapObj.objArr[y_destination][x_destination] = direction
                mapObj.displayMap()
                mapObj.objArr[y_destination][x_destination] = '-'
                mapObj.stdscr.refresh()
                time.sleep(0.1)
                mapObj.displayMap()
            return 0,x_destination,y_destination
    return 0,x_destination,y_destination

def checkAttackHitShurikens(mapObj, x_destination, y_destination, mapArr, fileNum):
    enemyType = check_enemy_type(x_destination , y_destination , mapArr, fileNum)
    if mapObj.objArr[y_destination][x_destination] == '-' or \
            (mapObj.objArr[y_destination][x_destination].isnumeric() and mapObj.exitArr[y_destination][x_destination] >= 0) or \
            (mapObj.objArr[y_destination][x_destination].isnumeric() and mapObj.exitArr[y_destination][x_destination] < 0 and enemyType == 3):
        kill_enemy(x_destination, y_destination , mapArr, fileNum, enemyType)
        previous_bl = mapObj.objArr[y_destination][x_destination]
        mapObj.objArr[y_destination][x_destination] = 'sh_atk'
        return previous_bl


def clearFieldShurikens(mapObj, x_destination, y_destination, previous):
    if mapObj.objArr[y_destination][x_destination] == 'sh_atk':
        if mapObj.exitArr[y_destination][x_destination] < 0:
            mapObj.objArr[y_destination][x_destination] = '-'
        else:
            mapObj.objArr[y_destination][x_destination] = previous
    curses.flushinp()
