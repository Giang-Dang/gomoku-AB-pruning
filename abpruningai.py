import random
import time

from copy import deepcopy
from math import inf as infinity
import Settings.aisettings as ai_settings
import Settings.gamesettings as game_settings
from state import State
from minimaxnode import MinimaxNode

class ABPruningAI:
    def __init__(self, __state: State) -> None:
        self.state = __state

    def next_move(self):
        if(self.state.board == game_settings.EMPTY_BOARD or len(self.state.moves) == 1):
            return self.random_move(self.state)
        
        root_node = MinimaxNode(self.state.board, self.state.moves[-1::1], self.state.current_turn, None)
        
        #test
        attrs = vars(root_node)
        print(', '.join("%s: %s" % item for item in attrs.items()))

        score = ABPruningAI.alpha_beta(root_node, ai_settings.MAX_TREE_DEPTH_LEVEL, -infinity, +infinity, True)
        return root_node.planing_next_move

    def random_move(self, state: State):
        possible_moves = State.generate_possible_moves(state.board)
        return random.choice(possible_moves)

    def alpha_beta(current_node: MinimaxNode, depth, alpha, beta, maximizingPlayer):
        # https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
        # https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
        
        # fail-soft alpha-beta
        if(depth == 0 or State.game_over(current_node.board)):
            return ABPruningAI.evaluate(current_node.board)
        
        if maximizingPlayer:
            value = -infinity
            child_nodes = current_node.generate_child_nodes()
            for child_node in child_nodes:
                temp = ABPruningAI.alpha_beta(child_node, depth - 1, alpha, beta, False)
                alpha = max(alpha, value)
                #value = max(value, temp)
                if temp > value:
                    value = temp
                    current_node.planing_next_move = child_node.last_move
                if value >= beta:
                    break
            return value
        else:
            value = + infinity
            child_nodes = current_node.generate_child_nodes()
            for child_node in child_nodes:
                temp = ABPruningAI.alpha_beta(child_node, depth - 1, alpha, beta, True)
                # value = min(value, temp)
                if temp < value:
                    value = temp
                    current_node.planing_next_move = child_node.last_move
                beta = min(beta, value)
            return value
    
    def evaluate(board):
        O_score = 0
        X_score = 0

        lines = State.split_board_to_arrays(board)

        for line in lines:
            line_O_score, line_X_score = ABPruningAI.evaluate_line(line)
            O_score += line_O_score
            X_score += line_X_score

        #test
        # if(O_score >= 50000 or X_score >= 50000):
        #     input()

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



