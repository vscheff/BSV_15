from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "True"

import pygame, sys, random
from pygame.locals import *

# Local Dependencies
from puzzle import UP, DOWN, LEFT, RIGHT, Puzzle
from minheap import MinHeap


# create constants
TILESIZE = 80
FPS = 30
BLANK = None
MIN_WINDOW_WIDTH = 640
MIN_WINDOW_HEIGHT = 480

#                 R    G    B
BLACK =         (  0,   0,   0)
WHITE =         (255, 255, 255)
GOLD =          (200, 180,   0)
BROWN =         (100,  50,   0)

# set colors
BGCOLOR = BROWN
TILECOLOR = GOLD
TEXTCOLOR = WHITE
BORDERCOLOR = BLACK
BASICFONTSIZE = 20

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE


# creates gui where puzzle is a Puzzle class variable
def gui(puzzle):
    global BOARDWIDTH, BOARDHEIGHT, WINDOWWIDTH, WINDOWHEIGHT, FPSCLOCK, XMARGIN, YMARGIN,\
           DISPLAYSURF, BASICFONT, SOLVE_SURF, SOLVE_RECT

    # set board and window size based on user given size (size x size puzzle)
    BOARDWIDTH = BOARDHEIGHT = puzzle.board_size
    WINDOWWIDTH = max(160 * BOARDWIDTH, MIN_WINDOW_WIDTH)
    WINDOWHEIGHT = max(120 * BOARDHEIGHT, MIN_WINDOW_HEIGHT)

    XMARGIN = (WINDOWWIDTH - TILESIZE * BOARDWIDTH) // 2
    YMARGIN = (WINDOWHEIGHT - TILESIZE * BOARDHEIGHT) // 2

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption(f"{BOARDWIDTH ** 2 - 1} Puzzle")
    BASICFONT = pygame.font.Font("freesansbold.ttf", BASICFONTSIZE)

    # create option button for solving
    SOLVE_SURF, SOLVE_RECT = make_text('Solve', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 30)

    get_starting_board(puzzle.board)
    starting_board = puzzle.board
   
    # Generate Solution Board
    k = 1
    solution_board = []
    for i in range(BOARDHEIGHT):
        solution_board.append([])
        for j in range(BOARDWIDTH):
            solution_board[i].append(k)
            k += 1
    solution_board[-1][-1] = 0

    # main loop where user can move tiles
    while True:
        slide_to = 4  # direction a tile should slide if there is one
        msg = "Click tiles next to empty space or press arrow keys to slide tiles."

        if puzzle.board == solution_board:
            msg = "Solved! (Esc to close)"

        draw_board(puzzle.board, msg)

        if quit_check():
            return
        for event in pygame.event.get():  # event handling loop
            # if user clicked in the window, get cords of spot clicked
            if event.type == MOUSEBUTTONUP:  # if user used mouse
                spot_x, spot_y = get_spot_clicked(puzzle.board, event.pos[0], event.pos[1])

                if (spot_x, spot_y) == (None, None):  # check if user clicked an option button
                    if SOLVE_RECT.collidepoint(event.pos):
                        draw_board(puzzle.board, "Solving (this might take a while)")
                        pygame.display.update()
                        FPSCLOCK.tick(FPS)
                        solved_puzzle = solve_puzzle(puzzle)
                        puzzle = Puzzle(solve_animation(solved_puzzle).board, BOARDHEIGHT, None)

                else:  # use clicked on a tile
                    # check if the clicked tile was next to blank spot
                    blank_y, blank_x = puzzle.find_blank_pos()
                    if spot_x == blank_x + 1 and spot_y == blank_y:
                        slide_to = LEFT
                    elif spot_x == blank_x - 1 and spot_y == blank_y:
                        slide_to = RIGHT
                    elif spot_x == blank_x and spot_y == blank_y + 1:
                        slide_to = UP
                    elif spot_x == blank_x and spot_y == blank_y - 1:
                        slide_to = DOWN

            elif event.type == KEYUP:  # user used keyboard
                # check if user entered a key to move a tile
                if event.key in (K_LEFT, K_a) and is_valid_move(puzzle, LEFT):
                    slide_to = LEFT
                elif event.key in (K_RIGHT, K_d) and is_valid_move(puzzle, RIGHT):
                    slide_to = RIGHT
                elif event.key in (K_UP, K_w) and is_valid_move(puzzle, UP):
                    slide_to = UP
                elif event.key in (K_DOWN, K_s) and is_valid_move(puzzle, DOWN):
                    slide_to = DOWN

        # if user wants to move a tile
        if slide_to != 4:
            # show tile slide
            slide_animation(puzzle, slide_to, "Click tiles next to empty space or press arrow keys to slide tiles.", 8)
            make_move(puzzle, slide_to)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


# function moves blank spot in given direction
def make_move(puzzle, move):
    blank_y, blank_x = puzzle.find_blank_pos()

    if move == UP:
        puzzle.board[blank_y][blank_x], puzzle.board[blank_y + 1][blank_x] = puzzle.board[blank_y + 1][blank_x], puzzle.board[blank_y][blank_x]
    elif move == DOWN:
        puzzle.board[blank_y][blank_x], puzzle.board[blank_y - 1][blank_x] = puzzle.board[blank_y - 1][blank_x], puzzle.board[blank_y][blank_x]
    elif move == LEFT:
        puzzle.board[blank_y][blank_x], puzzle.board[blank_y][blank_x + 1] = puzzle.board[blank_y][blank_x + 1], puzzle.board[blank_y][blank_x]
    elif move == RIGHT:
        puzzle.board[blank_y][blank_x], puzzle.board[blank_y][blank_x - 1] = puzzle.board[blank_y][blank_x - 1], puzzle.board[blank_y][blank_x]



