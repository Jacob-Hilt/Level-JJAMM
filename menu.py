#This file contains methods to display menu, timer and lives of the player all in a Menu class. The display
#is refreshed each time the player hits a key. Lives are lost or won through gameplay. 
#Joint effort by: Jerry Smedley, Jacob Hilt, Melissa Barnes, Mark Montes, Anthony Chin
#This work is made available under the "MIT License". Please see the file LICENSE in this distribution for license terms.

import curses, curses.panel
from curses import wrapper
import time

class Menu:
    #initializes time, death count and refresh count for menu
    def __init__(self):                             #holds level start time to calculate time for timer
            self.start_time = round(time.time(),2)
            self.current_deaths = 0
            self.refresh = 0
            curses.curs_set(0)
    
    #calls print border, stats and time, weapons, win condition and death message functions to display on menu
    def display_menu(self, begin_x, playObj, mapObj):                #Displays menu border, time and lives
            stdscr = curses.initscr()
            curses.start_color()
            curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
            curses.init_pair(10, curses.COLOR_WHITE, curses.COLOR_BLACK)
            curses.init_pair(11, curses.COLOR_RED, curses.COLOR_BLACK)
            begin_y = 3
            height = 5
            width = 70
            win = curses.newwin(height, width, begin_y, begin_x+2)
            deathNum = playObj.deaths
            stdscr.refresh();

	    #printboarder 
            self.print_border(stdscr, begin_y, begin_x)

	    #prints stats and time
            self.print_stats_and_time(stdscr, playObj, begin_y, begin_x)

            #print weapons in satchel  
            self.print_weapons(playObj, stdscr, begin_y, begin_x)

            #print win condition
            self.print_win_condition(mapObj, stdscr, begin_y, begin_x)

	    #print you died message
            self.print_death_message(deathNum, stdscr, begin_y, begin_x)
            
            pass

    #Helper function to return elapsed time for level
    def get_time():                 
            current_time = round(time.time(), 2)
            return round((current_time - self.start_time), 2)

    #Print border around menu window
    def print_border(self, stdscr, begin_y, begin_x):
            for i in range(0, 25):        #printing horizontal border
                    stdscr.addch(begin_y,begin_x+i, "*", curses.color_pair(9)) 
                    stdscr.addch(begin_y+14,begin_x+i, "*", curses.color_pair(9)) 
            for i in range(0, 15):        #printing vertical border
                    stdscr.addch(begin_y+i,begin_x, "*", curses.color_pair(9)) 
                    stdscr.addch(begin_y+i,begin_x+24, "*", curses.color_pair(9)) 

    #prints deaths, time and keys on menu
    def print_stats_and_time(self, stdscr, playObj, begin_y, begin_x):
            current_time = round(time.time(), 2)
            time_elapsed = "Time Elapsed: " + str(round((current_time - self.start_time), 2))
	    
            stdscr.addstr(begin_y+1, begin_x+1, 'Menu: ',curses.color_pair(10))   
            stdscr.addstr(begin_y+2, begin_x+1, 'Deaths: %s' %playObj.deaths, curses.color_pair(10))
            stdscr.addstr(begin_y+3, begin_x+1, time_elapsed, curses.color_pair(10))
            stdscr.addstr(begin_y+4, begin_x+1, 'keys: %s' %playObj.key, curses.color_pair(10))
            stdscr.addstr(begin_y+6, begin_x+1, "Satchel: ", curses.color_pair(10))
    
    #prints available weapons and *** which one is currently equipped on menu
    def print_weapons(self, playObj, stdscr, begin_y, begin_x): 
            if playObj.bow == True and playObj.sword == False and playObj.shurikens == False:
                    if playObj.equipped == 'bow':
                            stdscr.addstr(begin_y+8, begin_x+1, "***Bow***      ", curses.color_pair(10))
                    else:
                            stdscr.addstr(begin_y+8, begin_x+1, "Bow            ", curses.color_pair(10))
            if playObj.sword == True and playObj.bow == False and playObj.shurikens == False:
                    if playObj.equipped == 'sword':
                            stdscr.addstr(begin_y+7, begin_x+1, "***Sword***    ", curses.color_pair(10))
                    else:
                            stdscr.addstr(begin_y+7, begin_x+1, "Sword          ", curses.color_pair(10))
	    
            if playObj.sword == False and playObj.bow == False and playObj.shurikens == True:
                    if playObj.equipped == 'shurikens':
                            stdscr.addstr(begin_y+9, begin_x+1, "***Shurikens*** ", curses.color_pair(10))
                    else:
                            stdscr.addstr(begin_y+9, begin_x+1, "Shurikens       ", curses.color_pair(10))
	   
            if playObj.sword == True and playObj.bow == True and playObj.shurikens == False:
                    if playObj.equipped == 'sword':
                            stdscr.addstr(begin_y+7, begin_x+1, "***Sword***    ", curses.color_pair(10))
                            stdscr.addstr(begin_y+8, begin_x+1, "Bow            ", curses.color_pair(10))
                    else:
                            stdscr.addstr(begin_y+7, begin_x+1, "Sword          ", curses.color_pair(10))
                            stdscr.addstr(begin_y+8, begin_x+1, "***Bow***      ", curses.color_pair(10))

            if playObj.sword == True and playObj.bow == False  and playObj.shurikens == True:
                    if playObj.equipped == 'sword':
                            stdscr.addstr(begin_y+7, begin_x+1, "***Sword***    ", curses.color_pair(10))
                            stdscr.addstr(begin_y+9, begin_x+1, "Shurikens       ", curses.color_pair(10))
                    else:
                            stdscr.addstr(begin_y+7, begin_x+1, "Sword          ", curses.color_pair(10))
                            stdscr.addstr(begin_y+9, begin_x+1, "***Shurikens*** ", curses.color_pair(10))

            if playObj.sword == False and playObj.bow == True and playObj.shurikens == True:
                    if playObj.equipped == 'bow':
                            stdscr.addstr(begin_y+8, begin_x+1, "***Bow***      ", curses.color_pair(10))
                            stdscr.addstr(begin_y+9, begin_x+1, "Shurikens      ", curses.color_pair(10))
                    else:
                            stdscr.addstr(begin_y+8, begin_x+1, "Bow            ", curses.color_pair(10))
                            stdscr.addstr(begin_y+9, begin_x+1, "***Shurikens*** ", curses.color_pair(10))

            if playObj.sword == True and playObj.bow == True and playObj.shurikens == True:
                    if playObj.equipped == 'sword':
                            stdscr.addstr(begin_y+7, begin_x+1, "***Sword***    ", curses.color_pair(10))
                            stdscr.addstr(begin_y+8, begin_x+1, "Bow            ", curses.color_pair(10))
                            stdscr.addstr(begin_y+9, begin_x+1, "Shurikens      ", curses.color_pair(10))
                    if playObj.equipped == 'bow':
                            stdscr.addstr(begin_y+7, begin_x+1, "Sword          ", curses.color_pair(10))
                            stdscr.addstr(begin_y+8, begin_x+1, "***Bow***      ", curses.color_pair(10))
                            stdscr.addstr(begin_y+9, begin_x+1, "Shurikens      ", curses.color_pair(10))
                    if playObj.equipped == 'shurikens':
                            stdscr.addstr(begin_y+7, begin_x+1, "Sword          ", curses.color_pair(10))
                            stdscr.addstr(begin_y+8, begin_x+1, "Bow            ", curses.color_pair(10))
                            stdscr.addstr(begin_y+9, begin_x+1, "***Shurikens***", curses.color_pair(10))

    #prints win condition for each level on menu
    def print_win_condition(self, mapObj, stdscr, begin_y, begin_x):
            if mapObj.winCond == 'T':
                    stdscr.addstr(begin_y+11, begin_x+1, "Reach the exit!", curses.color_pair(10))
            if mapObj.winCond == 'E':
                    stdscr.addstr(begin_y+11, begin_x+1, "Kill all enemies!", curses.color_pair(10))
            if mapObj.winCond == 'K':
                    stdscr.addstr(begin_y+11, begin_x+1, "Grab the key!", curses.color_pair(10))
            if mapObj.winCond == 'S':
                    stdscr.addstr(begin_y+11, begin_x+1, "Grab the sword!", curses.color_pair(10))
            if mapObj.winCond == 'B':
                    stdscr.addstr(begin_y+11, begin_x+1, "Grab the bow!", curses.color_pair(10))

    #prints "You died" message if player dies, otherwise counts up to refresh and remove message on menu
    def print_death_message(self, deathNum, stdscr, begin_y, begin_x):
            if self.current_deaths < deathNum:
                    stdscr.addstr(begin_y+13, begin_x+1, "XXX You died!!! XXX", curses.color_pair(11))
                    self.current_deaths = deathNum
                    self.refresh = 0
            else:
	            self.refresh += 1  
            if self.refresh > 3: 
                    stdscr.addstr(begin_y+13, begin_x+1, "                   ", curses.color_pair(11))
                    self.refresh = 0
