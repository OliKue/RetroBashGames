import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint
import random


FIELD_SIZE = [30,60]
X_MID = FIELD_SIZE[1] / 2
Y_MID = FIELD_SIZE[0] / 2

def main():
    curses.initscr()
    curses.start_color()
    win = curses.newwin(FIELD_SIZE[0], FIELD_SIZE[1], 0, 0)
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
            GAME_STATE = "tetris" if key == ord('2') else GAME_STATE
            GAME_STATE = "exit" if key == ord('3') else GAME_STATE

        if GAME_STATE == "menu":
            win.border(0)
            win.addstr(2, 2, '1. Snake')
            win.addstr(4, 2, '2. Tetris')
            win.addstr(6, 2, '3. Exit')
        
        if GAME_STATE == "snake":
            win.clear()
            runSnake(win)
            win.clear()
            GAME_STATE = "menu"
        
        if GAME_STATE == "tetris":
            win.clear()
            runTetris(win)
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
        win.addstr(FIELD_SIZE[0] - 1, 2, 'Score : ' + str(score) + ' ')
        win.addstr(0, (FIELD_SIZE[1] // 2) - 3, ' SNAKE ')
        win.timeout(150 - (len(snake) // 5 + len(snake) // 10)%120)

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
        if snake[0][0] == FIELD_SIZE[0] - 1: snake[0][0] = 1
        if snake[0][1] == FIELD_SIZE[1] - 1: snake[0][1] = 1

        if snake[0] in snake[1:]: break

        if snake[0] == food:
            food = []
            score += 1
            while food == []:
                food = [randint(1, FIELD_SIZE[0] - 2), randint(1, FIELD_SIZE[1] - 2)]
                if food in snake: food = []
            win.addch(food[0], food[1], '*', curses.color_pair(1))
        else:
            last = snake.pop()
            win.addch(last[0], last[1], ' ')
        win.addch(snake[0][0], snake[0][1], '#', curses.color_pair(2))

def runTetris(win):
    score = 0
    legalKeys = [KEY_LEFT, KEY_RIGHT, KEY_DOWN, ord(' '), 27] # 27 is escape
    key = None

    # Tetris board dimensions
    HEIGHT, WIDTH = 28, 16

    # Tetromino shapes (represented as lists of (row, column) offsets)
    SHAPES = [
        [(0, 0), (0, 1), (1, 0), (1, 1)],  # Square
        [(0, 0), (0, 1), (0, 2), (0, 3)],  # Line
        [(0, 0), (0, 1), (0, 2), (1, 2)],  # L-shape
        [(0, 0), (0, 1), (0, 2), (1, 0)],  # Reverse L-shape
        [(0, 0), (0, 1), (1, 1), (1, 2)],  # S-shape
        [(0, 0), (1, 0), (1, 1), (2, 1)],  # Reverse S-shape
    ]

    # draw border
    def draw_boader(win):
        for y in range(HEIGHT+1):
            win.addch(y, 0, '|')
            win.addch(y, WIDTH + 1, '|')
            
        for x in range(WIDTH):
            win.addch(HEIGHT, x + 1, '=')
        win.refresh()
        
    def draw_score():
        nonlocal score
        win.addstr(10, WIDTH + 5, 'Score : ' + str(score) + ' ')

    def draw_board(win, board):
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if board[y][x] == '#':
                    win.addch(y, x + 1, '#')
        win.refresh()

    def clear_board(win):
        for y in range(HEIGHT):
            for x in range(WIDTH):
                win.addch(y, x + 1, ' ')
        win.refresh()

    def rotate(shape):
        return [(x, -y) for (y, x) in shape]

    def clear_rows(board):
        for y in range(0, HEIGHT):
            if all(board[y][x] == '#' for x in range(WIDTH)):
                nonlocal score
                score = score + 1
                draw_score()
                del board[y]
                board.insert(0,[' ' for _ in range(WIDTH+1)])

    draw_boader(win)
    draw_score()

    board = [[' ' for _ in range(WIDTH+1)] for _ in range(HEIGHT+1)]
    current_shape = random.choice(SHAPES)
    yD = 0
    xD = WIDTH // 2

    gameLost = False
    while (key != 27 and not gameLost):
        win.timeout(250 - (score // 5 + score // 10)%120)
        # user input
        key = None
        event = win.getch()
        if event in legalKeys:
            key = event
        if key == ord(' '):
            current_shape = rotate(current_shape)

        # xD and yD update
        newXD = xD + (1 if key == KEY_RIGHT else -1 if key == KEY_LEFT else 0)
        newYD = yD + 1

        # update falling pice
        # check if shape + xD on wall / in board
            # if allowed update to new X delta
        if all(x + newXD < WIDTH and x + newXD >= 0 and board[y + newYD][x + xD] == ' ' for  y,x in current_shape):
           xD = newXD
        # check if shape + yD on floor / in board
            # if allowed update to new Y delta
        if all(y + newYD < HEIGHT and board[y + newYD][x + xD] == ' ' for y, x in current_shape):
           yD = newYD
        # Lock the shape in place
        # if on floor add to board, calculate board update, add new pice, reset deltas
        else:
            for y, x in current_shape:
                board[y + yD][x + xD] = '#'
            yD = 0
            xD = WIDTH // 2
            current_shape = random.choice(SHAPES)
        
        # lose condition
        if(board[0][WIDTH // 2] == '#'):
            gameLost = True

        # draw current field
        clear_board(win)
        clear_rows(board)
        draw_board(win, board)
        for y, x in current_shape:
            win.addch(y + yD, x + xD + 1, '#')

if __name__ == '__main__':
    main()
