from os import system
import pkg_resources
from time import sleep
try:
    dist = pkg_resources.get_distribution("uni-curses")
except pkg_resources.DistributionNotFound:
    print("checking for py-launcher...")
    result = system("py -m pip")
    if result == 0:
        system("py -m pip install uni-curses")
    print(result)
    result = system("python -m pip install uni-curses")
    if result == 0:
        print("Successfully installed dependencies! Please restart the program!")
    else:
        print("Something went wrong when trying to install dependencies!")
    exit()
import unicurses as curses

firstcycle = True

LEVEL_MAP =[
        "     |     |     ",
        "  y  |  y  |  y  ",
        "_____|_____|_____",
        "     |     |     ",
        "  y  |  y  |  y  ",
        "_____|_____|_____",
        "     |     |     ",
        "  y  |  y  |  y  ",
        "     |     |     "
     ]
selector_x = 0
selector_y = 0
y_min = 0
y_max = 0
y_step = 0
x_min = 0
x_max = 0
x_step = 0
X = []
O = []
Xs = []
Os = []
player = False
end = False
def load_level_map():
    global MAP
    MAP = []
    for i in range(len(LEVEL_MAP)):
        MAP.append( [] )
        for j in range(len(LEVEL_MAP[i])):
            MAP[i].append(LEVEL_MAP[i][j])
def render_game_map():
    # render the map
    global coords, firstcycle
    if not firstcycle:
        c = getcoords()
    else:
        c = [1, 2]
        firstcycle = False
    a = 0
    coords = []
    coords.append([])
    coords.append([])
    coords.append([])
    for i in range(len(MAP)):
            for j in range(len(MAP[i])):
                obj = MAP[i][j]
                if not obj == "y":
                    curses.attron(curses.COLOR_PAIR(1))
                    curses.mvaddstr(i, j, obj)
                    curses.attroff(curses.COLOR_PAIR(1))
                else:
                    if [i, j] in O and c[0] == i and c[1] == j:
                        curses.attron(curses.COLOR_PAIR(4))
                        curses.mvaddstr(i, j, "O")
                        curses.attroff(curses.COLOR_PAIR(4))
                    elif [i, j] in X and c[0] == i and c[1] == j:
                        curses.attron(curses.COLOR_PAIR(3))
                        curses.mvaddstr(i, j, "X")
                        curses.attroff(curses.COLOR_PAIR(3))
                    elif [i, j] in O:
                        curses.attron(curses.COLOR_PAIR(5))
                        curses.mvaddstr(i, j, "O")
                        curses.attroff(curses.COLOR_PAIR(5))
                    elif [i, j] in X:
                        curses.attron(curses.COLOR_PAIR(6))
                        curses.mvaddstr(i, j, "X")
                        curses.attroff(curses.COLOR_PAIR(6))
                    elif c[0] == i and c[1] == j:
                        #print("tru")
                        curses.attron(curses.COLOR_PAIR(2))
                        curses.mvaddstr(i, j, "?")
                        curses.attroff(curses.COLOR_PAIR(2))
                    else:
                        curses.attron(curses.COLOR_PAIR(1))
                        curses.mvaddstr(i, j, " ")
                        curses.attroff(curses.COLOR_PAIR(1))
                    coords[a].append([i, j])
                    if not a == 2:
                        a += 1
                    else:
                        a = 0
            #print(coords)
def status():
    global player
    curses.attron(curses.COLOR_PAIR(1))
    curses.mvaddstr(11, 5, f"Player {int(player) + 1}")
    curses.mvaddstr(13, 0, "WASD for movement, e to place in selected field, q to quit.")
    curses.attroff(curses.COLOR_PAIR(1))
      
def checkwin():
    global X, O, end
    Xs = X
    Os = O
    for i in range(2, 14, 6):
        if [1, i] in Xs and [4, i] in Xs and [7, i] in Xs:
            end = True
            print("Player 1 Won!")
        elif [1, i] in Os and [4, i] in Os and [7, i] in Os:
            end = True
            print("Player 2 Won!")
    for i in range(1, 7, 3):
        if [i, 2] in Xs and [i, 8] in Xs and [i, 14] in Xs:
            end = True
            print("Player 1 Won!")
        elif [i, 2] in Os and [i, 8] in Os and [i, 14] in Os:
            end = True
            print("Player 2 Won!")
    if [1, 2] in Xs and [4, 8] in Xs and [7, 14] in Xs or [7, 2] in Xs and [4, 8] in Xs and [1, 14] in Xs:
        end = True
        print("Player 1 Won!")
    if [1, 2] in Os and [4, 8] in Os and [7, 14] in Os or [7, 2] in Os and [4, 8] in Os and [1, 14] in Os:
        end = True
        print("Player 2 Won!")

def getcoords():
    global selector_x, selector_y, coords
    return coords[selector_x][selector_y]

def main():
    global selector_y, selector_x, player, X, O, end
    load_level_map()
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    curses.start_color()
    curses.keypad(stdscr, True)
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_YELLOW)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_YELLOW)
    curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)
    end = False
    cycle = 0
    while not end:
        curses.clear()
        render_game_map()
        status()
        curses.refresh()
        k = curses.getch()
        if k == curses.CCHAR("d"):
            if selector_x != 2:
                selector_x += 1
        elif k == curses.CCHAR("a"):
            if selector_x != 0:
                selector_x -= 1
        elif k == curses.CCHAR("s"):
            if selector_y != 2:
                selector_y += 1
        elif k == curses.CCHAR("w"):
            if selector_y != 0:
                selector_y -= 1
        elif k == curses.CCHAR("q"):
            end = True
        elif k == curses.CCHAR("e"):
            if player:
                if not coords[selector_x][selector_y] in O:
                    X.append(coords[selector_x][selector_y])
                    player = not player
                    cycle +=1
                    if cycle == 9:
                        X = []
                        O = []
                        cycle = 0
            else:
                if not coords[selector_x][selector_y] in X:
                    O.append(coords[selector_x][selector_y])
                    player = not player
                    cycle +=1
                    if cycle == 9:
                        X = []
                        O = []
                        cycle = 0
        #simplify()
        checkwin()
    curses.clear()
    curses.refresh()
    curses.endwin()
        
if __name__ == "__main__":
    main()
    
