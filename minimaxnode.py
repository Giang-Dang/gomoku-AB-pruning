from copy import deepcopy
from state import State
import Settings.gamesettings as game_settings

class MinimaxNode:
    def __init__(self, board, last_move, current_turn, planing_next_move) -> None:
        self.board = deepcopy(board)
        self.last_move = last_move
        self.planing_next_move = planing_next_move
        self.current_turn = current_turn

    def generate_child_nodes(self):
        possible_moves = State.generate_possible_moves(self.board)
        child_nodes = []
        for move in possible_moves:
            child_node = MinimaxNode(self.board, move, game_settings.get_opponent(self.current_turn), None)
            child_node.board[move[0]][move[1]] = self.current_turn

            child_nodes.append(child_node)
        
        return child_nodes