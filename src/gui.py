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
from src.button import Button, TextBox
from src.puzzle import *
from src.thread import ThreadWithReturn

# Constants
FPS = 60                            # Target FPS for the game
WINDOW_WIDTH = 1600                 # Initial width of the game window [pixels]
WINDOW_HEIGHT = 900                 # Initial height of the game window [pixels]
SAFE_WIDTH = 275                    # Min space required between sides of the window and the game board [pixels]
SAFE_HEIGHT = 125                   # Min space required between top/bottom of the window and the game board [pixels]
GAME_FONT = "freesansbold.ttf"      # Font style used for in-game text
BASIC_FONT_RATIO = 4                # Font used for in-game text will be this many times smaller than menu buttons
TILE_FONT_RATIO = 4                 # Font used on tiles will be this many times smaller than the tile itself
TILE_SPEED_RATIO = 10               # Speed the tile will move at when animated (smaller numbers = faster slide)
BUTTON_SIZE_RATIO = (8, 11)         # In-game menu buttons will be this many times smaller than the screen
TEXTBOX_SIZE_RATIO = (12, 14)       # In-game text boxes will be this many times smaller than the screen
BUTTON_SPACING_RATIO = 3            # Spacing between the in-game menu buttons as a ratio to their height
BORDER_WIDTH = 4                    # Width of the border surrounding the game board
TOP_MESSAGE_OFFSET = (5, 5)         # Offset between the top message and the top-left corner of the screen [pixels]
TOTAL_MOVES_OFFSET = 5              # Offset between the top message and the moves counter [pixels]
INITIAL_GRID_SIZE = 4               # Grid size to use for puzzle when the game first starts
MIN_GRID_SIZE = 2                   # Minimum grid size allowed for puzzles
MAX_GRID_SIZE = 128                 # Maximum grid size allowed for puzzles

# In-Game Messages
MSG_INSTRUCTIONS = "Click tiles next to empty space or press arrow keys to slide tiles."
MSG_SEARCHING = "Finding Solution (this may take a while)"
MSG_SOLVED = "Solved! (Esc to close)"
MSG_SOLVING = "Solving the game board"

# Color mapping (R, G, B)
COLORS = {
    "black": (0,   0,   0),
    "white": (255, 255, 255),
    "gold":  (200, 180, 0),
    "brown": (100, 50,  0)
}

