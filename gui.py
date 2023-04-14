# References:
# https://www.pygame.org/project/3096/5107
# http://inventwithpython.com/pygame/chapter4.html

from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "True"

import pygame
from pygame.locals import *
from thread import ThreadWithReturn

# Local Dependencies
from puzzle import *

# create constants
TILE_SIZE = 80
FPS = 30
BLANK = None
MIN_WINDOW_WIDTH = 640
MIN_WINDOW_HEIGHT = 480
BASIC_FONT_SIZE = 20
TILE_SLIDE_SPEED = 8
BORDER_WIDTH = 4

# In-Game Messages
MSG_INSTRUCTIONS = "Click tiles next to empty space or press arrow keys to slide tiles."
MSG_SEARCHING = "Finding Solution (this may take a while)"
MSG_SOLVED = "Solved! (Esc to close)"
MSG_SOLVING = "Solving the game board"

# Color dictionary (R    G    B  )
COLORS = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "gold": (200, 180, 0),
    "brown": (100, 50, 0)
}

# set colors
BG_COLOR = COLORS["brown"]
TILE_COLOR = COLORS["gold"]
TEXT_COLOR = COLORS["white"]
BORDER_COLOR = COLORS["black"]
BUTTON_COLOR = COLORS["white"]
BUTTON_TEXT_COLOR = COLORS["black"]
MESSAGE_COLOR = COLORS["white"]

KEY_MAP = {
    K_LEFT: LEFT, K_a: LEFT,
    K_RIGHT: RIGHT, K_d: RIGHT,
    K_UP: UP, K_w: UP,
    K_DOWN: DOWN, K_s: DOWN
}


