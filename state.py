from copy import deepcopy

import Settings.gamesettings as game_settings
import Settings.aisettings as ai_settings

class State:
    def __init__(self):
        self.moves = []
        self.board = deepcopy(game_settings.EMPTY_BOARD)
        self.current_turn = game_settings.FIRST_TURN
    
    def update_move(self, last_turn, move_position):
        """
        It updates the board with the last move, state.current_turn made by the player or computer
        
        :param last_turn: The last player to make a move
        :param move_position: The position of the move that was just made
        """
        r, c = move_position
        self.moves.append(move_position)
        self.board[r][c] = last_turn

        if(last_turn == game_settings.COM):
            self.current_turn = game_settings.HUMAN
        
        if(last_turn == game_settings.HUMAN):
            self.current_turn = game_settings.COM

    def game_over(board):
        """
        It checks if there is a winning pattern in the board
        
        :param board: the current state of the game
        :return: the winner of the game.
        """
        value_lines = State.split_board_to_arrays(board)

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
                        return game_settings.O
                    
                    # COM win
                    if(temp_line == ai_settings.X_END_GAME_PATTERN):
                        return game_settings.X
                    
        return game_settings.EMPTY
    
    def split_board_to_arrays(board_state):
        """
        It takes a 2D array and returns a list of 1D arrays, where each 1D array is a row, column, or
        diagonal of the original 2D array
        
        :param board_state: a 2D array of the current board state
        :return: A list of lists.
        """
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
    
    def get_new_board_after_moves(board, last_moves, current_turn):
        """
        It takes a board, a list of moves, and the current turn, and returns a new board with the moves
        applied
        
        :param board: the current board
        :param last_moves: a list of tuples, each tuple is a move (row, col)
        :param current_turn: the current player's turn
        :return: A new board with the last moves applied to it.
        """
        new_board = [row[:] for row in board]
        if len(last_moves) == 0:
            return new_board

        for move in last_moves:
            current_turn = game_settings.get_opponent(current_turn)
            r, c = move
            new_board[r][c] = current_turn
        return new_board
    
    def is_valid_move(move_position, board):
        """
        It checks if the move is valid.
        
        :param move_position: the position of the move
        :param board: the board that the player is playing on
        :return: The return value is a boolean value.
        """
        move_r, move_c = move_position
        is_r_valid = (0 <= move_r < game_settings.BOARD_ROWS)
        is_c_valid = (0 <= move_c < game_settings.BOARD_COLS)
        return is_c_valid and is_r_valid
    
    def generate_possible_moves(board, expansion_range):
        """
        If the board is empty, return all possible moves. Otherwise, return all possible moves that are
        not empty and have a neighbor
        
        :param board: the current board state
        :return: A list of tuples.
        """
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
                    if not State.has_neighbor((r, c), board, expansion_range):
                        continue
                    possible_moves.append((r, c))
        # #test
        # for move in possible_moves:
        #     print(move, end=" ")
        # print()
        # print(len(possible_moves))

        return possible_moves
    
    def has_neighbor(move_position, board, expansion_range):
        """
        It checks if a given position has a neighbor within a given range
        
        :param move_position: The position of the move you want to check
        :param board: the current board state
        :param expansion_range: The number of rows and columns to expand from the move position
        :return: a boolean value.
        """
        move_r, move_c = move_position
        r_radius = expansion_range
        c_radius = expansion_range

        for r in range(-r_radius, r_radius + 1):
            for c in range(-c_radius, c_radius + 1):
                neighbor_c = move_c + c
                neighbor_r = move_r + r
                neighbor_position = (neighbor_r, neighbor_c)
                neighbor = 0

                if(State.is_valid_move(neighbor_position, board)):
                    neighbor = board[neighbor_r][neighbor_c]
                
                if(neighbor != game_settings.EMPTY):
                    return True
        return False
    
    def high_impact_move(board, current_turn):
        """
        It takes a board and a player, and returns the move that would have the highest impact on the
        board, and the score of that move
        
        :param board: the current board
        :param current_turn: the current player's turn
        :return: A tuple of the highest score move and the highest score. 
        Return (None, 0) if the highest impact move's score do not reach HIGH_IMPACT_MOVE_THRESHOLD.
        """
        temp_board = deepcopy(board)
        board_O_score, board_X_score = State.evaluate(board)
        highest_score = 0
        highest_score_move = None
        for r in range(0, game_settings.BOARD_ROWS):
            for c in range(0, game_settings.BOARD_COLS):
                if(temp_board[r][c] == game_settings.EMPTY):
                    temp_board[r][c] = current_turn
                    temp_board_O_score, temp_board_X_score = State.evaluate(temp_board)
                    score = 0
                    if(current_turn == game_settings.O):
                        score = temp_board_O_score - board_O_score
                    elif(current_turn == game_settings.X):
                        score = temp_board_X_score - board_X_score
                    
                    if(score > highest_score):
                        highest_score = score
                        highest_score_move = (r, c)
                    
                    temp_board[r][c] = game_settings.EMPTY
        
        if (highest_score >= ai_settings.HIGH_IMPACT_MOVE_THRESHOLD):
            return (highest_score_move, highest_score)
        else:
            return (None, 0)


    def get_direction_patterns(board, move, streak, current_turn):
        """
        It takes a board, a move, a streak, and the current turn, and returns a list of lists of the
        pieces in the directions of the move
        
        :param board: the current board
        :param move: the move that is being evaluated
        :param streak: the number of pieces in a row needed to win
        :param current_turn: the current player's turn
        :return: A list of lists of patterns.
        """
        if not State.is_valid_move(temp_move, board):
            return []
        # streak = number of unblocked pieces
        move_r, move_c = move
        # r ~ x
        # c ~ y
        direction_patterns = []
        # horizontal
        pattern = []
        for i in range(-streak, streak + 1):
            if(i == 0):
                temp_move = move
                pattern.append(current_turn)
            else:
                temp_move = (move_r + i, move_c)
                if(State.is_valid_move(temp_move, board)):
                    temp_move_r, temp_move_c = temp_move
                    pattern.append(board[temp_move_r][temp_move_c])
        if(len(pattern) > streak + 2):
            direction_patterns.append(pattern)

        # vertical
        pattern = []
        for i in range(-streak, streak + 1):
            if(i == 0):
                temp_move = move
                pattern.append(current_turn)
            else:
                temp_move = (move_r, move_c + i)
                if(State.is_valid_move(temp_move, board)):
                    temp_move_r, temp_move_c = temp_move
                    pattern.append(board[temp_move_r][temp_move_c])
        if(len(pattern) > streak + 2):
            direction_patterns.append(pattern)

        # diagonals
        # lower-left to upper-right
        pattern = []
        for i in range(-streak, streak + 1):
            if(i == 0):
                temp_move = move
                pattern.append(current_turn)
            else:
                temp_move = (move_r + i, move_c + i)
                if(State.is_valid_move(temp_move, board)):
                    temp_move_r, temp_move_c = temp_move
                    pattern.append(board[temp_move_r][temp_move_c])
        if(len(pattern) > streak + 2):
            direction_patterns.append(pattern)
        # upper-left to lower-right
        pattern = []
        for i in range(-streak, streak + 1):
            if(i == 0):
                temp_move = move
                pattern.append(current_turn)
            else:
                temp_move = (move_r - i, move_c + i)
                if(State.is_valid_move(temp_move, board)):
                    temp_move_r, temp_move_c = temp_move
                    pattern.append(board[temp_move_r][temp_move_c])
        if(len(pattern) > streak + 2):
            direction_patterns.append(pattern)

        return direction_patterns
    
    def evaluate(board):
        """
        It takes a board and returns a tuple of scores for each player
        
        :param board: the board to evaluate
        :return: The score of the board.
        """
        O_score = 0
        X_score = 0

        lines = State.split_board_to_arrays(board)

        for line in lines:
            line_O_score, line_X_score = State.evaluate_line(line)
            O_score += line_O_score
            X_score += line_X_score

        #test
        # if(O_score >= 50000 or X_score >= 50000):

        return (O_score, X_score)
    
    # return(O_score, X_score)
    def evaluate_line(line):
        """
        It takes a line of the board and returns the score for O and X
        
        :param line: a list of the board positions in a row, column, or diagonal
        :return: a tuple of two values.
        """
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
                    if(temp_line == pattern):
                        O_score += ai_settings.O_6_PATTERNS_SCORES[p]

                # X score
                for p, pattern in enumerate(ai_settings.X_6_PATTERNS):
                    if(temp_line == pattern):
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
                    if(temp_line == pattern):
                        O_score += ai_settings.O_5_PATTERNS_SCORES[p]

                # X score
                for p, pattern in enumerate(ai_settings.X_5_PATTERNS):
                    if(temp_line == pattern):
                        X_score += ai_settings.X_5_PATTERNS_SCORES[p]
        return(O_score, X_score)

    # unused function
    def has_checkmate(board, current_turn, move):
        """
        It checks if a move will be a "win move" for the current player
        
        :param board: the current board
        :param current_turn: the current player's turn
        :param move: the move that was just made
        :return: a boolean value.
        """
        # has_checkmate = a continuous-five

        # continuous-five
        streak = 5 - 1 # continuous-five cant be blocked
        continuous_five_pattern = None
        if(current_turn == game_settings.X):
            continuous_five_pattern = ai_settings.X_END_GAME_PATTERN
        elif(current_turn == game_settings.O):
            continuous_five_pattern = ai_settings.O_END_GAME_PATTERN

        direction_patterns = State.get_direction_patterns(board, move, streak, current_turn)
        if(len(direction_patterns) > 0) :
            for pattern in direction_patterns:
                for i in range(0, len(pattern) - len(continuous_five_pattern) + 1):
                    checking_pattern = [
                        pattern[i],
                        pattern[i+1],
                        pattern[i+2],
                        pattern[i+3],
                        pattern[i+4],
                    ]
                    if(checking_pattern == continuous_five_pattern):
                        return True
        return False
    
    # unused function
    def has_check(board, current_turn, move):
        """
        It checks if a move could lead to a win for the current player
        
        :param board: the current board
        :param current_turn: the current player's turn
        :param move: the move that is being checked
        :return: a boolean value.
        """
        # has_check = a unblocked four or n unblocked-threes (n >= 2) or unblocked-threes combine one-end-blocked-fours

        # unblocked four
        streak = 4 # streak = number of unblocked pieces
        unblocked_four_pattern = None
        if(current_turn == game_settings.X):
            unblocked_four_pattern = ai_settings.X_6_PATTERNS[0]
        elif(current_turn == game_settings.O):
            unblocked_four_pattern = ai_settings.O_6_PATTERNS[0]

        direction_patterns = State.get_direction_patterns(board, move, streak, current_turn)
        if(len(direction_patterns) > 0) :
            for pattern in direction_patterns:
                # make sure that current_turn is counted in pattern
                if(pattern[0] != game_settings.EMPTY and pattern[-1] != game_settings.EMPTY):
                    for i in range(0, len(pattern) - len(unblocked_four_pattern) + 1):
                        checking_pattern = [
                            pattern[i],
                            pattern[i+1],
                            pattern[i+2],
                            pattern[i+3],
                            pattern[i+4],
                            pattern[i+5]
                        ]
                        if(checking_pattern == unblocked_four_pattern):
                            return True
        # n unblocked-threes (n >= 2)
        unblocked_three_count = 0
        streak = 3 # streak = number of unblocked pieces
        unblocked_three_patterns = []
        unblocked_three_pattern_length = 6
        if(current_turn == game_settings.X):
            for pattern in ai_settings.X_6_PATTERNS:
                if(pattern.count(game_settings.X) == 3):
                    unblocked_three_patterns.append(pattern)
        elif(current_turn == game_settings.O):
            for pattern in ai_settings.O_6_PATTERNS:
                if(pattern.count(game_settings.O) == 3):
                    unblocked_three_patterns.append(pattern)
        
        direction_patterns = State.get_direction_patterns(board, move, streak, current_turn)
        
        if(len(direction_patterns) > 0) :
            for pattern in direction_patterns:
                # make sure that current_turn is counted in pattern
                if(pattern[0] != game_settings.EMPTY and pattern[-1] != game_settings.EMPTY):
                    for i in range(0, len(pattern) - unblocked_three_pattern_length + 1):
                        checking_pattern = [
                            pattern[i],
                            pattern[i+1],
                            pattern[i+2],
                            pattern[i+3],
                            pattern[i+4],
                            pattern[i+5]
                        ]
                        for unblocked_three_pattern in unblocked_three_patterns:
                            if(checking_pattern == unblocked_three_pattern):
                                unblocked_three_count += 1
            if (unblocked_three_count >= 2):
                return True
            
        # unblocked-threes combine one-end-blocked-fours
        return False
