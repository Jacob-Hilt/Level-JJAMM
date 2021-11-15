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
    return [atoi(c) for c in re.split(r'(\d+)', text)]


def check_enemy_type(xPos, yPos, mapArr, fileNum):
    for enemy in mapArr[fileNum].enemyArr:
        if enemy.xpos == xPos and enemy.ypos == yPos:
            return enemy.typ
    return -1


def kill_enemy(xPos, yPos, mapArr, fileNum, enemyType):
    for enemy in mapArr[fileNum].enemyArr:
        if enemy.xpos == xPos and enemy.ypos == yPos and enemy.typ == enemyType:
            enemy.dead()


def use_sword(c, playObj, mapObj, mapArr, fileNum):
    if not playObj.get_sword():
        # display 'no sword' message in menu
        return
    xDes = playObj.x_pos
    yDes = playObj.y_pos
    if c == curses.KEY_LEFT:
        if playObj.x_pos > 0:
            xDes -= 1
    if c == curses.KEY_RIGHT:
        if playObj.x_pos < mapObj.maxX - 1:
            xDes += 1
    if c == curses.KEY_UP:
        if playObj.y_pos < mapObj.maxY - 1:
            yDes -= 1
    if c == curses.KEY_DOWN:
        if playObj.y_pos > 0:
            yDes += 1

    if xDes >= mapObj.maxX or xDes < 0 or yDes >= mapObj.maxY or yDes < 0:
        return
    enemyTyp = check_enemy_type(xDes, yDes, mapArr, fileNum)
    if (mapObj.objArr[yDes][xDes].isnumeric() and mapObj.exitArr[yDes][xDes] >= 0) or \
            mapObj.objArr[yDes][xDes] == '-' or \
            (mapObj.objArr[yDes][xDes].isnumeric() and mapObj.exitArr[yDes][xDes] < 0 and enemyTyp == 1):
        previous = mapObj.objArr[yDes][xDes]
        mapObj.objArr[yDes][xDes] = 's'
        mapObj.displayMap()
        kill_enemy(xDes, yDes, mapArr, fileNum, enemyTyp)
        if previous == '-' or \
                (previous.isnumeric() and mapObj.exitArr[yDes][xDes] < 0 and check_enemy_type(xDes, yDes, mapArr, fileNum) == 1):
            mapObj.objArr[yDes][xDes] = '-'
            time.sleep(0.2)
            mapObj.displayMap()
        elif previous.isnumeric() and mapObj.exitArr[yDes][xDes] >= 0:
            mapObj.objArr[yDes][xDes] = mapObj.initArr[yDes][xDes]
            time.sleep(0.2)
            mapObj.displayMap()

    curses.flushinp()


