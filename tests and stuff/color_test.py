import curses, math

def main(stdscr):
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, min(255, curses.COLORS)):
        curses.init_pair(i + 1, i, -1)
        try:
            for i in range(0, 256):
                x = (i % 16) * 4
                y = math.floor(i / 16)
                stdscr.addstr(y, x, str(i).rjust(4), curses.color_pair(i))
        except curses.ERR:
            pass
    stdscr.getch()

curses.wrapper(main)