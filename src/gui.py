# References:
# https://www.pygame.org/project/3096/5107
# http://inventwithpython.com/pygame/chapter4.html
from __future__ import annotations

# Do this before importing pygame to prevent the support prompt from being printed to the terminal
from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "True"

import pygame as pg
from pygame.locals import *

# Local Dependencies
from src.button import Button
from src.puzzle import *
from src.thread import ThreadWithReturn

# Constants
FPS = 60                            # Target FPS for the game
WINDOW_WIDTH = 1600                 # Width of the game window [pixels]
WINDOW_HEIGHT = 900                 # Height of the game window [pixels]
SAFE_WIDTH = 150                    # Min space required between sides of the window and the game board [pixels]
SAFE_HEIGHT = 75                    # Min space required between top/bottom of the window and the game board [pixels]
GAME_FONT = "freesansbold.ttf"      # Font style used for in-game text
BASIC_FONT_SIZE = 20                # Size of the font used for text not on tiles [pixels]
TILE_FONT_RATIO = 4                 # Font used on tiles will be this many times smaller than the tile itself
TILE_SPEED_RATIO = 10               # Speed the tile will move at when animated (smaller numbers = faster slide)
BORDER_WIDTH = 4                    # Width of the border surrounding the game board
BUTTON_SIZE = (150, 75)             # Size of the in-game menu buttons [pixels]
BUTTON_SPACING = 25                 # Space between the in-game menu buttons [pixels]
TOP_MESSAGE_OFFSET = (5, 5)         # Offset between the top message and the top-left corner of the screen [pixels]
TOTAL_MOVES_OFFSET = (5, 30)        # Offset between moves counter and the top-left corner of the screen [pixels]


# In-Game Messages
MSG_INSTRUCTIONS = "Click tiles next to empty space or press arrow keys to slide tiles."
MSG_SEARCHING = "Finding Solution (this may take a while)"
MSG_SOLVED = "Solved! (Esc to close)"
MSG_SOLVING = "Solving the game board"

# Color mapping (R, G, B)
COLORS = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "gold": (200, 180, 0),
    "brown": (100, 50, 0)
}

# Color constants
BG_COLOR = COLORS["brown"]              # Color of the background
TILE_COLOR = COLORS["gold"]             # Color of the game tiles
TEXT_COLOR = COLORS["white"]            # Color of in-game text
BORDER_COLOR = COLORS["black"]          # Color of the border surrounding the game board
BUTTON_COLOR = COLORS["white"]          # Color of the menu buttons
BUTTON_TEXT_COLOR = COLORS["black"]     # Color of the menu button text

# Mapping of key-press to expected direction of tile movement
KEY_MAP = {
    K_LEFT: LEFT, K_a: LEFT,
    K_RIGHT: RIGHT, K_d: RIGHT,
    K_UP: UP, K_w: UP,
    K_DOWN: DOWN, K_s: DOWN
}


