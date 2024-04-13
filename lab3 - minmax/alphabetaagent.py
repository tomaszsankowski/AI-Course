from exceptions import AgentException

import copy


class AlphaBetaAgent:
    def __init__(self, my_token='o', depth=4, check_heuristics=1):
        self.my_token = my_token
        self.depth = depth
        self.check_heuristics = check_heuristics

    def decide(self, connect4):
        if connect4.who_moves != self.my_token:
            raise AgentException('not my round')
        return self.alphabeta(connect4, self.depth, -10, 10, True)[1]

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
            if self.check_heuristics == 1:
                value = self.heuristic1(connect4)
            elif self.check_heuristics == 2:
                value = self.heuristic2(connect4)
            elif self.check_heuristics == 3:
                value = self.heuristic3(connect4)
            else:
                value = 0
            return value, None
        elif is_maximizing:  # my Round
            value = -2
            for s in connect4.possible_drops():
                tmp_connect4 = copy.deepcopy(connect4)
                tmp_connect4.drop_token(s)
                tmp, _ = self.alphabeta(tmp_connect4, depth - 1, alpha, beta, False)
                if tmp > value or best_move is None:
                    value = tmp
                    best_move = s
                if value > alpha:
                    alpha = value
                if value >= beta:
                    break
        else:  # opponent's Round
            value = 2
            for s in connect4.possible_drops():
                tmp_connect4 = copy.deepcopy(connect4)
                tmp_connect4.drop_token(s)
                tmp, _ = self.alphabeta(tmp_connect4, depth - 1, alpha, beta, True)
                if tmp < value or best_move is None:
                    value = tmp
                    best_move = s
                if value < beta:
                    beta = value
                if value <= alpha:
                    break

        return value, best_move

    def heuristic1(self, connect4):
        my_token = self.my_token
        opponent_token = 'o' if self.my_token == 'x' else 'x'

        fours = connect4.iter_fours()

        # checking for fours

        my_fours = sum(1 for four in fours if four.count(my_token) == 4)
        opponent_fours = sum(1 for four in fours if four.count(opponent_token) == 4)
        if my_fours > 0:
            return 1
        elif opponent_fours > 0:
            return -1

        # reward for every four where we can potentially win

        my_threes = sum(1 for four in fours if four.count(my_token) == 3 and four.count('_') == 1)
        opponent_threes = sum(1 for four in fours if four.count(opponent_token) == 3 and four.count('_') == 1)

        my_twos = sum(1 for four in fours if four.count(my_token) == 2 and four.count('_') == 2)
        opponent_twos = sum(1 for four in fours if four.count(opponent_token) == 2 and four.count('_') == 2)

        # reward for every pawn in middle of map

        my_center_pawns = connect4.center_column().count(my_token)
        opponent_center_pawns = connect4.center_column().count(opponent_token)

        # count score

        epsilon = 0.000001
        score = 0.6 * (my_threes - opponent_threes) / (epsilon + my_threes + opponent_threes)
        score += 0.4 * (my_twos - opponent_twos) / (epsilon + my_twos + opponent_twos)
        score += 0.0 * (my_center_pawns - opponent_center_pawns) / (epsilon + my_center_pawns + opponent_center_pawns)

        return score

    def heuristic2(self, connect4):
        my_token = self.my_token
        opponent_token = 'o' if self.my_token == 'x' else 'x'

        fours = connect4.iter_fours()

        # checking for fours

        my_fours = sum(1 for four in fours if four.count(my_token) == 4)
        opponent_fours = sum(1 for four in fours if four.count(opponent_token) == 4)
        if my_fours > 0:
            return 1
        elif opponent_fours > 0:
            return -1

        # reward for every four where we can potentially win

        my_threes = sum(1 for four in fours if four.count(my_token) == 3 and four.count('_') == 1)
        opponent_threes = sum(1 for four in fours if four.count(opponent_token) == 3 and four.count('_') == 1)

        my_twos = sum(1 for four in fours if four.count(my_token) == 2 and four.count('_') == 2)
        opponent_twos = sum(1 for four in fours if four.count(opponent_token) == 2 and four.count('_') == 2)

        # reward for every pawn in middle of map

        my_center_pawns = connect4.center_column().count(my_token)
        opponent_center_pawns = connect4.center_column().count(opponent_token)

        # count score

        epsilon = 0.000001
        score = 0.6 * (my_threes - opponent_threes) / (epsilon + my_threes + opponent_threes)
        score += 0.3 * (my_twos - opponent_twos) / (epsilon + my_twos + opponent_twos)
        score += 0.1 * (my_center_pawns - opponent_center_pawns) / (epsilon + my_center_pawns + opponent_center_pawns)

        return score

    def heuristic3(self, connect4):
        my_token = self.my_token
        opponent_token = 'o' if self.my_token == 'x' else 'x'

        fours = connect4.iter_fours()

        # checking for fours

        my_fours = sum(1 for four in fours if four.count(my_token) == 4)
        opponent_fours = sum(1 for four in fours if four.count(opponent_token) == 4)
        if my_fours > 0:
            return 1
        elif opponent_fours > 0:
            return -1

        # reward for every four where we can potentially win

        my_threes = sum(1 for four in fours if four.count(my_token) == 3 and four.count('_') == 1)
        opponent_threes = sum(1 for four in fours if four.count(opponent_token) == 3 and four.count('_') == 1)

        my_twos = sum(1 for four in fours if four.count(my_token) == 2 and four.count('_') == 2)
        opponent_twos = sum(1 for four in fours if four.count(opponent_token) == 2 and four.count('_') == 2)

        # reward for every pawn in middle of map

        my_center_pawns = connect4.center_column().count(my_token)
        opponent_center_pawns = connect4.center_column().count(opponent_token)

        # count score

        epsilon = 0.000001
        score = 0.5 * (my_threes - opponent_threes) / (epsilon + my_threes + opponent_threes)
        score += 0.3 * (my_twos - opponent_twos) / (epsilon + my_twos + opponent_twos)
        score += 0.2 * (my_center_pawns - opponent_center_pawns) / (epsilon + my_center_pawns + opponent_center_pawns)

        return score
