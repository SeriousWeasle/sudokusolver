import curses

stdscr = curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

stdscr.clear()
curses.cbreak()
curses.noecho()

stdscr.addstr(10, 3, "Hello world!", curses.color_pair(1))
stdscr.addstr(10, 5, "yeet", curses.color_pair(2))
stdscr.getkey()
curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
stdscr.addstr(11, 5, "yeet", curses.color_pair(2))

stdscr.refresh()
stdscr.getkey()

curses.nocbreak()
curses.echo()
curses.endwin()