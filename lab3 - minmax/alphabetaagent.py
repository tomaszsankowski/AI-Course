import random
from exceptions import AgentException

import copy


class AlphaBetaAgent:
    def __init__(self, my_token='o'):
        self.my_token = my_token

    def decide(self, connect4):
        if connect4.who_moves != self.my_token:
            raise AgentException('not my round')
        return self.alphabeta(connect4, 4, float('-inf'), float('inf'), True)[1]

    def alphabeta(self, connect4, depth, alpha, beta, is_maximizing):
        best_move = None
        if connect4.game_over:
            if connect4.wins is None:
                return 0, None
            elif connect4.wins == self.my_token:
                return 1, None
            else:
                return -1, None
        elif depth == 0:
            return 0, None
        elif is_maximizing:  # my Round
            value = -1000
            for s in connect4.possible_drops():
                tmp_connect4 = copy.deepcopy(connect4)
                tmp_connect4.drop_token(s)
                tmp, _ = self.alphabeta(tmp_connect4, depth - 1, alpha, beta, False)
                if tmp > value:
                    value = tmp
                    best_move = s
                if value > alpha:
                    alpha = value
                if value >= beta:
                    break
        else:  # opponent's Round
            value = 1000
            for s in connect4.possible_drops():
                tmp_connect4 = copy.deepcopy(connect4)
                tmp_connect4.drop_token(s)
                tmp, _ = self.alphabeta(tmp_connect4, depth - 1, alpha, beta, True)
                if tmp < value:
                    value = tmp
                    best_move = s
                if value < beta:
                    beta = value
                if value <= alpha:
                    break

        return value, best_move
