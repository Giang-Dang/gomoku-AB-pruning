from copy import deepcopy

import Settings.gamesettings as game_settings
import Settings.aisettings as ai_settings

class State:
    def __init__(self):
        self.moves = []
        self.board = deepcopy(game_settings.EMPTY_BOARD)
        self.current_turn = game_settings.FIRST_TURN
    
    def update_move(self, last_turn, move_position):
        r, c = move_position
        self.moves.append(move_position)
        self.board[r][c] = last_turn

        if(last_turn == game_settings.COM):
            self.current_turn = game_settings.HUMAN
        
        if(last_turn == game_settings.HUMAN):
            self.current_turn = game_settings.COM

    def is_win(self):
        value_board = self.board
        value_lines = State.split_board_to_arrays(value_board)

        for value_line in value_lines:
            pattern_length = 5
            if(len(value_line) >= pattern_length):
                for i in range(0, len(value_line) - pattern_length + 1):
                    temp_line = [
                        value_line[i],
                        value_line[i+1],
                        value_line[i+2],
                        value_line[i+3],
                        value_line[i+4]
                    ]
                    # HUMAN win
                    if(temp_line == ai_settings.O_END_GAME_PATTERN):
                        return True
                    
                    # COM win
                    if(temp_line == ai_settings.X_END_GAME_PATTERN):
                        return True
                    
        return False
    
    def split_board_to_arrays(board_state):
        res_arrays = []
        # diagonals: (SQUARE ONLY)
        # https://stackoverflow.com/questions/6313308/get-all-the-diagonals-in-a-matrix-list-of-lists-in-python

        # convert "upper left - lower right" diagonal lines to list of "straight lines"
        #   0 1 2         list[[]]
        # 0 ⟍ ⟍ ⟍        —
        # 1 ⟍ ⟍ ⟍        — —
        # 2 * ⟍ ⟍    =>  — — —
        #                 — —
        #                 —
        # start at *
        diagonal_count = range(-(game_settings.BOARD_ROWS-1), game_settings.BOARD_COLS, 1)
        for d in diagonal_count:
            res_arrays.append( [ row[r+d] for r,row in enumerate(board_state) if 0 <= r+d < len(row)] )

        # convert "lower left - upper right" diagonal lines to list of "straight lines"
        #   0 1 2         list[[]]
        # 0 ⟋ ⟋ ⟋        —
        # 1 ⟋ ⟋ ⟋        — —
        # 2 ⟋ ⟋ *    =>  — — —
        #                 — —
        #                 —
        # start at *
        for d in diagonal_count:
            res_arrays.append( [ row[~(r+d)] for r,row in enumerate(board_state) if 0 <= r+d < len(row)] )

        # rows
        for row in board_state:
            res_arrays.append(deepcopy(row))

        # columns
        for c in range(0, game_settings.BOARD_COLS):
            temp_column = []
            for r in range(0, game_settings.BOARD_ROWS):
                temp_column.append(board_state[r][c])
            res_arrays.append(temp_column)
        
        return res_arrays
    
    def get_new_state_after_move(move, turn, board):
        new_board = [row[:] for row in board]
        r, c = move
        new_board[r][c] = turn
        return new_board