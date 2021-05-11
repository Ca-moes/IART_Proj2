# Onde vai ocorrer o jogo e haver a interação Agente-Ambiente
# https://github.com/towzeur/gym-abalone/blob/master/examples/demo.py
import numpy

from gym_neutreeko.game.engine.gamelogic import NeutreekoGame

if __name__ == "__main__":
    game = NeutreekoGame()
    board = NeutreekoGame.new_board()

    result = numpy.where(board == 1)
    print(result)
    listOfCoordinates = list(zip(result[0], result[1]))
    print(listOfCoordinates)