# Holds all attributes and methods needed to run the GUI
# attr          display - Surface object of the entire screen
# attr        fps_clock - Clock object used to help game run at desired FPS
# attr       board_size - length/width of the game board
# attr        tile_size - size of the sliding game tiles
# attr tile_slide_speed - number of pixels the tiles will slide each frame when animating their movement
# attr         x_margin - space between the sides of the screen and the game board in pixels
# attr         y_margin - space between the top/bottom of the screen and the game board in pixels
# attr        tile_font - Font object used to render the font on top of the sliding tiles
# attr       basic_font - Font object used to render text not on the tiles
# attr           puzzle - Puzzle object used to hold the the puzzle information
# attr    initial_board - 2D array representing the initial state of the game board before any input movements
# attr      top_message - Rect object that is the size of the currently displayed message at the top of the screen
# attr     move_counter - Rect object that is the size of the "number of moves" counter
# attr      total_moves - number of moves used since the initial board state
# attr     THREAD_solve - Thread object used to solve the puzzle concurrently
# attr          buttons - array of Button objects representing the in-game menu buttons
class GraphicsEngine:

    # param puzzle - Puzzle object holding the initial board state
    def __init__(self, puzzle: Puzzle):
        pg.init()

        self.display = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.fps_clock = pg.time.Clock()
        self.board_size = puzzle.board_size
        self.tile_size = (min(WINDOW_WIDTH - 150, WINDOW_HEIGHT - 75) - self.board_size + 1) // self.board_size
        self.tile_slide_speed = self.tile_size // TILE_SPEED_RATIO
        self.x_margin = (WINDOW_WIDTH - self.tile_size * self.board_size) // 2
        self.y_margin = (WINDOW_HEIGHT - self.tile_size * self.board_size) // 2
        self.tile_font = pg.font.Font(GAME_FONT, self.tile_size // TILE_FONT_RATIO)
        self.basic_font = pg.font.Font(GAME_FONT, BASIC_FONT_SIZE)
        self.puzzle = puzzle
        self.initial_board = puzzle.board
        self.top_message = None
        self.move_counter = None
        self.total_moves = 0
        self.THREAD_solve = None
        self.buttons = []

        self.initialize_display()

    # Prepares the screen and draws the board in preparation for the call to self.launch_gui()
    def initialize_display(self):
        pg.display.set_caption(f"{self.board_size ** 2 - 1} Puzzle")
        pg.display.set_icon(pg.image.load("icon.png"))

        # Draw starting condition of the game
        self.display.fill(BG_COLOR)
        self.draw_message(MSG_INSTRUCTIONS)
        self.draw_move_count()
        self.draw_board(self.puzzle.board)
        self.draw_buttons()

    # Draws the in-game menu buttons onto the screen
    def draw_buttons(self):
        button_names = ("Solve", "Reset", "New Board")
        button_funcs = (self.find_solution, self.reset_puzzle, self.new_puzzle)

        left_edge = WINDOW_WIDTH - (self.x_margin + BUTTON_SIZE[0]) // 2
        top_edge = self.y_margin

        # Create and draw a Button object for each menu button
        for name, func in zip(button_names, button_funcs):
            button = Button(pg.Rect(left_edge, top_edge, *BUTTON_SIZE), BUTTON_COLOR, name, func)
            self.display.fill(button.color, button.rect)
            pg.display.update(button.rect)
            
            text = self.basic_font.render(button.text, True, BUTTON_TEXT_COLOR)
            self.display.blit(text, text.get_rect(center=button.rect.center))

            self.buttons.append(button)
            
            top_edge += BUTTON_SPACING + BUTTON_SIZE[1]

    # Called by the "Solve" button. Starts a new thread to solve the puzzle
    def find_solution(self):
        if self.THREAD_solve is not None or self.puzzle.is_solution():
            return

        self.THREAD_solve = ThreadWithReturn(target=solve_puzzle, args=(self.puzzle,))
        self.THREAD_solve.start()
        self.draw_message(MSG_SEARCHING)

    # Called by the "Reset" button. Resets the board back to its initial state
    def reset_puzzle(self):
        self.THREAD_solve = None
        self.puzzle.set_board(self.initial_board)
        self.draw_board(self.puzzle.board)
        self.total_moves = 0
        self.draw_move_count()
        self.draw_message(MSG_INSTRUCTIONS)

    # Called by the "New Board" button. Generates and draws a new puzzle
    def new_puzzle(self):
        self.THREAD_solve = None
        self.puzzle.generate()
        self.initial_board = self.puzzle.board
        self.draw_board(self.puzzle.board)
        self.total_moves = 0
        self.draw_move_count()
        self.draw_message(MSG_INSTRUCTIONS)

    # Main execution loop of the GUI
    def launch_gui(self):
        while True:
            # Check if a solving Thread has been created and completed execution
            if self.THREAD_solve is not None and not self.THREAD_solve.is_alive():
                solved_puzzle = self.THREAD_solve.join()
                self.solve_animation(solved_puzzle)
                self.puzzle.set_board(solved_puzzle.board)
                self.draw_message(MSG_SOLVED)
                self.THREAD_solve = None

            # Call the event handler and check if user wants to make a valid move
            if (slide_to := self.event_handler()) and self.puzzle.is_valid_move(slide_to):
                # Animate the tile slide and update our game board
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

    # Handles and clears the event queue
    # return slide_to - integer representing the direction the user wishes to move a tile
    # return     None - if user did not request a tile move
    def event_handler(self) -> int | None:
        slide_to = None

        # Look through each even in the queue
        for event in pg.event.get():
            if event.type == QUIT:
                terminate()

            elif event.type == MOUSEBUTTONUP:
                # Check if the user clicked any of the in-game menu buttons
                for button in self.buttons:
                    if button.rect.collidepoint(*event.pos):
                        button.press()
                        break
                else:
                    # If they didn't click a menu button, check if they clicked a sliding tile
                    if not (spot_clicked := self.get_spot_clicked(event.pos[0], event.pos[1])):
                        continue

                    spot_x, spot_y = spot_clicked
                    blank_y, blank_x = self.puzzle.blank_pos

                    # Check if the clicked tile was next to the board's blank spot
                    if spot_y == blank_y:
                        if spot_x == blank_x + 1:
                            slide_to = LEFT
                        if spot_x == blank_x - 1:
                            slide_to = RIGHT
                    elif spot_x == blank_x:
                        if spot_y == blank_y + 1:
                            slide_to = UP
                        if spot_y == blank_y - 1:
                            slide_to = DOWN

            # Else terminate the program if the user pressed Esc
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()

                slide_to = KEY_MAP.get(event.key)

        return slide_to

    # Animates a tile slide when the user requests a tile movement
    # param move - integer representing the direction the user wishes to move in
    def slide_animation(self, move: int):
        if move == UP:
            coord_mod = [0, -1]
        elif move == DOWN:
            coord_mod = [0, 1]
        elif move == LEFT:
            coord_mod = [-1, 0]
        elif move == RIGHT:
            coord_mod = [1, 0]
        else:
            raise ValueError

        blank_y, blank_x = self.puzzle.blank_pos
        move_x, move_y = blank_x - coord_mod[0], blank_y - coord_mod[1]

        # Prepare base surface used to erase tile as it is moving
        base_surf = self.display.copy()
        pg.draw.rect(base_surf, BG_COLOR, (*self.get_left_top(move_x, move_y), self.tile_size, self.tile_size))

        # Animate the tile slide
        for i in range(self.tile_slide_speed, self.tile_size, self.tile_slide_speed):
            self.display.blit(base_surf, (0, 0))
            self.draw_tile(move_x, move_y, self.puzzle.board[move_y][move_x], coord_mod[0] * i, coord_mod[1] * i)

            pg.display.flip()
            self.fps_clock.tick(FPS)

        self.display.blit(base_surf, (0, 0))
        self.draw_tile(blank_x, blank_y, self.puzzle.board[move_y][move_x])
        pg.display.flip()

    # Draws a game board to the window
    # param board - 2D array of integers representing the game board
    def draw_board(self, board: list):
        left = self.x_margin - 1
        top = self.y_margin - 1
        width = self.board_size * self.tile_size
        height = self.board_size * self.tile_size
        border_offset = 2 * BORDER_WIDTH + self.board_size
        border_rect = (left - BORDER_WIDTH, top - BORDER_WIDTH, width + border_offset, height + border_offset)

        pg.draw.rect(self.display, BG_COLOR, (left, top, width + self.board_size, height + self.board_size))
        pg.draw.rect(self.display, BORDER_COLOR, border_rect, BORDER_WIDTH)

        # Draw each tile in the board
        for x in range(self.board_size):
            for y in range(self.board_size):
                if board[y][x]:
                    self.draw_tile(x, y, board[y][x])

    # Converts x and y pixel coordinates to x and y grid coordinates
    #  param              x - horizontal coordinate of the screen
    #  param              y - vertical coordinate of the screen
    # return tile_x, tile_y - coordinate pair of the tile clicked
    # return           None - if the user did not click on a tile
    def get_spot_clicked(self, x: int, y: int) -> tuple[int, int] | None:
        # Check if the Rect of any tile collides with the spot clicked
        for tile_y in range(self.board_size):
            for tile_x in range(self.board_size):
                if pg.Rect(*self.get_left_top(tile_x, tile_y), self.tile_size, self.tile_size).collidepoint(x, y):
                    return tile_x, tile_y

        return None

    # Returns the left and top pixel coordinates of a tile
    # param x - horizontal grid coordinate of the tile
    # param y - vertical grid coordinate of the tile
    def get_left_top(self, x: int, y: int) -> tuple[int, int]:
        return self.x_margin + (x * self.tile_size) + (x - 1), self.y_margin + (y * self.tile_size) + (y - 1)

    # Draws a given tile onto the screen
    # param     x - horizontal grid coordinate of the tile
    # param     y - vertical grid coordinate of the tile
    # param   num - integer to display on top of the tile
    # param adj_x - number of pixels to offset the horizontal position of the tile
    # param adj_y - number of pixels to offset the vertical position of the tile
    def draw_tile(self, x: int, y: int, num: int, adj_x: int = 0, adj_y: int = 0):
        left, top = self.get_left_top(x, y)

        pg.draw.rect(self.display, TILE_COLOR, (left + adj_x, top + adj_y, self.tile_size, self.tile_size))
        text_surf = self.tile_font.render(str(num), True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=(left + self.tile_size // 2 + adj_x, top + self.tile_size // 2 + adj_y))

        self.display.blit(text_surf, text_rect)

    # Draws a given message at the top of the screen
    # param msg - string of text to display
    def draw_message(self, msg: str):
        if self.top_message is not None:
            pg.draw.rect(self.display, BG_COLOR, self.top_message)

        text_surf, text_rect = self.make_text(msg, TEXT_COLOR, BG_COLOR, *TOP_MESSAGE_OFFSET)
        self.display.blit(text_surf, text_rect)

        self.top_message = text_rect

    # Draw the "Total Moves" counter
    def draw_move_count(self):
        if self.move_counter is not None:
            pg.draw.rect(self.display, BG_COLOR, self.move_counter)

        message_str = f"Total Moves: {str(self.total_moves)}"
        text_surf, text_rect = self.make_text(message_str, TEXT_COLOR, BG_COLOR, *TOTAL_MOVES_OFFSET)
        self.display.blit(text_surf, text_rect)

        self.move_counter = text_rect

    # Creates Surface and Rect objects for a given string
    #  param                 text - string to render
    #  param                color - color to render the text with
    #  param             bg_color - color to fill the Rect behind the text with
    #  param                  top - top edge to render the text at
    #  param                 left - left edge to render the text at
    # return text_surf, text_rect - the Rendered Surface and Rect objects for the string
    def make_text(self, text: str, color: tuple, bg_color: tuple, top: int, left: int) -> tuple[pg.Surface, pg.Rect]:
        text_surf = self.basic_font.render(text, True, color, bg_color)
        text_rect = text_surf.get_rect()
        text_rect.topleft = (top, left)

        return text_surf, text_rect

    # Animates the solution path of a puzzle
    # param node - Puzzle object holding the solved puzzle
    def solve_animation(self, node: Puzzle):

        # Build the path from solution to initial board state
        path = [node]
        while node.parent:
            node = node.parent
            path.append(node)

        self.draw_message(MSG_SOLVING)

        # Draw each board in the solution path in reverse order
        for i in range(len(path) - 1, -1, -1):
            self.draw_board(path[i].board)
            self.total_moves += 1
            self.draw_move_count()
            pg.display.flip()
            self.fps_clock.tick(FPS)
            quit_check()


# Terminates the GUI
def terminate():
    pg.quit()
    exit('\nProgram Quit... Good Bye!')


# Checks if the user selected the quit button
# return  True - if the user requested to quit
# return False - if the user did not request to quit
def quit_check() -> bool:
    # get all QUIT events
    if pg.event.get(QUIT):
        terminate()
        return True

    # Look through all KEYUP events and check if user pressed the Esc key
    for event in pg.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
            return True
        # put other KEYUP event objects back into the queue
        pg.event.post(event)

    return False
