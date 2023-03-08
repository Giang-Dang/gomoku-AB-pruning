import Settings.gamesettings as game_settings

# FPS
FPS = 60

# RGB COLOR
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GREY = (195, 195, 195)
COLOR_WOOD_BROWN = (208, 161, 115)
COLOR_BLUE = (0, 0, 255)
COLOR_RED = (255, 0, 0)
COLOR_WHITE_VANILLA = (244, 240, 220)
COLOR_BRIGHT_YELLOW = (251, 230, 91)
COLOR_CYAN = (57, 183, 237)
COLOR_DARK_GREEN = (0, 100, 0)

# BORDER
BORDER_SIZE = 30

# INFO TEXT
INFO_TEXT_FONT_SIZE = 30

NEW_GAME_INFO_TEXT = "PRESS \"NEW GAME\" TO START NEW GAME"
HUMAN_TURN_INFO_TEXT = "YOUR TURN"
COM_TURN_INFO_TEXT = "AI TURN"
HUMAN_WIN_INFO_TEXT = "HUMAN WIN!"
COM_WIN_INFO_TEXT = "AI WIN!"
DRAW_INFO_TEXT = "DRAW!"

# BOARD
SQUARE_SIZE = 35 

CENTER_CIRCLE_RADIUS = 8

BOARD_WIDTH = game_settings.BOARD_COLS * SQUARE_SIZE
BOARD_HEIGHT = game_settings.BOARD_ROWS * SQUARE_SIZE

BOARD_POS_X_MIN = BORDER_SIZE
BOARD_POS_Y_MIN = BORDER_SIZE + INFO_TEXT_FONT_SIZE + BORDER_SIZE
BOARD_POS_X_MAX = BOARD_POS_X_MIN + BOARD_WIDTH
BOARD_POS_Y_MAX = BOARD_POS_Y_MIN + BOARD_HEIGHT

BOARD_COLOR = COLOR_WHITE_VANILLA
BOARD_LINE_WIDTH = 2

# BUTTON
BUTTON_WIDTH = 125
BUTTON_HEIGHT = 45
BUTTON_COLOR = COLOR_CYAN
BUTTON_TEXT_COLOR = COLOR_BLACK
BUTTON_TEXT_FONT_SIZE = 15


# WINDOW
WINDOW_WIDTH = BORDER_SIZE + BOARD_WIDTH + BORDER_SIZE
WINDOW_HEIGHT = BORDER_SIZE + INFO_TEXT_FONT_SIZE + BORDER_SIZE + BOARD_HEIGHT + BORDER_SIZE + BUTTON_HEIGHT + BORDER_SIZE*2
WINDOW_TITLE = 'Caro'

# CELL
O_CELL_BORDER = 4
O_RADIUS = SQUARE_SIZE/2
O_LINE_THICKNESS = 4

X_CELL_BORDER = 6
X_LINE_THICKNESS = 6


# NEW GAME BUTTON

NEW_GAME_BUTTON_POS_X_MIN = BORDER_SIZE + (BOARD_WIDTH - BUTTON_WIDTH)/2
NEW_GAME_BUTTON_POS_X_MAX = NEW_GAME_BUTTON_POS_X_MIN + BUTTON_WIDTH
NEW_GAME_BUTTON_POS_Y_MIN = BORDER_SIZE*2 + INFO_TEXT_FONT_SIZE + BOARD_HEIGHT + BORDER_SIZE
NEW_GAME_BUTTON_POS_Y_MAX = NEW_GAME_BUTTON_POS_Y_MIN + BUTTON_HEIGHT

NEW_GAME_BUTTON_POS = (NEW_GAME_BUTTON_POS_X_MIN, NEW_GAME_BUTTON_POS_Y_MIN)