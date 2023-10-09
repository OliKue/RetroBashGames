import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint

def main():
    curses.initscr()
    curses.start_color()
    win = curses.newwin(20, 60, 0, 0)
    win.keypad(1)
    curses.noecho()
    curses.curs_set(0)
    curses.cbreak()
    win.border(0)
    win.nodelay(1)

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    GAME_STATE = "menu"

    while GAME_STATE != "exit":

        event = win.getch()
        key = None if event == -1 else event

        if key != None:
            GAME_STATE = "snake" if key == ord('1') else GAME_STATE
            GAME_STATE = "exit" if key == ord('2') else GAME_STATE

        if GAME_STATE == "menu":
            win.border(0)
            win.addstr(2, 2, '1. Snake')
            win.addstr(4, 2, '2. Exit')
        
        if GAME_STATE == "snake":
            win.clear()
            runSnake(win)
            win.clear()
            GAME_STATE = "menu"

    curses.endwin()

def runSnake(win):
    legalKeys = [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27] # 27 is escape
    illegalDirection = {KEY_LEFT: KEY_RIGHT, KEY_RIGHT: KEY_LEFT, KEY_UP: KEY_DOWN, KEY_DOWN: KEY_UP}

    key = KEY_RIGHT
    score = 0

    snake = [[4,10], [4,9], [4,8]]
    food = [10,20]

    win.addch(food[0], food[1], '*', curses.color_pair(1))

    while key != 27:
        win.border(0)
        win.addstr(19, 2, 'Score : ' + str(score) + ' ')
        win.addstr(0, 27, ' SNAKE ')
        win.timeout(150 - (len(snake)/5 + len(snake)/10)%120)

        prevKey = key
        event = win.getch()
        key = key if event == -1 else event

        if key not in legalKeys or key == illegalDirection.get(prevKey):
            key = prevKey

        yD = 1 if key == KEY_DOWN else -1 if key == KEY_UP else 0
        xD = 1 if key == KEY_RIGHT else -1 if key == KEY_LEFT else 0
        snake.insert(0, [snake[0][0] + yD, snake[0][1] + xD])

        if snake[0][0] == 0: snake[0][0] = 18
        if snake[0][1] == 0: snake[0][1] = 58
        if snake[0][0] == 19: snake[0][0] = 1
        if snake[0][1] == 59: snake[0][1] = 1

        if snake[0] in snake[1:]: break

        if snake[0] == food:
            food = []
            score += 1
            while food == []:
                food = [randint(1, 18), randint(1, 58)]
                if food in snake: food = []
            win.addch(food[0], food[1], '*', curses.color_pair(1))
        else:
            last = snake.pop()
            win.addch(last[0], last[1], ' ')
        win.addch(snake[0][0], snake[0][1], '#', curses.color_pair(2))


if __name__ == '__main__':
    main()