def use_bow(c, playObj, mapObj, mapArr, fileNum):
    if not playObj.get_bow():
        # display 'no bow' message in menu
        return
    xDes = playObj.x_pos
    yDes = playObj.y_pos
    if c == curses.KEY_LEFT:
        if playObj.x_pos > 0:
            xDes -= 1
            while xDes >= 0:
                if mapObj.objArr[yDes][xDes] == '-' or \
                        (mapObj.objArr[yDes][xDes].isnumeric() and mapObj.exitArr[yDes][xDes] >= 0):
                    previous = mapObj.objArr[yDes][xDes]
                    mapObj.objArr[yDes][xDes] = 'b_l_atk'
                    mapObj.displayMap()
                    mapObj.objArr[yDes][xDes] = previous
                    mapObj.stdscr.refresh()
                    time.sleep(0.1)
                    mapObj.displayMap()
                    xDes -= 1
                else:
                    if mapObj.objArr[yDes][xDes].isnumeric() and mapObj.exitArr[yDes][xDes] < 0:
                        enemyType = check_enemy_type(xDes, yDes, mapArr, fileNum)
                        if enemyType == 2:
                            kill_enemy(xDes, yDes, mapArr, fileNum, enemyType)
                            mapObj.objArr[yDes][xDes] = 'b_l_atk'
                            mapObj.displayMap()
                            mapObj.objArr[yDes][xDes] = '-'
                            mapObj.stdscr.refresh()
                            time.sleep(0.1)
                            mapObj.displayMap()
                    break

    if c == curses.KEY_RIGHT:
        if playObj.x_pos < mapObj.maxX - 1:
            xDes += 1
            while xDes <= mapObj.maxX - 1:
                if mapObj.objArr[yDes][xDes] == '-' or \
                        (mapObj.objArr[yDes][xDes].isnumeric() and mapObj.exitArr[yDes][xDes] >= 0):
                    previous = mapObj.objArr[yDes][xDes]
                    mapObj.objArr[yDes][xDes] = 'b_r_atk'
                    mapObj.displayMap()
                    mapObj.objArr[yDes][xDes] = previous
                    mapObj.stdscr.refresh()
                    time.sleep(0.1)
                    mapObj.displayMap()
                    xDes += 1
                else:
                    if mapObj.objArr[yDes][xDes].isnumeric() and mapObj.exitArr[yDes][xDes] < 0:
                        enemyType = check_enemy_type(xDes, yDes, mapArr, fileNum)
                        if enemyType == 2:
                            kill_enemy(xDes, yDes, mapArr, fileNum, enemyType)
                            mapObj.objArr[yDes][xDes] = 'b_r_atk'
                            mapObj.displayMap()
                            mapObj.objArr[yDes][xDes] = '-'
                            mapObj.stdscr.refresh()
                            time.sleep(0.1)
                            mapObj.displayMap()
                    break

    if c == curses.KEY_UP:
        if playObj.y_pos < mapObj.maxY - 1:
            yDes -= 1
            while yDes >= 0:
                if mapObj.objArr[yDes][xDes] == '-' or \
                        (mapObj.objArr[yDes][xDes].isnumeric() and mapObj.exitArr[yDes][xDes] >= 0):
                    previous = mapObj.objArr[yDes][xDes]
                    mapObj.objArr[yDes][xDes] = 'b_u_atk'
                    mapObj.displayMap()
                    mapObj.objArr[yDes][xDes] = previous
                    mapObj.stdscr.refresh()
                    time.sleep(0.1)
                    mapObj.displayMap()
                    yDes -= 1
                else:
                    if mapObj.objArr[yDes][xDes].isnumeric() and mapObj.exitArr[yDes][xDes] < 0:
                        enemyType = check_enemy_type(xDes, yDes, mapArr, fileNum)
                        if enemyType == 2:
                            kill_enemy(xDes, yDes, mapArr, fileNum, enemyType)
                            mapObj.objArr[yDes][xDes] = 'b_u_atk'
                            mapObj.displayMap()
                            mapObj.objArr[yDes][xDes] = '-'
                            mapObj.stdscr.refresh()
                            time.sleep(0.1)
                            mapObj.displayMap()
                    break

    if c == curses.KEY_DOWN:
        if playObj.y_pos > 0:
            yDes += 1
            while yDes <= mapObj.maxY - 1:
                if mapObj.objArr[yDes][xDes] == '-' or \
                        (mapObj.objArr[yDes][xDes].isnumeric() and mapObj.exitArr[yDes][xDes] >= 0):
                    previous = mapObj.objArr[yDes][xDes]
                    mapObj.objArr[yDes][xDes] = 'b_d_atk'
                    mapObj.displayMap()
                    mapObj.objArr[yDes][xDes] = previous
                    mapObj.stdscr.refresh()
                    time.sleep(0.1)
                    mapObj.displayMap()
                    yDes += 1
                else:
                    if mapObj.objArr[yDes][xDes].isnumeric() and mapObj.exitArr[yDes][xDes] < 0:
                        enemyType = check_enemy_type(xDes, yDes, mapArr, fileNum)
                        if enemyType == 2:
                            kill_enemy(xDes, yDes, mapArr, fileNum, enemyType)
                            mapObj.objArr[yDes][xDes] = 'b_d_atk'
                            mapObj.displayMap()
                            mapObj.objArr[yDes][xDes] = '-'
                            mapObj.stdscr.refresh()
                            time.sleep(0.1)
                            mapObj.displayMap()
                    break
    curses.flushinp()