class GraphicsEngine:

    def __init__(self, puzzle: Puzzle):
        pygame.init()

        self.board_width = self.board_height = puzzle.board_size
        self.window_width = max(160 * puzzle.board_size, MIN_WINDOW_WIDTH)
        self.window_height = max(120 * puzzle.board_size, MIN_WINDOW_HEIGHT)
        self.display = pygame.display.set_mode((self.window_width, self.window_height))
        self.x_margin = (self.window_width - TILE_SIZE * self.board_width) // 2
        self.y_margin = (self.window_height - TILE_SIZE * self.board_height) // 2
        self.basic_font = pygame.font.Font("freesansbold.ttf", BASIC_FONT_SIZE)
        self.fps_clock = pygame.time.Clock()
        self.puzzle = puzzle
        self.top_message = None
        self.THREAD_solve = None

        pygame.display.set_caption(f"{self.board_width ** 2 - 1} Puzzle")
        self.display.fill(BG_COLOR)
        self.draw_message(MSG_INSTRUCTIONS)
        self.draw_board(puzzle.board)
        solve_surface, solve_rect = \
            self.make_text("Solve", TEXT_COLOR, TILE_COLOR, self.window_width - 120, self.window_height - 30)
        self.display.blit(solve_surface, solve_rect)

        self.solve_rect = solve_rect

    # creates gui where puzzle is a Puzzle class variable
    def gui(self):
        # main loop where user can move tiles
        while True:
            if self.THREAD_solve is not None and not self.THREAD_solve.is_alive():
                solved_puzzle = self.THREAD_solve.join()
                self.solve_animation(solved_puzzle)
                self.puzzle.set_board(solved_puzzle.board)
                self.THREAD_solve = None
                self.draw_message(MSG_SOLVED)

            # if user wants to move a tile
            if slide_to := self.event_handler():
                if not self.puzzle.is_valid_move(slide_to):
                    continue

                # show tile slide
                self.slide_animation(slide_to, TILE_SLIDE_SPEED)
                self.puzzle.set_board(self.puzzle.move(slide_to))

                if self.puzzle.is_solution():
                    self.draw_message(MSG_SOLVED)
                elif self.THREAD_solve is None:
                    self.draw_message(MSG_INSTRUCTIONS)

            pygame.display.flip()
            self.fps_clock.tick(FPS)

    def event_handler(self):
        slide_to = None

        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()
            # if user clicked in the window, get cords of spot clicked
            elif event.type == MOUSEBUTTONUP:  # if user used mouse
                spot_x, spot_y = self.get_spot_clicked(event.pos[0], event.pos[1])

                if (spot_x, spot_y) == (None, None):  # check if user clicked an option button
                    if self.solve_rect.collidepoint(event.pos) and self.THREAD_solve is None:
                        self.THREAD_solve = ThreadWithReturn(target=solve_puzzle, args=(self.puzzle,))
                        self.THREAD_solve.start()
                        self.draw_message(MSG_SEARCHING)

                else:  # user clicked on a tile
                    # check if the clicked tile was next to blank spot
                    blank_y, blank_x = self.puzzle.blank_pos
                    if spot_x == blank_x + 1 and spot_y == blank_y:
                        slide_to = LEFT
                    elif spot_x == blank_x - 1 and spot_y == blank_y:
                        slide_to = RIGHT
                    elif spot_x == blank_x and spot_y == blank_y + 1:
                        slide_to = UP
                    elif spot_x == blank_x and spot_y == blank_y - 1:
                        slide_to = DOWN

            elif event.type == KEYUP:  # user used keyboard
                if event.key == K_ESCAPE:
                    terminate()  # terminate if user activates Esc key

                slide_to = KEY_MAP.get(event.key)

        return slide_to

    # function displays tile slide animation, does not check if move is valid
    def slide_animation(self, move: int, speed: int):
        blank_y, blank_x = self.puzzle.blank_pos

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
        else:
            raise ValueError

        # prepare base surface
        base_surf = self.display.copy()

        # display blank space over the moving tile on base_surf surface
        move_left, move_top = self.get_left_top(move_x, move_y)
        pygame.draw.rect(base_surf, BG_COLOR, (move_left, move_top, TILE_SIZE, TILE_SIZE))

        # animate tile slide
        for i in range(speed, TILE_SIZE, speed):
            self.display.blit(base_surf, (0, 0))
            if move == UP:
                self.draw_tile(move_x, move_y, self.puzzle.board[move_y][move_x], 0, -i)
            elif move == DOWN:
                self.draw_tile(move_x, move_y, self.puzzle.board[move_y][move_x], 0, i)
            elif move == LEFT:
                self.draw_tile(move_x, move_y, self.puzzle.board[move_y][move_x], -i, 0)
            elif move == RIGHT:
                self.draw_tile(move_x, move_y, self.puzzle.board[move_y][move_x], i, 0)

            pygame.display.flip()
            self.fps_clock.tick(FPS)

        self.display.blit(base_surf, (0, 0))
        self.draw_tile(blank_x, blank_y, self.puzzle.board[move_y][move_x])
        pygame.display.flip()

    # function draws board in window
    def draw_board(self, board: list):
        left = self.x_margin
        top = self.y_margin
        width = self.board_width * TILE_SIZE
        height = self.board_height * TILE_SIZE
        border_offset = 2 * BORDER_WIDTH + self.board_width - 1
        border_rect = (left - BORDER_WIDTH - 1, top - BORDER_WIDTH - 1, width + border_offset, height + border_offset)

        pygame.draw.rect(self.display, BG_COLOR, (left, top, width + self.board_width, height + self.board_height))
        pygame.draw.rect(self.display, BORDER_COLOR, border_rect, BORDER_WIDTH)

        for x in range(self.board_height):
            for y in range(self.board_width):
                if board[y][x]:
                    self.draw_tile(x, y, board[y][x])

    # function finds x and y board coordinates from x and y pixel coordinates
    def get_spot_clicked(self, x: int, y: int):
        for tile_y in range(self.board_height):
            for tile_x in range(self.board_width):
                left, top = self.get_left_top(tile_x, tile_y)
                tile_rect = pygame.Rect(left, top, TILE_SIZE, TILE_SIZE)
                if tile_rect.collidepoint(x, y):
                    return tile_x, tile_y
        return None, None

    # function gets left and top position of tile
    def get_left_top(self, x: int, y: int):
        left = self.x_margin + (x * TILE_SIZE) + (x - 1)
        top = self.y_margin + (y * TILE_SIZE) + (y - 1)
        return left, top

    # function draws a tile at the given coordinates
    def draw_tile(self, x: int, y: int, num: int, adj_x: int = 0, adj_y: int = 0):
        left, top = self.get_left_top(x, y)

        pygame.draw.rect(self.display, TILE_COLOR, (left + adj_x, top + adj_y, TILE_SIZE, TILE_SIZE))
        text_surf = self.basic_font.render(str(num), True, TEXT_COLOR)
        text_rect = text_surf.get_rect()
        text_rect.center = left + TILE_SIZE // 2 + adj_x, top + TILE_SIZE // 2 + adj_y
        self.display.blit(text_surf, text_rect)

    def draw_message(self, msg: str):
        if self.top_message is not None:
            pygame.draw.rect(self.display, BG_COLOR, self.top_message)

        text_surf, text_rect = self.make_text(msg, MESSAGE_COLOR, BG_COLOR, 5, 5)
        self.display.blit(text_surf, text_rect)
        self.top_message = text_rect

    # function creates text objects for Surface and Rectangle
    def make_text(self, text: str, color: tuple, bg_color: tuple, top: int, left: int):
        text_surf = self.basic_font.render(text, True, color, bg_color)
        text_rect = text_surf.get_rect()
        text_rect.topleft = (top, left)
        return text_surf, text_rect

    def solve_animation(self, node: Puzzle):
        path = [node]

        while node.parent:
            node = node.parent
            path.append(node)

        self.draw_message(MSG_SOLVING)

        for i in range(len(path) - 1, -1, -1):
            self.draw_board(path[i].board)
            pygame.display.flip()
            self.fps_clock.tick(FPS)
            quit_check()


# function terminates gui
def terminate():
    pygame.quit()
    exit('\nProgram Quit... Good Bye!')

# function checks if user selected the quit button
def quit_check():
    # get all QUIT events
    if pygame.event.get(QUIT):
        terminate()
        return True

    for event in pygame.event.get(KEYUP):  # get all KEYUP events
        if event.key == K_ESCAPE:
            terminate()  # terminate if user activates Esc key
            return True
        pygame.event.post(event)  # put other KEYUP event objects back

    return False
