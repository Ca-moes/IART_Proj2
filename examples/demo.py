# Onde vai ocorrer o jogo e haver a interação Agente-Ambiente
# https://github.com/towzeur/gym-abalone/blob/master/examples/demo.py
import numpy

from gym_neutreeko.game.engine.gamelogic import NeutreekoGame

if __name__ == "__main__":
    game = NeutreekoGame()
    game.reset()

    print(game.board)
    print(game.get_possible_moves(NeutreekoGame.WHITE))
