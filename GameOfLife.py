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


def sqare(s:str):
    BASE = ["     ",
        "  y  ",]
    l = s.split("x")
    for i in range(0, (int(l[0])-1)):
        BASE.append("_____")
        BASE.append("     ")
        BASE.append("  y  ")
    BASE.append("     ")
    #print(BASE)
    #%
    new = []
    for i in range(0, (int(l[1]) -1 )):
        c = 2
        l2 = len(BASE)
        for string in BASE:
            #print(string)
            
            if l2 == 1:
                new.append(string + "|     ")
                continue
            elif c == 0:
                new.append(string + "|  y  ")
                c += 1
            elif c == 1:
                new.append(string + "|_____")
                c += 1
            elif c == 2:
                new.append(string + "|     ")
                c = 0
            l2-=1
        #print(new)
        #time.sleep(2)
        
        del BASE
        BASE = new
        new = []
        
    return BASE



firstcycle = True

LEVEL_MAP = sqare(input("How big? (XxY):"))
selector_x = 0
selector_y = 0
y_min = 0
y_max = 0
y_step = 0
x_min = 0
x_max = 0
x_step = 0
cells = []
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
    for i in MAP[1]:
        if i == "y":
            coords.append([])
    for i in range(len(MAP)):
            for j in range(len(MAP[i])):
                obj = MAP[i][j]
                if not obj == "y":
                    curses.attron(curses.COLOR_PAIR(1))
                    curses.mvaddstr(i, j, obj)
                    curses.attroff(curses.COLOR_PAIR(1))
                else:
                    if [i, j] in cells and c == [i, j]:
                        curses.attron(curses.COLOR_PAIR(3))
                        curses.mvaddstr(i, j, "?")
                        curses.attroff(curses.COLOR_PAIR(3))
                    elif [i, j] in cells:
                        curses.attron(curses.COLOR_PAIR(4))
                        curses.mvaddstr(i, j, "#")
                        curses.attroff(curses.COLOR_PAIR(4))
                    elif c == [i, j]:
                        #print("tru")
                        curses.attron(curses.COLOR_PAIR(2))
                        curses.mvaddstr(i, j, "?")
                        curses.attroff(curses.COLOR_PAIR(2))
                    else:
                        curses.attron(curses.COLOR_PAIR(1))
                        curses.mvaddstr(i, j, " ")
                        curses.attroff(curses.COLOR_PAIR(1))
                    coords[a].append([i, j])
                    if not a == (len(coords)-1):
                        a += 1
                    else:
                        a = 0
                        
def render_game_map_no_cursor():
    # render the map
    global coords, firstcycle
    if not firstcycle:
        c = getcoords()
    else:
        c = [1, 2]
        firstcycle = False
    a = 0
    coords = []
    for i in MAP[1]:
        if i == "y":
            coords.append([])
    for i in range(len(MAP)):
            for j in range(len(MAP[i])):
                obj = MAP[i][j]
                if not obj == "y":
                    curses.attron(curses.COLOR_PAIR(1))
                    curses.mvaddstr(i, j, obj)
                    curses.attroff(curses.COLOR_PAIR(1))
                else:
                    
                    if [i, j] in cells:
                        curses.attron(curses.COLOR_PAIR(4))
                        curses.mvaddstr(i, j, "#")
                        curses.attroff(curses.COLOR_PAIR(4))
                    else:
                        curses.attron(curses.COLOR_PAIR(1))
                        curses.mvaddstr(i, j, " ")
                        curses.attroff(curses.COLOR_PAIR(1))
                    coords[a].append([i, j])
                    if not a == (len(coords)-1):
                        a += 1
                    else:
                        a = 0
            #print(coords)
def status():
    curses.attron(curses.COLOR_PAIR(1))
    curses.mvaddstr((len(MAP)+5), 0, "WASD for movement, e to place in selected field, f to choose a number, q to quit.")
    curses.attroff(curses.COLOR_PAIR(1))

def getnum():
    curses.attron(curses.COLOR_PAIR(1))
    curses.mvaddstr((len(MAP)+6), 0, "Please enter a value. E to Proceed")
    curses.attroff(curses.COLOR_PAIR(1))
    curses.move((len(MAP)+7), 5)
    done = False
    string = ""
    while not done:
        k = curses.getch()
        #print(k)
        if k == curses.CCHAR("e"):
            done = True
        try:
            key = int(chr(k))
        except ValueError:
            continue
        string += str(key)
        curses.move((len(MAP)+7), 3)
        curses.addstr((string + "                       "))
    try:
        return int(string)
    except ValueError as err:
        curses.endwin()
        raise ValueError(err)
        

