import curses


def end_screen(stdscr, playObj, menuObj):
    time = menuObj.get_time()
    deaths = playObj.deaths
    stdscr.erase()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)
    pad = curses.newpad(curses.LINES - 1, curses.COLS - 1)
    titlePadX = curses.COLS // 4
    titlePadY = curses.LINES // 5
    midY = curses.LINES // 2
    midX = curses.COLS // 2
    title = curses.newpad(titlePadY, titlePadX)
    title.nodelay(False)

    # read jjamm welcome screen from eternal file
    with open("visuals/jjamm.txt") as textFile:
        jjamm = [list(map(int, line.split(','))) for line in textFile]

    for i in range(len(jjamm)):
        for j in range(len(jjamm[i])):
            if jjamm[i][j]:
                pad.addch(i + 2, j + 2, 'T', curses.color_pair(1))

    # read gameOver welcome screen from eternal file
    with open("visuals/gameOver.txt") as textFile:
        gameOver = [list(map(int, line.split(','))) for line in textFile]

    for i in range(len(gameOver)):
        for j in range(len(gameOver[i])):
            if gameOver[i][j]:
                pad.addch(i + 15, j + 25, 'T', curses.color_pair(3))

    pad.addstr(midY, midX, 'Total deaths: %s' % deaths, curses.color_pair(2))
    pad.addstr(midY + 1, midX, 'Total keys collected: %s' % playObj.key, curses.color_pair(2))
    pad.addstr(midY + 2, midX, 'Total time to complete levels: %s' % time, curses.color_pair(2))
    pad.addstr(midY + 3, midX, 'Press any key to exit', curses.color_pair(2))

    pad.box()
    pad.refresh(0, 0, 0, 0, curses.LINES - 2, curses.COLS - 2)
    pad.nodelay(False)
    pad.getch()
    pad.clear()
    curses.nocbreak()
    curses.echo()
    curses.endwin()
