import pygame
from time import sleep

from state import State
import Settings.rendersettings as render_settings
import Settings.gamesettings as game_settings


class GameRender:
    def __init__(self, state: State):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((render_settings.WINDOW_WIDTH, render_settings.WINDOW_HEIGHT))
        pygame.display.set_caption(render_settings.WINDOW_TITLE)
        self.screen.fill(render_settings.BOARD_COLOR)
        self.update_state(state.board, game_settings.FIRST_TURN, False)
        pygame.display.update()

    
    def update_state(self, board, turn, is_win):
        self.clear()
        if(is_win):
            # current turn == HUMAN => COM win
            if(turn == game_settings.COM):
                self.draw_board(board, render_settings.COM_WIN_INFO_TEXT, render_settings.COLOR_BLUE)
            # current turn == HUMAN => COM win
            if(turn == game_settings.HUMAN):
                self.draw_board(board, render_settings.HUMAN_WIN_INFO_TEXT, render_settings.COLOR_RED)
            return

        if(turn == game_settings.HUMAN):
            self.draw_board(board, render_settings.HUMAN_TURN_INFO_TEXT, render_settings.COLOR_RED)

        if(turn == game_settings.COM):
            self.draw_board(board, render_settings.COM_TURN_INFO_TEXT, render_settings.COLOR_BLUE)

    def draw_X(self, x, y):
        #    x
        # y ╔═════════════════════════════════▶
        #   ║ (X1, Y1) ╔═══╗ (X2, Y1)
        #   ║          ║   ║
        #   ▼ (X1, Y2) ╚═══╝ (X2, Y2)
        #
        # line 1: (X1, Y1) -> (X2, Y2)
        # line 2: (X1, Y2) -> (X2, Y1)
        pos_X1 = render_settings.BOARD_POS_X_MIN + y * render_settings.SQUARE_SIZE
        pos_X2 = render_settings.BOARD_POS_X_MIN + (y+1) * render_settings.SQUARE_SIZE
        pos_Y1 = render_settings.BOARD_POS_Y_MIN + x * render_settings.SQUARE_SIZE
        pos_Y2 = render_settings.BOARD_POS_Y_MIN + (x+1) * render_settings.SQUARE_SIZE
        # subtract cell border
        pos_X1 = pos_X1 + render_settings.X_CELL_BORDER
        pos_X2 = pos_X2 - render_settings.X_CELL_BORDER
        pos_Y1 = pos_Y1 + render_settings.X_CELL_BORDER
        pos_Y2 = pos_Y2 - render_settings.X_CELL_BORDER
        # draw line 1
        pygame.draw.line(self.screen, render_settings.COLOR_BLUE, (pos_X1, pos_Y1), (pos_X2, pos_Y2), render_settings.X_LINE_THICKNESS)
        # draw line 2
        pygame.draw.line(self.screen, render_settings.COLOR_BLUE, (pos_X1, pos_Y2), (pos_X2, pos_Y1), render_settings.X_LINE_THICKNESS)
        
    def draw_O(self, x, y):
        posX = render_settings.BOARD_POS_X_MIN + render_settings.SQUARE_SIZE/2 + y * render_settings.SQUARE_SIZE + render_settings.O_LINE_THICKNESS/2
        posY = render_settings.BOARD_POS_Y_MIN + render_settings.SQUARE_SIZE/2 + x * render_settings.SQUARE_SIZE + render_settings.O_LINE_THICKNESS/2
        # subtract cell border
        radius = render_settings.O_RADIUS - render_settings.O_CELL_BORDER
        # draw circle
        pygame.draw.circle(self.screen, render_settings.COLOR_RED, [posX, posY], radius , render_settings.O_LINE_THICKNESS)
    
    def draw_button(self, pos, width, height, text):
        rectButton = pygame.Rect(pos, (width, height))
        font_text = pygame.font.Font(pygame.font.get_default_font(), render_settings.BUTTON_TEXT_FONT_SIZE)
        text_surf = font_text.render(text, True, render_settings.BUTTON_TEXT_COLOR)
        text_rect = text_surf.get_rect(center = rectButton.center)
        pygame.draw.rect(self.screen, render_settings.BUTTON_COLOR, rectButton)
        self.screen.blit(text_surf, text_rect)

    def draw_info_text(self, text, textColor):
        text_pos = (render_settings.WINDOW_WIDTH/2, render_settings.BORDER_SIZE + render_settings.INFO_TEXT_FONT_SIZE/2)

        font_text = pygame.font.Font(pygame.font.get_default_font(), render_settings.INFO_TEXT_FONT_SIZE)
        text_surf = font_text.render(text, False, textColor)
        text_rect = text_surf.get_rect(center = text_pos)
        self.screen.blit(text_surf, text_rect)
        pygame.display.update()

    
    def draw_board(self, board_state, infoText, infoTextColor):
        # draw board
        # draw vertical line
        for r in range (0, game_settings.BOARD_COLS + 1):
            
            pygame.draw.line(self.screen, render_settings.COLOR_BLACK, 
            [render_settings.BOARD_POS_X_MIN + render_settings.SQUARE_SIZE * r, render_settings.BOARD_POS_Y_MIN], [render_settings.BOARD_POS_X_MIN + render_settings.SQUARE_SIZE * r, render_settings.BOARD_POS_Y_MIN + render_settings.BOARD_HEIGHT], render_settings.BOARD_LINE_WIDTH)
        # draw horizontal line
        for r in range (0, game_settings.BOARD_ROWS + 1):
            pygame.draw.line(self.screen, render_settings.COLOR_BLACK,
            [render_settings.BOARD_POS_X_MIN, render_settings.BOARD_POS_Y_MIN + render_settings.SQUARE_SIZE * r], [render_settings.BOARD_POS_X_MIN + render_settings.BOARD_WIDTH, render_settings.BOARD_POS_Y_MIN + render_settings.SQUARE_SIZE * r], render_settings.BOARD_LINE_WIDTH)
        
        # draw INFO TEXT
        self.draw_info_text(infoText, infoTextColor)

        # draw NEW GAME button
        self.draw_button(render_settings.NEW_GAME_BUTTON_POS, render_settings.BUTTON_WIDTH, render_settings.BUTTON_HEIGHT, "NEW GAME")

        # render board moves
        for r in range (0, game_settings.BOARD_ROWS):
            for c in range (0, game_settings.BOARD_COLS):
                # Empty cell
                if board_state[r][c] == game_settings.EMPTY: 
                    continue
                # Human move
                if board_state[r][c] == game_settings.O: 
                    self.draw_O(r, c)
                # COM move
                if board_state[r][c] == game_settings.X: 
                    self.draw_X(r, c)
        pygame.display.update()
        #test
        print("Drawing board is completed")
    
    #COM moves
    def update_com_move(self, com_move, state: State, is_win):
        state.update_move(game_settings.COM, com_move)
        self.update_state(state.board, game_settings.HUMAN, is_win)

    #HUMAN moves
    def is_new_game_button_pressed(self, mouse_position):
        mouse_x_position, mouse_y_position = mouse_position
        is_in_x_button_area = render_settings.NEW_GAME_BUTTON_POS_X_MIN < mouse_x_position < render_settings.NEW_GAME_BUTTON_POS_X_MAX
        is_in_y_button_area = render_settings.NEW_GAME_BUTTON_POS_Y_MIN < mouse_y_position < render_settings.NEW_GAME_BUTTON_POS_Y_MAX
        return is_in_x_button_area and is_in_y_button_area
        
    def is_new_move_valid(self, mouse_position, state: State):
        if (self.is_mouse_position_in_board_area(mouse_position)):
            square_x_position, square_y_position =  self.get_board_square_position(mouse_position)
            is_selected_square_empty = state.board[square_x_position][square_y_position] == game_settings.EMPTY
            return is_selected_square_empty
        else:
            return False

    def is_mouse_position_in_board_area(self, mouse_position):
        mouse_x_position, mouse_y_position = mouse_position
        is_mouse_x_position_valid = render_settings.BOARD_POS_X_MIN < mouse_x_position < render_settings.BOARD_POS_X_MAX
        is_mouse_y_position_valid = render_settings.BOARD_POS_Y_MIN < mouse_y_position < render_settings.BOARD_POS_Y_MAX
        return is_mouse_x_position_valid and is_mouse_y_position_valid

    def get_board_square_position(self, mouse_position):
        mouse_x_position, mouse_y_position = mouse_position
        #The boardsquare's x, y position is inverse to the mouse positions'. 
        board_square_y_position = int((mouse_x_position - render_settings.BOARD_POS_X_MIN) / render_settings.SQUARE_SIZE)
        board_square_x_position = int((mouse_y_position - render_settings.BOARD_POS_Y_MIN) / render_settings.SQUARE_SIZE)
        return (board_square_x_position, board_square_y_position)
    
    def clear(self):
        self.screen.fill(render_settings.BOARD_COLOR)
        pygame.display.update()

    def handle_human_action(self, state: State, is_win):
        mouse_button_pressed = pygame.mouse.get_pressed()
        # mouse left click
        if mouse_button_pressed[0]:
            mouse_position = pygame.mouse.get_pos()
            if self.is_new_game_button_pressed(mouse_position):
                state = State()
                print(state.board)
                self = GameRender(state)
                return True
            if self.is_new_move_valid(mouse_position, state):
                human_move = self.get_board_square_position(mouse_position)
                state.update_move(game_settings.HUMAN, human_move)
                self.update_state(state.board, game_settings.COM, is_win)
                return True
        return False
    