# function terminates gui
def terminate():
    pygame.quit()


# function checks if user selected the quit button
def quit_check():
    for event in pygame.event.get(QUIT):  # get all QUIT events
        terminate()
        return True

    for event in pygame.event.get(KEYUP):  # get all KEYUP events
        if event.key == K_ESCAPE:
            terminate()  # terminate if user activates Esc key
            return True
        pygame.event.post(event)  # put other KEYUP event objects back

    return False


# function checks if user entered move is a valid move
def is_valid_move(puzzle, move):
    blank_y, blank_x = puzzle.find_blank_pos()
    return (move == UP and blank_y != len(puzzle.board) - 1) or \
           (move == DOWN and blank_y != 0) or \
           (move == LEFT and blank_x != len(puzzle.board[0]) - 1) or \
           (move == RIGHT and blank_x != 0)


# function creates starting board
def get_starting_board(board):
    draw_board(board, "")
    pygame.display.update()
    pygame.time.wait(500)  # pause 500 ms for effect

# function displays tile slide animation, does not check if move is valid
def slide_animation(puzzle, move, msg, speed):
    blank_y, blank_x = puzzle.find_blank_pos()

    if move == UP:
        move_x = blank_x
        move_y = blank_y + 1
    elif move == DOWN:
        move_x = blank_x
        move_y = blank_y - 1
    elif move == LEFT:
        move_x = blank_x + 1
        move_y = blank_y
    elif move == RIGHT:
        move_x = blank_x - 1
        move_y = blank_y

    # prepare base surface
    draw_board(puzzle.board, msg)
    base_surf = DISPLAYSURF.copy()

    # display blank space over the moving tile on base_surf surface
    move_left, move_top = get_left_top(move_x, move_y)
    pygame.draw.rect(base_surf, BGCOLOR, (move_left, move_top, TILESIZE, TILESIZE))

    # animate tile slide
    for i in range(0, TILESIZE, speed):
        quit_check()
        DISPLAYSURF.blit(base_surf, (0, 0))
        if move == UP:
            draw_tile(move_x, move_y, puzzle.board[move_y][move_x], 0, -i)
        if move == DOWN:
            draw_tile(move_x, move_y, puzzle.board[move_y][move_x], 0, i)
        if move == LEFT:
            draw_tile(move_x, move_y, puzzle.board[move_y][move_x], -i, 0)
        if move == RIGHT:
            draw_tile(move_x, move_y, puzzle.board[move_y][move_x], i, 0)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


# function draws board in window
def draw_board(board, message):
    DISPLAYSURF.fill(BGCOLOR)

    if message:
        text_surf, text_rect = make_text(message, MESSAGECOLOR, BGCOLOR, 5, 5)
        DISPLAYSURF.blit(text_surf, text_rect)

    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[y][x] and board[y][x] != 0:
                draw_tile(x, y, board[y][x])

    left = XMARGIN - 1
    top = YMARGIN - 1
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)

    DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)


# function finds x and y board coordinates from x and y pixel coordinates
def get_spot_clicked(board, x, y):
    for tile_y in range(len(board)):
        for tile_x in range(len(board[0])):
            left, top = get_left_top(tile_x, tile_y)
            tile_rect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tile_rect.collidepoint(x, y):
                return tile_x, tile_y
    return None, None


# function gets left and top position of tile
def get_left_top(x, y):
    left = XMARGIN + (x * TILESIZE) + (x - 1)
    top = YMARGIN + (y * TILESIZE) + (y - 1)
    return left, top

# function draws a tile at the given coordinates
def draw_tile(x, y, num, adj_x=0, adj_y=0):
    left, top = get_left_top(x, y)

    pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left + adj_x, top + adj_y, TILESIZE, TILESIZE))
    text_surf = BASICFONT.render(str(num), True, TEXTCOLOR)
    text_rect = text_surf.get_rect()
    text_rect.center = left + int(TILESIZE / 2) + adj_x, top + int(TILESIZE / 2) + adj_y
    DISPLAYSURF.blit(text_surf, text_rect)


# function creates text objects for Surface and Rectangle
def make_text(text, color, bgcolor, top, left):
    text_surf = BASICFONT.render(text, True, color, bgcolor)
    text_rect = text_surf.get_rect()
    text_rect.topleft = (top, left)
    return text_surf, text_rect


def solve_animation(node: Puzzle):
    path = [node]
    solution_node = None

    while node.parent:
        node = node.parent
        path.append(node)

    for i in range(len(path) - 1, -1, -1):
        if path[i].is_solution:
            solution_node = path[i]
        draw_board(path[i].board, "Solving (this might take a while)")
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        quit_check()

    return solution_node


def solve_puzzle(puzzle: Puzzle):
    live_nodes = MinHeap()
    live_nodes.insert(puzzle)
    checked_boards = {str(puzzle.board): True}

    while live_nodes:
        current_node = live_nodes.pop_root()

        if current_node.is_solution():
            return current_node

        for direction in UP, DOWN, LEFT, RIGHT:
            new_board = current_node.move(direction)
            if new_board and str(new_board) not in checked_boards:
                live_nodes.insert(Puzzle(new_board, puzzle.board_size, current_node))
                checked_boards[str(new_board)] = True

    print("\nNo solution found! Are you sure the puzzle was solvable?")
    return None