def check_coords(x, y):
    if x == -1:
        x = (len(coords[0])-1)
    elif x == len(coords):
        x = 0
    if y == -1:
        y = (len(coords)-1)
    elif y == len(coords):
        y = 0
    return coords[x][y]
    ...
def get_neighbours(x, y):
    count = 0
    #try:
    
    for i in range((y - 1), (y + 2)):
        
        if check_coords(x-1, i) in cells:
            count +=1
                    

    for i in range((y - 1), (y + 2)):
            #print("i:",i)

        if check_coords(x+1, i) in cells:
            count +=1
    #except IndexError:
        #print(sx)
        #exit()
    
    if check_coords(x, y-1) in cells:
        count += 1
    
    if check_coords(x, y+1) in cells:
        count+=1
    #print(count)
    return count
    ...      
def simulate(num):
    global cells
    #print(cells)
    done = False
    end="cycles"
    for i in range(0, num):
        newcells = []
        oldcells = []
        if len(cells) == 0:
            end = "cells"
            break
        else:
            n = 1
            for x in range(0, len(coords)):
                for y in range(0, len(coords)):
                    neighbours=get_neighbours(x, y)
                    if coords[x][y] in cells:
                        #print("cell " , n)
                        #print([x, y])
                        #n +=1
                        if neighbours == 2 or neighbours == 3:
                            newcells.append(coords[x][y])
                    else:
                        if neighbours == 3:
                            newcells.append(coords[x][y])
        if cells == newcells:
            end = "static"
            break
        #elif oldcells == newcells:
            #end = "semi"
            #break
        oldcells = cells
        cells = newcells
        curses.clear()
        render_game_map_no_cursor()
        curses.attron(curses.COLOR_PAIR(1))
        curses.mvaddstr((len(MAP)+ 5), 0, f"Cycle {i} of {num} ({num - i} left)")
        curses.attroff(curses.COLOR_PAIR(1))
        curses.refresh()
        sleep(0.01)
                    
                        
                        
    curses.attron(curses.COLOR_PAIR(1))
    if end == "cycles":
        curses.mvaddstr((len(MAP)+ 5), 0, "Simulation ended, no cycles left (Press any key to continue)")
    elif end == "cells":
        curses.mvaddstr((len(MAP)+ 5), 0, "Simulation ended, no cells left (Press any key to continue)")
    elif end == "static":
        curses.mvaddstr((len(MAP)+ 5), 0, "Simulation ended, cells became static (Press any key to continue)")
    elif end == "semi":
        curses.mvaddstr((len(MAP)+ 5), 0, "Simulation ended, cells became semi-static (Press any key to continue)")
    curses.attroff(curses.COLOR_PAIR(1))
    curses.getch()
                        
                
    ...

def getcoords():
    global selector_x, selector_y, coords
    return coords[selector_x][selector_y]

def main():
    global selector_y, selector_x, X, O, end
    load_level_map()
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    curses.start_color()
    curses.keypad(stdscr, True)
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_YELLOW)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)
    end = False
    cycle = 0
    while not end:
        curses.clear()
        render_game_map()
        status()
        curses.refresh()

        k = curses.getch()

        if k == curses.CCHAR("d"):
            if selector_x != (len(coords)-1):
                selector_x += 1
        elif k == curses.CCHAR("a"):
            if selector_x != 0:
                selector_x -= 1
        elif k == curses.CCHAR("s"):
            if selector_y != (len(coords[0])-1):
                selector_y += 1
        elif k == curses.CCHAR("w"):
            if selector_y != 0:
                selector_y -= 1
        elif k == curses.CCHAR("q"):
            end = True
        elif k == curses.CCHAR("e"):
            if not coords[selector_x][selector_y] in cells:
                cells.append(coords[selector_x][selector_y])
            else:
                cells.remove(coords[selector_x][selector_y])
        elif k == curses.CCHAR("f"):
            num = getnum()
            simulate(num)
                

    curses.clear()
    curses.refresh()
    curses.endwin()
        
if __name__ == "__main__":
    
    main()
    