# Color constants
BG_COLOR = COLORS["brown"]              # Color of the background
TILE_COLOR = COLORS["gold"]             # Color of the game tiles
TEXT_COLOR = COLORS["white"]            # Color of in-game text
BORDER_COLOR = COLORS["black"]          # Color of the border surrounding the game board
BUTTON_COLOR = COLORS["white"]          # Color of the menu buttons
BUTTON_TEXT_COLOR = COLORS["black"]     # Color of the menu button text
ACTIVE_TEXTBOX_COLOR = COLORS["gold"]   # Color of active text boxes

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
# attr           puzzle - Puzzle object used to hold the the puzzle information
# attr    initial_board - 2D array representing the initial state of the game board before any input movements
# attr       board_size - length/width of the game board
# attr        tile_size - size of the sliding game tiles
# attr tile_slide_speed - number of pixels the tiles will slide each frame when animating their movement
# attr        tile_font - Font object used to render the font on top of the sliding tiles
# attr         x_margin - space between the sides of the screen and the game board in pixels
# attr         y_margin - space between the top/bottom of the screen and the game board in pixels
# attr       basic_font - Font object used to render text not on the tiles
# attr      top_message - Rect object that is the size of the currently displayed message at the top of the screen
# attr     move_counter - Rect object that is the size of the "number of moves" counter
# attr      total_moves - number of moves used since the initial board state
# attr     THREAD_solve - Thread object used to solve the puzzle concurrently
# attr          buttons - array of Button objects representing the in-game menu buttons
# attr  active_text_box - current active text box that is handling user input
# attr  next_board_size - user requested next board size that will be applied when "New Board" button is pressed
class GraphicsEngine:
    def __init__(self):
        pg.init()
        pg.display.set_icon(pg.image.load("icon.png"))

        self.display = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), RESIZABLE)
        self.fps_clock = pg.time.Clock()
        self.puzzle = Puzzle(size=INITIAL_GRID_SIZE)
        self.initial_board = self.puzzle.board
        self.board_size = self.puzzle.board_size
        self.tile_size = 0
        self.tile_slide_speed = 0
        self.tile_font = None
        self.x_margin = 0
        self.y_margin = 0
        self.basic_font = None
        self.top_message = None
        self.move_counter = None
        self.total_moves = 0
        self.THREAD_solve = None
        self.buttons = []
        self.active_text_box = None
        self.next_board_size = None

        self.prepare_grid()
        self.draw_display()
        self.draw_board(self.puzzle.board)

    # Prepares various attributes to be appropriate for the selected board size
    def prepare_grid(self):
        width, height = self.display.get_size()

        self.tile_size = (min(width - SAFE_WIDTH, height - SAFE_HEIGHT) - self.board_size + 1) // self.board_size
        self.tile_font = pg.font.Font(GAME_FONT, self.tile_size // TILE_FONT_RATIO)
        self.tile_slide_speed = max(1, self.tile_size // TILE_SPEED_RATIO)
        self.x_margin = (width - self.tile_size * self.board_size) // 2 - 1
        self.y_margin = (height - self.tile_size * self.board_size) // 2 - 1

        pg.display.set_caption(f"{self.board_size ** 2 - 1} Puzzle")
    
    # Draws the base screen
    def draw_display(self):
        # Draw starting condition of the game
        self.display.fill(BG_COLOR)
        self.draw_menu()
        self.draw_message(MSG_INSTRUCTIONS)
        self.draw_move_count()

    # Draws the in-game menu onto the screen
    def draw_menu(self):
        button_names = ("Solve", "Reset", "New Board")
        button_funcs = (self.find_solution, self.reset_puzzle, self.new_puzzle)

        # Calculate appropriate sizes for current screen size
        width, height = self.display.get_size()
        button_size = (width // BUTTON_SIZE_RATIO[0], height // BUTTON_SIZE_RATIO[1])
        textbox_size = (width // TEXTBOX_SIZE_RATIO[0], height // TEXTBOX_SIZE_RATIO[1])
        self.basic_font = pg.font.Font(GAME_FONT, min(*button_size) // BASIC_FONT_RATIO)
        button_spacing = button_size[1] // BUTTON_SPACING_RATIO

        left_edge = width - (self.x_margin + button_size[0]) // 2
        top_edge = self.y_margin

        # Clear the buttons list of any previously drawn buttons
        self.buttons = []

        # Create and draw a Button object for each menu button
        for name, func in zip(button_names, button_funcs):
            self.draw_button(Button(Rect(left_edge, top_edge, *button_size), BUTTON_COLOR, name, func))

            top_edge += button_spacing + button_size[1]

        # Draw label for the Board Size text box
        rect = Rect(left_edge, top_edge, *button_size)
        text = self.basic_font.render("Board Size", True, TEXT_COLOR)
        self.display.blit(text, text.get_rect(topleft=rect.topleft))

        top_edge += button_spacing

        # Draw the Board Size text box
        rect = Rect(left_edge, top_edge, *textbox_size)
        text_box = TextBox(rect, ACTIVE_TEXTBOX_COLOR, BUTTON_COLOR, str(self.board_size), self.set_active_text_box)
        text_box.args = (text_box,)
        self.draw_button(text_box)

        # Flip screen here to prevent blank buttons while generating large puzzles
        pg.display.flip()

    # Draws a given button to the screen
    # param button - Button object to be drawn
    # param  color - color used to fill the button
    # param append - indicates whether the button should be appended to the list of buttons
    def draw_button(self, button: Button, color: tuple = None, append: bool = True):
        fill_color = color if color is not None else button.color

        self.display.fill(fill_color, button.rect)
        pg.display.update(button.rect)

        text = self.basic_font.render(button.text, True, BUTTON_TEXT_COLOR)
        self.display.blit(text, text.get_rect(center=button.rect.center))

        if append:
            self.buttons.append(button)

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

        # If the user has requested a new board size, update the board size and redraw the display
        if self.next_board_size is not None and self.board_size != self.next_board_size:
            self.clear_board()
            self.board_size = self.next_board_size
            self.next_board_size = None
            self.prepare_grid()

        self.puzzle.generate(self.board_size)
        self.initial_board = self.puzzle.board
        self.draw_board(self.puzzle.board)

        self.total_moves = 0
        self.draw_move_count()
        self.draw_message(MSG_INSTRUCTIONS)

    # Called when a text box is clicked, allows user input to be handled by the text box
    # param text_box - TextBox object that was clicked
    def set_active_text_box(self, text_box: TextBox):
        self.active_text_box = text_box
        self.draw_button(text_box, text_box.active_color, False)

    # Called when the user clicks outside of a text box, deactivates the active text box
    def reset_active_text_box(self):
        text_box = self.active_text_box
        self.active_text_box = None

        # Ensure new board size is within allotted range
        self.next_board_size = min(MAX_GRID_SIZE, max(MIN_GRID_SIZE, int(text_box.text)))
        if self.next_board_size != int(text_box.text):
            text_box.text = str(self.next_board_size)

        # Redraw the text box in its inactive state
        self.draw_button(text_box, append=False)
        pg.display.update(text_box.rect)

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
    #  param allow_updates - indicates whether board updates should happen during this call
    # return      slide_to - integer representing the direction the user wishes to move a tile
    # return          None - if user did not request a tile move
    def event_handler(self, allow_updates: bool = True) -> int | None:
        slide_to = None

        # Look through each event in the queue
        for event in pg.event.get():
            if event.type == QUIT:
                terminate()

            # User resized the screen
            if event.type == VIDEORESIZE:
                # Set these to None to prevent phantom rects from being drawn over text
                self.top_message = None
                self.move_counter = None

                # Redraw the screen
                self.prepare_grid()
                self.draw_display()
                self.draw_board(self.puzzle.board)

            # User clicked on the screen
            elif event.type == MOUSEBUTTONUP:
                if self.active_text_box is not None:
                    self.reset_active_text_box()

                if not allow_updates:
                    continue

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

            # User pressed a keyboard button
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()

                # If no text box is active, get the slide_to direction for the keypress
                if self.active_text_box is None:
                    slide_to = KEY_MAP.get(event.key)
                    continue

                if event.key == K_RETURN:
                    self.reset_active_text_box()

                # Let active text box handle the event, and redraw the text box if necessary
                elif self.active_text_box.handle_key(event):
                    self.set_active_text_box(self.active_text_box)

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
        # Clear previous game board and draw the border
        pg.draw.rect(self.display, BORDER_COLOR, self.clear_board(), BORDER_WIDTH)

        # Draw each tile in the board
        for x in range(self.board_size):
            for y in range(self.board_size):
                if board[y][x]:
                    self.draw_tile(x, y, board[y][x])

    # Clears the game board in preparation for it to be drawn
    # return rect - Rect object representing the are that was cleared
    def clear_board(self) -> Rect:
        size = self.board_size * (self.tile_size + 1) + 2 * BORDER_WIDTH
        rect = Rect(self.x_margin - BORDER_WIDTH, self.y_margin - BORDER_WIDTH, size, size)
        pg.draw.rect(self.display, BG_COLOR, rect)

        return rect

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
        return self.x_margin + (x * self.tile_size) + x, self.y_margin + (y * self.tile_size) + y

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

    # Draws the "Total Moves" counter
    def draw_move_count(self):
        if self.move_counter is not None:
            pg.draw.rect(self.display, BG_COLOR, self.move_counter)

        message_str = f"Total Moves: {str(self.total_moves)}"
        top_left = TOP_MESSAGE_OFFSET[0], self.basic_font.get_height() + TOP_MESSAGE_OFFSET[1] + TOTAL_MOVES_OFFSET
        text_surf, text_rect = self.make_text(message_str, TEXT_COLOR, BG_COLOR, *top_left)
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
            self.event_handler(False)


# Terminates the GUI
def terminate():
    pg.quit()
    exit('\nProgram Quit... Good Bye!')
