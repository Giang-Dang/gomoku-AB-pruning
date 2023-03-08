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
        """
        The function first checks if the current state is the first move or not. If it is, it will
        return a random move. If not, it will check if the opponent has a high impact move. If it does,
        the AI will take that move. If not, it will use the alpha-beta pruning algorithm to find the
        best move
        :return: The next move to be played.
        """
        #first move
        if(self.state.board == game_settings.EMPTY_BOARD or len(self.state.moves) <= 1):
            return self.random_move(self.state, 1)
        
        # check if opponent has high impact move, AI will take this move
        if ai_settings.ENABLE_HIGH_IMPACT_MOVE:
            opponent_high_impact_move, opponent_high_impact_score = State.high_impact_move(self.state.board, game_settings.get_opponent(self.state.current_turn))
            player_high_impact_move, player_high_impact_score = State.high_impact_move(self.state.board, self.state.current_turn)
            if opponent_high_impact_move and opponent_high_impact_score > player_high_impact_score:
                return opponent_high_impact_move
            if player_high_impact_move and player_high_impact_score >= opponent_high_impact_score: # >=: Prioritize playing the move to the advantage of the player
                return player_high_impact_move

        # if not
        root_node = MinimaxNode(self.state.board, self.state.moves[-1::1], self.state.current_turn, None)
        
        # #test
        # attrs = vars(root_node)
        # print(', '.join("%s: %s" % item for item in attrs.items()))

        score = ABPruningAI.alpha_beta(root_node, ai_settings.MAX_TREE_DEPTH_LEVEL, -infinity, +infinity, True)
        return root_node.planing_next_move

    def random_move(self, state: State, expansion_range):
        """
        The function takes in a state and an expansion range, and returns a random move from the
        possible moves
        
        :param state: the current state of the game
        :type state: State
        :param expansion_range: The number of steps to expand the search tree
        :return: A tuple of two integers.
        """
        # AI move first
        if(state.board == game_settings.EMPTY_BOARD):
            return(int(game_settings.BOARD_ROWS / 2), int(game_settings.BOARD_COLS / 2))
        # HUMAN move first
        possible_moves = State.generate_possible_moves(state.board, expansion_range)
        return random.choice(possible_moves)

    def alpha_beta(current_node: MinimaxNode, depth, alpha, beta, maximizingPlayer):
        """
        
        It's a recursive function that implements alpha beta pruning algorithm 
        to calculate the best possible score for the current player, given the current board state
        
        :param current_node: MinimaxNode, depth, alpha, beta, maximizingPlayer
        :type current_node: MinimaxNode
        :param depth: The depth of the search tree
        :param alpha: the best value that the maximizing player currently can guarantee at this point or
        above
        :param beta: the best value that the maximizing player currently can guarantee at that level or
        higher
        :param maximizingPlayer: True if it's the AI's turn, False if it's the player's turn
        :return: The value of the best move.
        """
        # https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
        # https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
        
        # fail-soft alpha-beta
        if(depth == 0 or State.game_over(current_node.board)):
            O_score, X_score = State.evaluate(current_node.board)
            return X_score - O_score
        
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
    
    



