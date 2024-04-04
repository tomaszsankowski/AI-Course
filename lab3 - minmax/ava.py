from exceptions import GameplayException
from connect4 import Connect4
from randomagent import RandomAgent
from minmaxagent import MinMaxAgent
from alphabetaagent import AlphaBetaAgent

connect4 = Connect4(width=7, height=6)
agent1 = RandomAgent('o')
agent2 = MinMaxAgent('x', 5, True)
agent3 = MinMaxAgent('o', 5, False)
agent4 = AlphaBetaAgent('o', 6, 1)
agent5 = AlphaBetaAgent('x', 6, 2)
while not connect4.game_over:
    connect4.draw()
    try:
        if connect4.who_moves == agent4.my_token:
            n_column = agent4.decide(connect4)
        else:
            n_column = agent5.decide(connect4)
        print(n_column)
        connect4.drop_token(n_column)
    except (ValueError, GameplayException):
        print('invalid move')

connect4.draw()

# dla heurystyk 1 i 2 z reguły drugi gracz wygrywa
# dla heurystyki 1/2 i 0 z reguły drugi gracz przegrywa wygrywa
# nieuwzględnianie pionków na środku daje lepszy wynik
# waziejsze wydaje sie uwzglednianie trojek (3->0.8 2->0.2)
# czesciej wygrywa drugi gracz
# nieuzwglednianie srodkowych pionkow powoduje, ze gracze "buduja sie" od lewej strony
# oznacza to, ze gra bez uwzgledniania srodkowych jest mniej dynamiczna
