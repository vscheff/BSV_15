# References:
# https://www.pygame.org/project/3096/5107
# http://inventwithpython.com/pygame/chapter4.html
from __future__ import annotations

from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "True"

import pygame as pg
from pygame.locals import *

# Local Dependencies
from src.button import Button
from src.puzzle import *
from src.thread import ThreadWithReturn

# create constants
FPS = 30
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900
BASIC_FONT_SIZE = 20
TILE_FONT_RATIO = 4
TILE_SPEED_RATIO = 10
BORDER_WIDTH = 4
GAME_FONT = "freesansbold.ttf"
BUTTON_SIZE = (150, 75)
BUTTON_SPACING = 25

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
        pg.init()

        self.board_width = self.board_height = puzzle.board_size
        self.display = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.safe_height = WINDOW_HEIGHT - 75
        self.safe_width = WINDOW_WIDTH - 150
        self.tile_size = (min(self.safe_width, self.safe_height) - self.board_width + 1) // self.board_width
        self.tile_slide_speed = self.tile_size // TILE_SPEED_RATIO
        self.x_margin = (WINDOW_WIDTH - self.tile_size * self.board_width) // 2
        self.y_margin = (WINDOW_HEIGHT - self.tile_size * self.board_height) // 2
        self.tile_font = pg.font.Font(GAME_FONT, self.tile_size // TILE_FONT_RATIO)
        self.basic_font = pg.font.Font(GAME_FONT, BASIC_FONT_SIZE)
        self.fps_clock = pg.time.Clock()
        self.puzzle = puzzle
        self.initial_board = puzzle.board
        self.top_message = None
        self.THREAD_solve = None
        self.move_counter = None
        self.total_moves = 0
        self.solve_rect = None
        self.buttons = []

        self.initialize_display()

    def initialize_display(self):
        pg.display.set_caption(f"{self.board_width ** 2 - 1} Puzzle")
        pg.display.set_icon(pg.image.load("icon.png"))
        self.display.fill(BG_COLOR)
        self.draw_message(MSG_INSTRUCTIONS)
        self.draw_move_count()
        self.draw_board(self.puzzle.board)

        self.draw_buttons()

    def draw_buttons(self):
        button_names = ("Solve", "Reset", "New Board")
        button_funcs = (self.find_solution, self.reset_puzzle, self.new_puzzle)

        left_edge = WINDOW_WIDTH - (self.x_margin + BUTTON_SIZE[0]) // 2
        top_edge = self.y_margin

        for name, func in zip(button_names, button_funcs):
            button = Button(pg.Rect(left_edge, top_edge, *BUTTON_SIZE), BUTTON_COLOR, name, func)
            self.display.fill(button.color, button.rect)
            pg.display.update(button.rect)
            
            text = self.basic_font.render(button.text, True, BUTTON_TEXT_COLOR)
            rect = text.get_rect(center=button.rect.center)
            self.display.blit(text, rect)
            self.buttons.append(button)
            
            top_edge += BUTTON_SPACING + BUTTON_SIZE[1]

    def find_solution(self):
        if self.THREAD_solve is not None or self.puzzle.is_solution():
            return

        self.THREAD_solve = ThreadWithReturn(target=solve_puzzle, args=(self.puzzle,))
        self.THREAD_solve.start()
        self.draw_message(MSG_SEARCHING)

    def reset_puzzle(self):
        self.THREAD_solve = None
        self.puzzle.set_board(self.initial_board)
        self.draw_board(self.puzzle.board)
        self.total_moves = 0
        self.draw_move_count()
        self.draw_message(MSG_INSTRUCTIONS)

    def new_puzzle(self):
        self.THREAD_solve = None
        self.puzzle.generate()
        self.initial_board = self.puzzle.board
        self.draw_board(self.puzzle.board)
        self.total_moves = 0
        self.draw_move_count()
        self.draw_message(MSG_INSTRUCTIONS)

    # creates gui where puzzle is a Puzzle class variable
    def launch_gui(self):
        # main loop where user can move tiles
        while True:
            if self.THREAD_solve is not None and not self.THREAD_solve.is_alive():
                solved_puzzle = self.THREAD_solve.join()
                self.solve_animation(solved_puzzle)
                self.puzzle.set_board(solved_puzzle.board)
                self.THREAD_solve = None
                self.draw_message(MSG_SOLVED)

            # if user wants to move a tile
            if (slide_to := self.event_handler()) and self.puzzle.is_valid_move(slide_to):
                # show tile slide
                self.slide_animation(slide_to)
                self.puzzle.set_board(self.puzzle.move(slide_to))

                if self.puzzle.is_solution():
                    self.draw_message(MSG_SOLVED)
                elif self.THREAD_solve is None:
                    self.draw_message(MSG_INSTRUCTIONS)

                self.total_moves += 1
                self.draw_move_count()

            pg.display.flip()
            self.fps_clock.tick(FPS)

    def event_handler(self) -> int | None:
        slide_to = None

        for event in pg.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()
            # if user clicked in the window, get cords of spot clicked
            elif event.type == MOUSEBUTTONUP:  # if user used mouse
                for button in self.buttons:
                    if button.rect.collidepoint(*event.pos):
                        button.press()
                        break
                else:  # user clicked on a tile
                    # check if the clicked tile was next to blank spot
                    if not (spot_clicked := self.get_spot_clicked(event.pos[0], event.pos[1])):
                        continue
                    spot_x, spot_y = spot_clicked
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
    def slide_animation(self, move: int):
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
        pg.draw.rect(base_surf, BG_COLOR, (move_left, move_top, self.tile_size, self.tile_size))

        # animate tile slide
        for i in range(self.tile_slide_speed, self.tile_size, self.tile_slide_speed):
            self.display.blit(base_surf, (0, 0))
            if move == UP:
                self.draw_tile(move_x, move_y, self.puzzle.board[move_y][move_x], 0, -i)
            elif move == DOWN:
                self.draw_tile(move_x, move_y, self.puzzle.board[move_y][move_x], 0, i)
            elif move == LEFT:
                self.draw_tile(move_x, move_y, self.puzzle.board[move_y][move_x], -i, 0)
            elif move == RIGHT:
                self.draw_tile(move_x, move_y, self.puzzle.board[move_y][move_x], i, 0)

            pg.display.flip()
            self.fps_clock.tick(FPS)

        self.display.blit(base_surf, (0, 0))
        self.draw_tile(blank_x, blank_y, self.puzzle.board[move_y][move_x])
        pg.display.flip()

    # function draws board in window
    def draw_board(self, board: list):
        left = self.x_margin
        top = self.y_margin
        width = self.board_width * self.tile_size
        height = self.board_height * self.tile_size
        border_offset = 2 * BORDER_WIDTH + self.board_width - 1
        border_rect = (left - BORDER_WIDTH - 1, top - BORDER_WIDTH - 1, width + border_offset, height + border_offset)

        pg.draw.rect(self.display, BG_COLOR, (left-1, top-1, width + self.board_width, height + self.board_height))
        pg.draw.rect(self.display, BORDER_COLOR, border_rect, BORDER_WIDTH)

        for x in range(self.board_height):
            for y in range(self.board_width):
                if board[y][x]:
                    self.draw_tile(x, y, board[y][x])

    # function finds x and y board coordinates from x and y pixel coordinates
    def get_spot_clicked(self, x: int, y: int) -> tuple[int, int]:
        for tile_y in range(self.board_height):
            for tile_x in range(self.board_width):
                left, top = self.get_left_top(tile_x, tile_y)
                tile_rect = pg.Rect(left, top, self.tile_size, self.tile_size)
                if tile_rect.collidepoint(x, y):
                    return tile_x, tile_y

    # function gets left and top position of tile
    def get_left_top(self, x: int, y: int) -> tuple[int, int]:
        left = self.x_margin + (x * self.tile_size) + (x - 1)
        top = self.y_margin + (y * self.tile_size) + (y - 1)
        return left, top

    # function draws a tile at the given coordinates
    def draw_tile(self, x: int, y: int, num: int, adj_x: int = 0, adj_y: int = 0):
        left, top = self.get_left_top(x, y)

        pg.draw.rect(self.display, TILE_COLOR, (left + adj_x, top + adj_y, self.tile_size, self.tile_size))
        text_surf = self.tile_font.render(str(num), True, TEXT_COLOR)
        text_rect = text_surf.get_rect()
        text_rect.center = left + self.tile_size // 2 + adj_x, top + self.tile_size // 2 + adj_y
        self.display.blit(text_surf, text_rect)

    def draw_message(self, msg: str):
        if self.top_message is not None:
            pg.draw.rect(self.display, BG_COLOR, self.top_message)

        text_surf, text_rect = self.make_text(msg, MESSAGE_COLOR, BG_COLOR, 5, 5)
        self.display.blit(text_surf, text_rect)
        self.top_message = text_rect

    def draw_move_count(self):
        if self.move_counter is not None:
            pg.draw.rect(self.display, BG_COLOR, self.move_counter)

        text_surf, text_rect = self.make_text(f"Total Moves: {str(self.total_moves)}", MESSAGE_COLOR, BG_COLOR, 5, 30)
        self.display.blit(text_surf, text_rect)
        self.move_counter = text_rect

    # function creates text objects for Surface and Rectangle
    def make_text(self, text: str, color: tuple, bg_color: tuple, top: int, left: int) -> tuple[pg.Surface, pg.Rect]:
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
            self.total_moves += 1
            self.draw_move_count()
            pg.display.flip()
            self.fps_clock.tick(FPS)
            quit_check()


# function terminates gui
def terminate():
    pg.quit()
    exit('\nProgram Quit... Good Bye!')


# function checks if user selected the quit button
def quit_check() -> bool:
    # get all QUIT events
    if pg.event.get(QUIT):
        terminate()
        return True

    for event in pg.event.get(KEYUP):  # get all KEYUP events
        if event.key == K_ESCAPE:
            terminate()  # terminate if user activates Esc key
            return True
        pg.event.post(event)  # put other KEYUP event objects back

    return False
