from gym_neutreeko.game.engine.gamelogic import NeutreekoEasyGame

env = NeutreekoEasyGame()
for i in range(0, 100):
    print(NeutreekoEasyGame.new_board())
    print()
