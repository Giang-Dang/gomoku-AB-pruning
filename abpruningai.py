import random
import Settings.aisettings as ai_settings
import Settings.gamesettings as game_settings
from state import State

class ABPruningAI:
    def __init__(self, __state: State) -> None:
        self.state = __state

    def next_move(self):
        if(self.state.board == game_settings.EMPTY_BOARD or len(self.state.moves) == 1):
            return self.random_move(self.state)
        return self.random_move(self.state)

    def random_move(self, state: State):
        possible_moves = self.generate_possible_moves(state.board)
        return random.choice(possible_moves)

    def generate_possible_moves(self, board):
        possible_moves = []
        if(board == game_settings.EMPTY_BOARD):
            for r in range(0, game_settings.BOARD_ROWS):
                for c in range(0, game_settings.BOARD_COLS):
                    possible_moves.append((r, c))
        else:
            for r in range(0, game_settings.BOARD_ROWS):
                for c in range(0, game_settings.BOARD_COLS):
                    temp_move = board[r][c]
                    if(temp_move != game_settings.EMPTY):
                        continue
                    if not self.has_neighbor((r, c), board):
                        continue
                    possible_moves.append((r, c))
        return possible_moves
    
    def has_neighbor(self, move_position, board):
        move_r, move_c = move_position
        r_radius = ai_settings.EXPANSION_RANGE
        c_radius = ai_settings.EXPANSION_RANGE

        for r in range(-r_radius, r_radius + 1):
            for c in range(-c_radius, c_radius + 1):
                neighbor_c = move_c + c
                neighbor_r = move_r + r
                neighbor_position = (neighbor_r, neighbor_c)
                neighbor = 0
                
                if(self.is_valid_move(neighbor_position, board)):
                    neighbor = board[neighbor_r][neighbor_c]
                
                if(neighbor != game_settings.EMPTY):
                    return True
        return False
    
    def is_valid_move(self, move_position, board):
        move_r, move_c = move_position
        is_r_valid = (0 <= move_r < game_settings.BOARD_ROWS)
        is_c_valid = (0 <= move_c < game_settings.BOARD_COLS)
        return is_c_valid and is_r_valid

    def evaluate(board):
        O_score = 0
        X_score = 0

        lines = State.split_board_to_arrays(board)

        for line in lines:
            line_O_score, line_X_score = ABPruningAI.evaluate_line(line)
            O_score += line_O_score
            X_score += line_X_score

        if(game_settings.O == game_settings.HUMAN):
            return X_score - O_score
        else:
            return O_score - X_score
    
    # return(O_score, X_score)
    def evaluate_line(line):
        O_score = 0
        X_score = 0

        # check 6 patterns
        pattern_length = 6
        if(len(line) >= pattern_length):
            for i in range(0, len(line) - pattern_length + 1):
                temp_line = [
                    line[i],
                    line[i+1],
                    line[i+2],
                    line[i+3],
                    line[i+4],
                    line[i+5]
                ]
                # O score
                for p, pattern in enumerate(ai_settings.O_6_PATTERNS):
                    if(line == pattern):
                        O_score += ai_settings.O_6_PATTERNS_SCORES[p]

                # X score
                for p, pattern in enumerate(ai_settings.X_6_PATTERNS):
                    if(line == pattern):
                        X_score += ai_settings.X_6_PATTERNS_SCORES[p]

        # check 6 patterns
        pattern_length = 5
        if(len(line) >= pattern_length):
            for i in range(0, len(line) - pattern_length + 1):
                temp_line = [
                    line[i],
                    line[i+1],
                    line[i+2],
                    line[i+3],
                    line[i+4]
                ]
                # O score
                for p, pattern in enumerate(ai_settings.O_5_PATTERNS):
                    if(line == pattern):
                        O_score += ai_settings.O_5_PATTERNS_SCORES[p]

                # X score
                for p, pattern in enumerate(ai_settings.X_5_PATTERNS):
                    if(line == pattern):
                        X_score += ai_settings.X_5_PATTERNS_SCORES[p]
        return(O_score, X_score)
    
    def is_leaf_node():
        pass