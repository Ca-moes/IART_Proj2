# Onde vai ocorrer o jogo e haver a interação Agente-Ambiente
# https://github.com/towzeur/gym-abalone/blob/master/examples/demo.py
import numpy

from gym_neutreeko.game.engine.gamelogic import NeutreekoGame

if __name__ == "__main__":
    game = NeutreekoGame()
    game.reset()

    print(game.board)
    possible_moves = game.OLD_get_possible_moves(NeutreekoGame.WHITE)
    for move in possible_moves:
        print(move)

    # # Escolha de uma move (aleatório)
    # index1 = numpy.random.randint(0, len(possible_moves))
    # play_piece_position = possible_moves[index1]
    # index2 = numpy.random.randint(len(play_piece_position[1]))
    # play_direction = play_piece_position[1][index2]
    # print(f'Piece Position -> {play_piece_position[0]} \nDirection -> {play_direction}')
    # # Efetuar o move