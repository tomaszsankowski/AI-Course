from exceptions import AgentException

import copy


class MinMaxAgent:
    def __init__(self, my_token='o'):
        self.my_token = my_token

    def decide(self, connect4):
        if connect4.who_moves != self.my_token:
            raise AgentException('not my round')
        else:
            return self.minimax(connect4, 4, True)[1]

    def minimax(self, connect4, depth, is_maximizing):
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
                tmp, _ = self.minimax(tmp_connect4, depth-1, False)
                if tmp > value:
                    value = tmp
                    best_move = s
        else:  # opponent's Round
            value = 1000
            for s in connect4.possible_drops():
                tmp_connect4 = copy.deepcopy(connect4)
                tmp_connect4.drop_token(s)
                tmp, _ = self.minimax(tmp_connect4, depth - 1, True)
                if tmp < value:
                    value = tmp
                    best_move = s

        return value, best_move