def use_shurikens(playObj, mapObj, mapArr, fileNum):
    if not playObj.get_shurikens():
        return
    xDes = playObj.x_pos
    yDes = playObj.y_pos

    if (xDes - 1) >= 0 and (yDes + 1) <= mapObj.maxY - 1:
        enemyType = check_enemy_type(xDes - 1, yDes + 1, mapArr, fileNum)
        if mapObj.objArr[yDes + 1][xDes - 1] == '-' or \
                (mapObj.objArr[yDes + 1][xDes - 1].isnumeric() and mapObj.exitArr[yDes + 1][xDes - 1] >= 0) or \
                (mapObj.objArr[yDes + 1][xDes - 1].isnumeric() and mapObj.exitArr[yDes + 1][xDes - 1] < 0 and enemyType == 3):
            kill_enemy(xDes - 1, yDes + 1, mapArr, fileNum, enemyType)
            previous_bl = mapObj.objArr[yDes + 1][xDes - 1]
            mapObj.objArr[yDes + 1][xDes - 1] = 'sh_atk'

    if (xDes - 1) >= 0 and (yDes - 1) >= 0:
        enemyType = check_enemy_type(xDes - 1, yDes - 1, mapArr, fileNum)
        if mapObj.objArr[yDes - 1][xDes - 1] == '-' or \
                (mapObj.objArr[yDes - 1][xDes - 1].isnumeric() and mapObj.exitArr[yDes - 1][xDes - 1] >= 0) or \
                (mapObj.objArr[yDes - 1][xDes - 1].isnumeric() and mapObj.exitArr[yDes - 1][xDes - 1] < 0 and enemyType == 3):
            kill_enemy(xDes - 1, yDes - 1, mapArr, fileNum, enemyType)
            previous_ul = mapObj.objArr[yDes - 1][xDes - 1]
            mapObj.objArr[yDes - 1][xDes - 1] = 'sh_atk'

    if (xDes + 1) <= mapObj.maxX - 1 and (yDes + 1) <= mapObj.maxY - 1:
        enemyType = check_enemy_type(xDes + 1, yDes + 1, mapArr, fileNum)
        if mapObj.objArr[yDes + 1][xDes + 1] == '-' or \
                (mapObj.objArr[yDes + 1][xDes + 1].isnumeric() and mapObj.exitArr[yDes + 1][xDes + 1] >= 0) or \
                (mapObj.objArr[yDes + 1][xDes + 1].isnumeric() and mapObj.exitArr[yDes + 1][xDes + 1] < 0 and enemyType == 3):
            kill_enemy(xDes + 1, yDes + 1, mapArr, fileNum, enemyType)
            previous_br = mapObj.objArr[yDes + 1][xDes + 1]
            mapObj.objArr[yDes + 1][xDes + 1] = 'sh_atk'

    if (xDes + 1) <= mapObj.maxX - 1 and (yDes - 1) >= 0:
        enemyType = check_enemy_type(xDes + 1, yDes - 1, mapArr, fileNum)
        if mapObj.objArr[yDes - 1][xDes + 1] == '-' or \
                (mapObj.objArr[yDes - 1][xDes + 1].isnumeric() and mapObj.exitArr[yDes - 1][xDes + 1] >= 0) or \
                (mapObj.objArr[yDes - 1][xDes + 1].isnumeric() and mapObj.exitArr[yDes - 1][xDes + 1] < 0 and enemyType == 3):
            kill_enemy(xDes + 1, yDes - 1, mapArr, fileNum, enemyType)
            previous_ur = mapObj.objArr[yDes - 1][xDes + 1]
            mapObj.objArr[yDes - 1][xDes + 1] = 'sh_atk'

    mapObj.displayMap()

    if (xDes - 1) >= 0 and (yDes + 1) <= mapObj.maxY - 1:
        if mapObj.objArr[yDes + 1][xDes - 1] == 'sh_atk':
            if mapObj.exitArr[yDes + 1][xDes - 1] < 0:
                mapObj.objArr[yDes + 1][xDes - 1] = '-'
            else:
                mapObj.objArr[yDes + 1][xDes - 1] = previous_bl

    if (xDes - 1) >= 0 and (yDes - 1) >= 0:
        if mapObj.objArr[yDes - 1][xDes - 1] == 'sh_atk':
            if mapObj.exitArr[yDes - 1][xDes - 1] < 0:
                mapObj.objArr[yDes - 1][xDes - 1] = '-'
            else:
                mapObj.objArr[yDes - 1][xDes - 1] = previous_ul

    if (xDes + 1) <= mapObj.maxX - 1 and (yDes + 1) <= mapObj.maxY - 1:
        if mapObj.objArr[yDes + 1][xDes + 1] == 'sh_atk':
            if mapObj.exitArr[yDes + 1][xDes + 1] < 0:
                mapObj.objArr[yDes + 1][xDes + 1] = '-'
            else:
                mapObj.objArr[yDes + 1][xDes + 1] = previous_br

    if (xDes + 1) <= mapObj.maxX - 1 and (yDes - 1) >= 0:
        if mapObj.objArr[yDes - 1][xDes + 1] == 'sh_atk':
            if mapObj.exitArr[yDes - 1][xDes + 1] < 0:
                mapObj.objArr[yDes - 1][xDes + 1] = '-'
            else:
                mapObj.objArr[yDes - 1][xDes + 1] = previous_ur

    time.sleep(0.2)
    mapObj.displayMap()
    curses.flushinp()


def game(c, playObj, mapObj, mapArr, fileNum):
    newMap = None
    if c == ord('w'):
        newMap = playObj.move('w', mapObj, fileNum)

    elif c == ord('a'):
        newMap = playObj.move('a', mapObj, fileNum)

    elif c == ord('s'):
        newMap = playObj.move('s', mapObj, fileNum)

    elif c == ord('d'):
        newMap = playObj.move('d', mapObj, fileNum)

    elif c == curses.KEY_LEFT or c == curses.KEY_RIGHT or c == curses.KEY_UP or c == curses.KEY_DOWN:
        equipped = playObj.get_equipped()
        if equipped == 'sword':
            use_sword(c, playObj, mapObj, mapArr, fileNum)
        elif equipped == 'bow':
            use_bow(c, playObj, mapObj, mapArr, fileNum)
        elif equipped == 'shurikens':
            use_shurikens(playObj, mapObj, mapArr, fileNum)

    elif c == ord('r'):
        mapObj.reset(playObj)

    elif c == ord('1'):
        playObj.swap_equipped('sword')

    elif c == ord('2'):
        if playObj.get_bow():
            playObj.swap_equipped('bow')

    elif c == ord('3'):
        if playObj.get_shurikens():
            playObj.swap_equipped('shurikens')

    mapObj.displayMap()
    # menuObj.display_menu(mapObj.maxX+2, playObj, mapObj)

    return newMap

